from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Setup Jinja2 for email templates
template_dir = Path(__file__).parent.parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        # For testing without domain verification, use a verified sender email
        # Go to SendGrid > Settings > Sender Authentication > Single Sender Verification
        # Verify any email you have access to (like your personal Gmail)
        self.from_email = Email(settings.FROM_EMAIL, settings.FROM_NAME)
    
    def _render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render email template with context."""
        template = jinja_env.get_template(template_name)
        return template.render(**context)
    
    async def send_lead_notification(
        self,
        contact_name: str,
        contact_email: str,
        contact_company: str,
        contact_message: str,
        submission_id: str
    ) -> bool:
        """Send new lead notification to ATTEC team."""
        try:
            html_content = self._render_template(
                "lead_notification.html",
                {
                    "contact_name": contact_name,
                    "contact_email": contact_email,
                    "contact_company": contact_company or "Not provided",
                    "contact_message": contact_message,
                    "submission_id": submission_id,
                }
            )
            
            message = Mail(
                from_email=self.from_email,
                to_emails=To(settings.NOTIFICATION_EMAIL),
                subject=f"New Lead: {contact_name} from {contact_company or 'Website'}",
                html_content=Content("text/html", html_content)
            )
            
            response = self.client.send(message)
            logger.info(f"Lead notification sent: {response.status_code}")
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            logger.error(f"Failed to send lead notification: {str(e)}")
            return False
    
    async def send_auto_reply(
        self,
        contact_name: str,
        contact_email: str
    ) -> bool:
        """Send auto-reply confirmation to contact."""
        try:
            html_content = self._render_template(
                "auto_reply.html",
                {
                    "contact_name": contact_name,
                }
            )
            
            message = Mail(
                from_email=self.from_email,
                to_emails=To(contact_email),
                subject="Thank you for contacting ATTEC",
                html_content=Content("text/html", html_content)
            )
            
            response = self.client.send(message)
            logger.info(f"Auto-reply sent to {contact_email}: {response.status_code}")
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            logger.error(f"Failed to send auto-reply to {contact_email}: {str(e)}")
            return False


# Singleton instance
email_service = EmailService()

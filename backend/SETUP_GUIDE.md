# ATTEC Backend - Setup & Deployment Guide

## 🚀 Quick Start

### 1. Set up Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your configuration
# Important variables:
# - DATABASE_URL: Your PostgreSQL connection string
# - SECRET_KEY: Generate a secure key (use: openssl rand -hex 32)
# - SENDGRID_API_KEY: Your SendGrid API key
# - FROM_EMAIL: Your sender email address
# - NOTIFICATION_EMAIL: Email to receive lead notifications
# - ADMIN_EMAIL and ADMIN_PASSWORD: Initial admin credentials
```

### 3. Set up Database

#### Option A: Local PostgreSQL

```bash
# Install PostgreSQL
# Create database
createdb attec

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/attec
```

#### Option B: Hosted PostgreSQL (Recommended for Production)

Use one of these services:
- **Railway**: Includes PostgreSQL
- **Render**: Free PostgreSQL tier
- **Supabase**: Free PostgreSQL tier
- **Neon**: Serverless PostgreSQL

Update `DATABASE_URL` in `.env` with the provided connection string.

### 4. Run Database Migrations

```bash
# Create initial migration
alembic upgrade head
```

### 5. Create Admin User

```bash
# Run the admin creation script
python scripts/create_admin.py

# You'll see output with the admin credentials
# ⚠️ Change the password after first login!
```

### 6. Start the Server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 7. Test the API

Visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

---

## 📧 SendGrid Setup

1. **Create Account**: Sign up at [SendGrid.com](https://signup.sendgrid.com/)
2. **Verify Sender**: Go to Settings → Sender Authentication
   - Add and verify your email address (hello@attec.co.ke)
3. **Create API Key**: Settings → API Keys → Create API Key
   - Choose "Restricted Access"
   - Grant "Mail Send" permissions
   - Copy the API key to `.env` as `SENDGRID_API_KEY`

### Testing Email

```python
# Test in Python console
from app.services.email_service import email_service
import asyncio

async def test():
    await email_service.send_auto_reply(
        contact_name="Test User",
        contact_email="your-email@example.com"
    )

asyncio.run(test())
```

---

## 🧪 Testing

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_contact.py
```

---

## 🚢 Deployment

### Option 1: Railway (Recommended)

1. **Create Account**: [railway.app](https://railway.app)

2. **Create New Project**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   
   # Add PostgreSQL
   railway add
   # Select: PostgreSQL
   ```

3. **Set Environment Variables**:
   - Go to project → Variables
   - Add all variables from `.env.example`
   - Railway will auto-provide `DATABASE_URL`

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Run Migrations**:
   ```bash
   railway run alembic upgrade head
   railway run python scripts/create_admin.py
   ```

### Option 2: Render

1. **Create Account**: [render.com](https://render.com)

2. **Create PostgreSQL Database**:
   - Dashboard → New → PostgreSQL
   - Copy the connection string

3. **Create Web Service**:
   - Dashboard → New → Web Service
   - Connect your Git repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:
   - Add all variables from `.env.example`
   - Use the PostgreSQL connection string for `DATABASE_URL`

5. **Deploy**:
   - Render will auto-deploy on git push

### Option 3: Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t attec-backend .

# Run
docker run -p 8000:8000 --env-file .env attec-backend
```

---

## 🔐 Security Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Change admin password from default
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS only (enforce in deployment platform)
- [ ] Update `ALLOWED_ORIGINS` with actual frontend domain
- [ ] Enable database backups
- [ ] Set up monitoring/logging
- [ ] Review and test rate limiting settings
- [ ] Verify email deliverability

---

## 📊 Database Management

### Create New Migration

```bash
# After modifying models
alembic revision --autogenerate -m "description of changes"

# Review the generated migration file
# Then apply it
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

### View Migration History

```bash
alembic history
alembic current
```

---

## 🔧 Troubleshooting

### Issue: Database connection error

```bash
# Check DATABASE_URL format
# PostgreSQL: postgresql://user:password@host:port/database
# Ensure PostgreSQL is running
# Check firewall/network settings
```

### Issue: Email not sending

```bash
# Check SendGrid API key is valid
# Verify sender email is authenticated in SendGrid
# Check SendGrid dashboard for errors
# Review logs: look for "Email sending failed" messages
```

### Issue: Import errors

```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version (3.11+ required)
python --version
```

### Issue: CORS errors from frontend

```bash
# Add frontend URL to ALLOWED_ORIGINS in .env
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com

# Restart the server after changes
```

---

## 📈 Monitoring & Logs

### View Logs

```bash
# Development
# Logs print to console

# Production (Railway)
railway logs

# Production (Render)
# View logs in Render dashboard
```

### Health Check

```bash
# Check API health
curl http://localhost:8000/health

# Should return:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "environment": "production"
# }
```

---

## 🔄 Updating the Backend

```bash
# Pull latest code
git pull

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Update dependencies
pip install -r requirements.txt

# Run new migrations
alembic upgrade head

# Restart server
```

---

## 💡 Tips

1. **Use Environment-Specific .env Files**:
   - `.env.development`
   - `.env.production`

2. **Set up Automated Backups**:
   - Most hosting platforms offer automatic database backups
   - Enable and configure retention policies

3. **Monitor Email Deliverability**:
   - Check SendGrid statistics regularly
   - Watch for bounces and complaints

4. **Set up Alerts**:
   - Configure alerts for API errors
   - Monitor database performance
   - Track submission rates

5. **Regular Maintenance**:
   - Review and clean old analytics data
   - Archive completed submissions
   - Update dependencies regularly

---

## 🆘 Support

If you encounter issues:

1. Check the logs for error messages
2. Review this documentation
3. Check FastAPI documentation: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
4. Check SQLAlchemy documentation for database issues
5. Review SendGrid documentation for email issues

---

**Backend is production-ready! 🚀**

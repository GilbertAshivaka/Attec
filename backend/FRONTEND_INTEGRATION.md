# Frontend Integration Guide

## Connecting React Frontend to FastAPI Backend

### 1. Update Contact Form Component

Replace the `handleSubmit` function in `frontend/src/components/Contact.jsx`:

```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  setIsSubmitting(true);
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    
    const data = await response.json();
    
    if (response.ok && data.success) {
      setSubmitted(true);
      setTimeout(() => {
        setSubmitted(false);
        setFormData({ name: '', email: '', company: '', message: '' });
      }, 3000);
    } else {
      // Handle error
      alert('Failed to submit. Please try again.');
    }
  } catch (error) {
    console.error('Error submitting form:', error);
    alert('Network error. Please check your connection.');
  } finally {
    setIsSubmitting(false);
  }
};
```

### 2. Add Loading State

Add this state to Contact.jsx:

```javascript
const [isSubmitting, setIsSubmitting] = useState(false);
```

Update the submit button:

```javascript
<button 
  type="submit" 
  className="contact-submit"
  disabled={isSubmitting}
>
  <Send size={20} />
  {isSubmitting ? 'Sending...' : 'Send Message'}
</button>
```

### 3. Optional: Add Analytics Tracking

Create a new file `frontend/src/utils/analytics.js`:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const trackEvent = async (eventType, eventData = {}) => {
  try {
    // Generate or get session ID
    let sessionId = sessionStorage.getItem('sessionId');
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      sessionStorage.setItem('sessionId', sessionId);
    }
    
    await fetch(`${API_URL}/api/v1/analytics/event`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        eventType,
        eventData,
        sessionId,
      }),
    });
  } catch (error) {
    // Silently fail - analytics shouldn't block the app
    console.error('Analytics error:', error);
  }
};

export const trackPageView = (page) => {
  trackEvent('page_view', { page });
};

export const trackClick = (button, location) => {
  trackEvent('button_click', { button, location });
};

export const trackServiceInterest = (service) => {
  trackEvent('service_interest', { service });
};
```

### 4. Use Analytics in Components

In `Hero.jsx`:

```javascript
import { trackClick } from '../utils/analytics';

// In the component
<a 
  href="#contact" 
  className="btn-primary"
  onClick={() => trackClick('Start AI Journey', 'hero')}
>
  Start Your AI Journey
</a>
```

In `Services.jsx`:

```javascript
import { trackServiceInterest, trackClick } from '../utils/analytics';

// In the component
<a 
  href="#contact" 
  className="service-cta"
  onClick={() => {
    trackServiceInterest(service.title);
    trackClick('Get Started', 'services');
  }}
>
  Get Started
</a>
```

In `App.jsx` (track page loads):

```javascript
import { useEffect } from 'react';
import { trackPageView } from './utils/analytics';

// In the component
useEffect(() => {
  trackPageView(window.location.pathname);
}, []);
```

### 5. Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

For production, create `frontend/.env.production`:

```env
VITE_API_URL=https://your-backend-domain.com
```

Update API calls to use:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### 6. Handle CORS During Development

The backend is already configured to allow the frontend URL. Make sure in `backend/.env`:

```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 7. Production Deployment

When deploying to production:

1. **Backend**:
   - Deploy to Railway/Render/etc.
   - Update `ALLOWED_ORIGINS` with production frontend URL
   - Update `FRONTEND_URL` in .env

2. **Frontend**:
   - Deploy to Vercel/Netlify/etc.
   - Set `VITE_API_URL` environment variable to backend URL

### 8. Testing the Integration

1. Start backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Start frontend:
   ```bash
   cd frontend
   pnpm dev
   ```

3. Test contact form:
   - Fill out and submit
   - Check browser console for any errors
   - Check backend logs for request
   - Check email (both auto-reply and notification)

4. Test analytics:
   - Open browser dev tools → Network tab
   - Click around the site
   - Should see POST requests to /api/v1/analytics/event

### 9. Optional: Create API Service Layer

Create `frontend/src/services/api.js`:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIService {
  async submitContact(data) {
    const response = await fetch(`${API_URL}/api/v1/contact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error('Failed to submit contact form');
    }
    
    return response.json();
  }
  
  async trackEvent(eventType, eventData, sessionId) {
    const response = await fetch(`${API_URL}/api/v1/analytics/event`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        eventType,
        eventData,
        sessionId,
      }),
    });
    
    return response.json();
  }
}

export default new APIService();
```

Then use it in components:

```javascript
import api from '../services/api';

// In handleSubmit
try {
  const result = await api.submitContact(formData);
  if (result.success) {
    setSubmitted(true);
  }
} catch (error) {
  console.error('Error:', error);
}
```

---

## Quick Checklist

- [ ] Backend is running on http://localhost:8000
- [ ] Frontend is running on http://localhost:5173
- [ ] CORS is configured correctly in backend .env
- [ ] Contact form submits successfully
- [ ] Auto-reply email is received
- [ ] Team notification email is received
- [ ] Analytics events are tracked (check backend logs)
- [ ] No CORS errors in browser console

---

## Troubleshooting

### CORS Error
```
Access to fetch at 'http://localhost:8000/api/v1/contact' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Fix**: Add frontend URL to `ALLOWED_ORIGINS` in backend `.env`

### Network Error
```
Failed to fetch
```

**Fix**: Make sure backend is running on port 8000

### 404 Not Found
```
POST http://localhost:8000/api/v1/contact 404
```

**Fix**: Check backend is running and endpoint exists at `/api/v1/contact`

### Email Not Sending
- Check SendGrid API key is valid
- Check sender email is verified in SendGrid
- Check backend logs for email errors

---

## Example: Complete Contact.jsx Update

Here's the complete updated Contact component:

```javascript
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { useState } from 'react';
import { Mail, Building, User, MessageSquare, Send, CheckCircle } from 'lucide-react';
import './Contact.css';

const Contact = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: '',
  });

  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError(''); // Clear error on input
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/v1/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        setSubmitted(true);
        setTimeout(() => {
          setSubmitted(false);
          setFormData({ name: '', email: '', company: '', message: '' });
        }, 5000);
      } else {
        setError(data.error?.message || 'Failed to submit. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="contact" className="contact" ref={ref}>
      {/* ... rest of component stays the same until the form ... */}
      
      <motion.form
        className="contact-form"
        onSubmit={handleSubmit}
        initial={{ opacity: 0, x: 30 }}
        animate={inView ? { opacity: 1, x: 0 } : {}}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        {submitted ? (
          <div className="contact-success">
            <CheckCircle size={48} />
            <h3>Thank You!</h3>
            <p>We've received your message and will get back to you within 24 hours.</p>
          </div>
        ) : (
          <>
            {error && (
              <div className="contact-error">
                <p>{error}</p>
              </div>
            )}
            
            <div className="form-group">
              <label htmlFor="name">
                <User size={18} />
                Full Name *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="John Doe"
                disabled={isSubmitting}
              />
            </div>

            {/* ... other form fields ... */}

            <button 
              type="submit" 
              className="contact-submit"
              disabled={isSubmitting}
            >
              <Send size={20} />
              {isSubmitting ? 'Sending...' : 'Send Message'}
            </button>
          </>
        )}
      </motion.form>
      
      {/* ... rest of component ... */}
    </section>
  );
};

export default Contact;
```

Add error styles to `Contact.css`:

```css
.contact-error {
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  color: #991b1b;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.contact-error p {
  margin: 0;
}

.contact-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

---

**You're all set! The frontend and backend are ready to work together! 🎉**

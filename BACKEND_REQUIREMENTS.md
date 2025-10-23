# ATTEC Backend - Requirements & Specifications

## 📋 Overview

The backend will serve as the API and business logic layer for the ATTEC website, handling contact form submissions, content management, analytics, and future service integrations.

---

## 🎯 Core Functionality Requirements

### 1. Contact Form Management

**Priority: HIGH** - Critical for lead generation

#### Features:
- ✅ Receive and validate contact form submissions
- ✅ Store form data in database
- ✅ Send email notifications to ATTEC team
- ✅ Send auto-reply confirmation to clients
- ✅ Spam protection (rate limiting, honeypot fields)
- ✅ Form submission tracking and analytics

#### API Endpoints:
```
POST /api/contact
- Body: { name, email, company, message }
- Response: { success, message, submissionId }
```

#### Email Templates:
1. **To ATTEC Team**: New lead notification with full details
2. **To Client**: Professional auto-reply confirming receipt and next steps

#### Database Schema:
```
ContactSubmissions
- id (UUID)
- name (String)
- email (String)
- company (String, optional)
- message (Text)
- submittedAt (DateTime)
- ipAddress (String)
- userAgent (String)
- status (enum: new, contacted, qualified, converted, archived)
- assignedTo (String, optional)
- notes (Text, optional)
- createdAt (DateTime)
- updatedAt (DateTime)
```

---

### 2. Content Management System (CMS)

**Priority: MEDIUM** - Important for easy updates without code changes

#### Features:
- ✅ Manage service offerings (title, description, price, features)
- ✅ Update company information (mission, values, team)
- ✅ Manage process steps
- ✅ Edit hero section content
- ✅ Update contact information
- ✅ Simple admin dashboard for non-technical updates

#### API Endpoints:
```
GET /api/services
- Response: Array of service objects

PUT /api/services/:id (Admin only)
- Body: Service object
- Response: Updated service

GET /api/content/:section
- Response: Content object for specific section

PUT /api/content/:section (Admin only)
- Body: Content object
- Response: Updated content
```

#### Database Schema:
```
Services
- id (UUID)
- title (String)
- icon (String)
- duration (String)
- price (String)
- description (Text)
- features (JSON Array)
- popular (Boolean)
- order (Integer)
- active (Boolean)
- createdAt (DateTime)
- updatedAt (DateTime)

Content
- id (UUID)
- section (String: hero, story, about, process, etc.)
- data (JSON)
- version (Integer)
- updatedAt (DateTime)
- updatedBy (String)
```

---

### 3. Authentication & Authorization

**Priority: MEDIUM** - Needed for admin panel access

#### Features:
- ✅ Admin login with email/password
- ✅ JWT-based authentication
- ✅ Password hashing (bcrypt)
- ✅ Protected admin routes
- ✅ Session management
- ✅ Password reset functionality

#### API Endpoints:
```
POST /api/auth/login
- Body: { email, password }
- Response: { token, user }

POST /api/auth/logout
- Response: { success }

POST /api/auth/refresh
- Response: { token }

POST /api/auth/reset-password
- Body: { email }
- Response: { success }

POST /api/auth/reset-password/:token
- Body: { password }
- Response: { success }
```

#### Database Schema:
```
Users
- id (UUID)
- email (String, unique)
- password (String, hashed)
- name (String)
- role (enum: admin, editor, viewer)
- active (Boolean)
- lastLogin (DateTime)
- createdAt (DateTime)
- updatedAt (DateTime)
```

---

### 4. Analytics & Tracking

**Priority: MEDIUM** - Important for understanding user behavior

#### Features:
- ✅ Track page views
- ✅ Track button clicks (CTA tracking)
- ✅ Track form submissions
- ✅ Track service interest (which service card gets most clicks)
- ✅ Basic user journey analytics
- ✅ Dashboard to view metrics

#### API Endpoints:
```
POST /api/analytics/event
- Body: { eventType, eventData, metadata }
- Response: { success }

GET /api/analytics/summary (Admin only)
- Query: { startDate, endDate, metric }
- Response: Analytics summary object

GET /api/analytics/leads (Admin only)
- Response: Lead conversion metrics
```

#### Database Schema:
```
AnalyticsEvents
- id (UUID)
- eventType (String: pageview, click, submission, etc.)
- eventData (JSON)
- sessionId (String)
- ipAddress (String)
- userAgent (String)
- referrer (String)
- timestamp (DateTime)

LeadMetrics
- id (UUID)
- date (Date)
- totalSubmissions (Integer)
- uniqueVisitors (Integer)
- conversionRate (Float)
- topServices (JSON)
- topSources (JSON)
```

---

### 5. Email Service Integration

**Priority: HIGH** - Critical for communication

#### Options (Choose One):
1. **SendGrid** (Recommended)
   - Reliable, scalable
   - Great deliverability
   - Free tier: 100 emails/day
   
2. **Resend** (Modern Alternative)
   - Developer-friendly
   - Great for transactional emails
   - Free tier: 3,000 emails/month

3. **AWS SES** (If using AWS)
   - Cost-effective at scale
   - Requires more setup

#### Features:
- ✅ Send notification emails
- ✅ Send auto-reply emails
- ✅ Email templates with dynamic content
- ✅ Email delivery tracking
- ✅ Handle bounces and complaints

---

### 6. File Upload & Storage (Future)

**Priority: LOW** - For case studies, blog images, team photos

#### Features:
- ✅ Upload images for blog posts
- ✅ Upload case study documents
- ✅ Team member photos
- ✅ Image optimization and resizing
- ✅ CDN integration

#### Storage Options:
1. **Cloudinary** (Recommended for images)
2. **AWS S3** (General file storage)
3. **Vercel Blob** (If hosting on Vercel)

---

## 🛠️ Technology Stack Recommendations

### Backend Framework
**Option 1: Node.js + Express** (Recommended for speed)
- Fast development
- Large ecosystem
- Easy integration with React
- Team likely familiar with JavaScript

**Option 2: Python + FastAPI**
- Great for AI integrations later
- Modern, fast
- Excellent documentation
- Type safety with Pydantic

**Recommendation**: **Node.js + Express** for MVP, considering JavaScript consistency with frontend

### Database
**Option 1: PostgreSQL** (Recommended)
- Robust, reliable
- Great for relational data
- JSON support for flexible fields
- Mature ecosystem

**Option 2: MongoDB**
- Flexible schema
- Good for rapid iteration
- JSON-native

**Recommendation**: **PostgreSQL** for data integrity and structure

### ORM/Database Tool
- **Prisma** (Recommended for Node.js)
  - Type-safe
  - Great migrations
  - Excellent developer experience
  
- **Drizzle ORM** (Alternative)
  - Lightweight
  - Great TypeScript support

### API Architecture
- **RESTful API** (Recommended for MVP)
  - Simple, well-understood
  - Easy to document
  - Wide client support

### Authentication
- **JWT** (JSON Web Tokens)
- **bcrypt** for password hashing
- **jsonwebtoken** for token generation

### Email Service
- **SendGrid** or **Resend** (Recommended)

### Validation
- **Zod** (TypeScript-first schema validation)
- **express-validator** (Alternative)

### Additional Tools
- **cors** - Handle cross-origin requests
- **helmet** - Security headers
- **express-rate-limit** - Rate limiting
- **dotenv** - Environment variables
- **winston** or **pino** - Logging
- **nodemailer** - Email sending (if not using service)

---

## 📁 Proposed Backend Structure

```
backend/
├── src/
│   ├── config/
│   │   ├── database.js          # DB connection
│   │   ├── email.js             # Email service config
│   │   └── auth.js              # Auth config
│   ├── controllers/
│   │   ├── contactController.js # Contact form logic
│   │   ├── authController.js    # Authentication logic
│   │   ├── contentController.js # CMS logic
│   │   ├── servicesController.js
│   │   └── analyticsController.js
│   ├── models/
│   │   ├── Contact.js           # Contact model
│   │   ├── User.js              # User model
│   │   ├── Service.js           # Service model
│   │   ├── Content.js           # Content model
│   │   └── AnalyticsEvent.js    # Analytics model
│   ├── routes/
│   │   ├── contact.js           # Contact routes
│   │   ├── auth.js              # Auth routes
│   │   ├── content.js           # Content routes
│   │   ├── services.js          # Services routes
│   │   └── analytics.js         # Analytics routes
│   ├── middleware/
│   │   ├── auth.js              # Auth middleware
│   │   ├── validation.js        # Request validation
│   │   ├── errorHandler.js      # Error handling
│   │   └── rateLimiter.js       # Rate limiting
│   ├── services/
│   │   ├── emailService.js      # Email sending logic
│   │   ├── analyticsService.js  # Analytics logic
│   │   └── crmService.js        # Future CRM integration
│   ├── utils/
│   │   ├── logger.js            # Logging utility
│   │   ├── validators.js        # Data validators
│   │   └── helpers.js           # Helper functions
│   ├── templates/
│   │   ├── email/
│   │   │   ├── leadNotification.html
│   │   │   └── autoReply.html
│   ├── app.js                   # Express app setup
│   └── server.js                # Server entry point
├── prisma/
│   ├── schema.prisma            # Database schema
│   └── migrations/              # DB migrations
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .gitignore
├── package.json
├── README.md
└── tsconfig.json (if using TypeScript)
```

---

## 🔐 Security Requirements

### Must-Have Security Features:
1. ✅ **Input Validation** - Validate all user inputs
2. ✅ **SQL Injection Protection** - Use parameterized queries (Prisma handles this)
3. ✅ **XSS Protection** - Sanitize inputs, use helmet
4. ✅ **CORS Configuration** - Whitelist frontend domain
5. ✅ **Rate Limiting** - Prevent abuse (100 requests/15min per IP)
6. ✅ **Password Hashing** - bcrypt with salt rounds
7. ✅ **HTTPS Only** - Enforce in production
8. ✅ **Environment Variables** - Never commit secrets
9. ✅ **Error Handling** - Don't leak system info
10. ✅ **Request Size Limits** - Prevent large payload attacks

---

## 🚀 MVP vs Future Features

### MVP (Minimum Viable Product) - Build First
✅ Contact form API
✅ Email notifications
✅ Basic admin authentication
✅ Contact submission storage
✅ Basic analytics (form submissions)
✅ CORS and security setup
✅ Error handling and logging

### Phase 2 - After Launch
⏳ Full CMS for content management
⏳ Advanced analytics dashboard
⏳ Lead scoring system
⏳ Email campaign management
⏳ File upload for case studies
⏳ Blog management system
⏳ Testimonials management

### Phase 3 - Scale Features
⏳ CRM integration (HubSpot, Salesforce)
⏳ Payment processing for service bookings
⏳ Client portal
⏳ Project management integration
⏳ Calendar booking (Calendly integration)
⏳ Live chat integration
⏳ Multi-language support

---

## 📊 API Response Standards

### Success Response:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [ ... ]
  }
}
```

### HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

---

## 🌍 Environment Variables

```env
# Server
NODE_ENV=development
PORT=5000
API_URL=http://localhost:5000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/attec

# Frontend
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,https://attec.co.ke

# Authentication
JWT_SECRET=your-super-secret-key
JWT_EXPIRES_IN=7d
REFRESH_TOKEN_SECRET=your-refresh-secret

# Email Service (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=hello@attec.co.ke
NOTIFICATION_EMAIL=team@attec.co.ke

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Admin
ADMIN_EMAIL=admin@attec.co.ke
ADMIN_PASSWORD=temporary-password-change-on-first-login
```

---

## 📈 Performance Requirements

- **Response Time**: < 200ms for API calls
- **Uptime**: 99.9% availability target
- **Concurrent Users**: Support 100+ simultaneous users
- **Database Queries**: Optimized with indexes
- **Caching**: Implement for frequently accessed data

---

## 🧪 Testing Strategy

### Unit Tests:
- Controller functions
- Service functions
- Validation logic
- Utility functions

### Integration Tests:
- API endpoints
- Database operations
- Email sending
- Authentication flow

### Tools:
- **Jest** - Testing framework
- **Supertest** - API testing
- **@faker-js/faker** - Test data generation

---

## 📝 Documentation Requirements

1. **API Documentation** - Swagger/OpenAPI spec
2. **Setup Guide** - How to run locally
3. **Deployment Guide** - Production deployment steps
4. **Database Schema** - Entity relationship diagram
5. **Environment Setup** - Required variables
6. **Contribution Guide** - For team members

---

## 🚀 Deployment Strategy

### Hosting Options:

**Option 1: Vercel (Recommended for Serverless)**
- Easy deployment
- Automatic scaling
- Works well with Next.js if you migrate frontend
- Vercel Postgres available

**Option 2: Railway**
- Simple deployment
- Database included
- Good for Node.js apps
- Affordable pricing

**Option 3: Render**
- Free tier available
- PostgreSQL included
- Auto-deploy from GitHub

**Option 4: AWS (Traditional)**
- EC2 + RDS
- More control
- Requires more setup
- Better for scale

**Recommendation**: **Railway** or **Render** for MVP (easy + affordable)

---

## 🎯 Success Metrics

### Technical Metrics:
- ✅ 100% API uptime
- ✅ < 200ms average response time
- ✅ Zero data loss
- ✅ All tests passing

### Business Metrics:
- ✅ Contact form submission rate > 2%
- ✅ Email delivery rate > 95%
- ✅ Lead response time < 24 hours
- ✅ Zero spam submissions getting through

---

## 💰 Estimated Costs (Monthly)

### MVP Phase:
- **Hosting (Railway/Render)**: $0-20 (free tier or basic)
- **Database (PostgreSQL)**: Included in hosting
- **Email (SendGrid)**: $0 (free tier - 100/day)
- **Domain**: ~$1/month (already have)
- **SSL**: $0 (included with hosting)

**Total MVP**: ~$0-20/month

### Growth Phase:
- **Hosting**: $20-50
- **Database**: Included or $10-20
- **Email**: $20-50 (paid tier for more volume)
- **CDN/Storage**: $5-10

**Total Growth**: ~$50-130/month

---

## ✅ What I Recommend for MVP

### Build First (Priority Order):

1. **Contact Form API** ⭐⭐⭐
   - This is THE most critical feature
   - Enables lead generation immediately
   - Simple but essential

2. **Email Notifications** ⭐⭐⭐
   - Auto-reply to clients
   - Notify ATTEC team
   - Professional communication

3. **Basic Admin Auth** ⭐⭐
   - Secure admin endpoints
   - View submitted contacts
   - Basic dashboard

4. **Contact Storage** ⭐⭐⭐
   - PostgreSQL database
   - Store all submissions
   - Track status

5. **Security & Rate Limiting** ⭐⭐⭐
   - Prevent spam
   - Protect API
   - Essential for production

6. **Basic Analytics** ⭐
   - Track submissions
   - Source tracking
   - Simple metrics

### Skip for Now (Build Later):
- Full CMS (you can edit code for now)
- Advanced analytics dashboard
- File uploads
- Payment processing

---

## 🤔 Questions for You to Consider

Before I start building, please confirm:

1. **Tech Stack**: Node.js + Express + PostgreSQL + Prisma? ✓
2. **Email Service**: SendGrid or Resend? (I recommend SendGrid)
3. **Hosting**: Railway, Render, or Vercel? (I recommend Railway)
4. **MVP Scope**: Focus on contact form + email + basic admin? ✓
5. **TypeScript**: Use TypeScript or plain JavaScript? (TypeScript recommended)
6. **Admin Panel**: Build simple API-only or include basic frontend dashboard?

---

## 📋 Summary

This backend will:
- ✅ Handle contact form submissions professionally
- ✅ Send automated emails to you and clients
- ✅ Store leads in PostgreSQL database
- ✅ Provide secure admin access to view submissions
- ✅ Track basic analytics
- ✅ Be production-ready with proper security
- ✅ Scale as ATTEC grows
- ✅ Cost almost nothing to start (~$0-20/month)

**Ready to build when you approve!** 🚀

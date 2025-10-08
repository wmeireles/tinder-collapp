# 📚 Collapp API Documentation

## 🚀 Base URL
```
http://localhost:8000
```

## 🔐 Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## 📋 Endpoints

### 🔑 Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### 👤 Onboarding
- `POST /onboarding/step1` - Complete step 1 (basic info)
- `POST /onboarding/step2` - Complete step 2 (social media)
- `POST /onboarding/step3` - Complete step 3 (preferences)
- `POST /onboarding/complete` - Mark onboarding as complete
- `GET /onboarding/status` - Get onboarding status

### 💕 Matching
- `GET /matching/discover` - Get potential matches
- `POST /matching/swipe` - Swipe on a user
- `GET /matching/matches` - Get user matches

### 💬 Chat
- `GET /chat/chats` - Get user chats
- `GET /chat/{chat_id}/messages` - Get chat messages
- `POST /chat/{chat_id}/messages` - Send message

### 🎯 Wanted Posts
- `POST /wanted/posts` - Create wanted post
- `GET /wanted/posts` - Browse wanted posts
- `GET /wanted/my-posts` - Get user's wanted posts
- `POST /wanted/applications` - Apply to wanted post

### 🤖 AI Features
- `POST /ai/analyze-match` - Get AI match analysis
- `POST /ai/suggest-collaboration` - Get collaboration suggestions
- `POST /ai/generate-mediakit` - Generate media kit content

### 📧 Invitations
- `POST /invitations/create` - Create invitation
- `GET /invitations/my-invitations` - Get user invitations
- `POST /invitations/use` - Use invitation code

### 🔗 Link in Bio
- `POST /linkinbio/create` - Create link page
- `GET /linkinbio/my-pages` - Get user pages
- `GET /linkinbio/{slug}` - Get public page
- `PUT /linkinbio/{slug}` - Update page

### 📊 Media Kit
- `POST /mediakit/create` - Create media kit
- `GET /mediakit/my-mediakit` - Get user media kit
- `GET /mediakit/{user_id}` - Get public media kit
- `PUT /mediakit/update` - Update media kit

### 🔔 Notifications
- `GET /notifications/` - Get notifications
- `GET /notifications/unread` - Get unread notifications
- `PUT /notifications/{id}/read` - Mark as read
- `PUT /notifications/mark-all-read` - Mark all as read
- `GET /notifications/count` - Get unread count

### 💼 Offers
- `POST /offers/create` - Create offer
- `GET /offers/my-offers` - Get user offers
- `GET /offers/browse` - Browse offers
- `GET /offers/{offer_id}` - Get offer details
- `PUT /offers/{offer_id}` - Update offer
- `POST /offers/{offer_id}/accept` - Accept offer

### 💳 Subscriptions
- `GET /subscriptions/plans` - Get available plans
- `GET /subscriptions/my-subscription` - Get user subscription
- `POST /subscriptions/upgrade` - Upgrade subscription
- `POST /subscriptions/cancel` - Cancel subscription
- `GET /subscriptions/usage` - Get usage stats

### 🏥 Health
- `GET /health/` - Basic health check
- `GET /health/db` - Database health check

## 📝 Request/Response Examples

### Register User
```json
POST /auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response:
{
  "id": "uuid",
  "email": "user@example.com",
  "name": null,
  "plan": "free",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Create Offer
```json
POST /offers/create
{
  "title": "Instagram Post Collaboration",
  "description": "Looking for fashion brands to collaborate",
  "package_details": {
    "deliverables": ["1 Instagram post", "3 stories"],
    "audience": "25K followers, 18-35 age group"
  },
  "price": 500.00,
  "currency": "USD",
  "delivery_time": 7
}
```

## 🚨 Error Responses
```json
{
  "detail": "Error message"
}
```

## 📊 Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

## 🔒 Rate Limiting
- 100 requests per minute per IP
- Authenticated users may have higher limits based on subscription

## 📱 WebSocket Support
Real-time features available at:
- `/ws/chat/{chat_id}` - Real-time messaging
- `/ws/notifications` - Real-time notifications
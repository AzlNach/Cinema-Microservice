# Cinema Booking Microservices System

A comprehensive cinema booking platform built with microservices architecture, featuring separate services for user management, movie catalog, cinema operations, booking system, payments, and promotional coupons.

## 🎬 System Overview

This project implements a complete cinema booking ecosystem using microservices architecture with GraphQL API gateway. The system provides both public access for browsing movies and cinemas, and authenticated features for booking management.

## 🏗️ Architecture & Technical Stack

### **Microservices Architecture**
- **API Gateway**: Centralized entry point using Flask with GraphQL endpoint
- **6 Independent Services**: Each with dedicated databases and responsibilities
- **Service Communication**: Internal GraphQL-based communication between services
- **Database Per Service**: MySQL databases with service-specific schemas

### **Technology Stack**
- **Backend**: Python Flask for all services
- **API Layer**: GraphQL with Graphene library
- **Database**: MySQL 8.0 with dedicated schemas per service
- **Frontend**: Vanilla JavaScript with Bootstrap 5.3
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT-based token authentication

### **Security Features**
- Private internal network for service communication
- No direct database access from external networks
- JWT token-based authentication and authorization
- Role-based access control (Admin/User)

## 🚀 Core Functionality

### **Public Features (No Authentication Required)**
- **Movie Browsing**: View movie catalog with details, ratings, and descriptions
- **Cinema Discovery**: Browse cinema locations with facility information
- **Showtime Viewing**: Check available movie showtimes across cinemas

### **User Features (Authentication Required)**
- **Account Management**: Registration, login, profile management
- **Ticket Booking**: Select movies, choose seats, complete bookings
- **Payment Processing**: Secure payment handling with multiple methods
- **Booking History**: View past and upcoming bookings
- **Coupon Usage**: Apply discount coupons during booking

### **Admin Features (Admin Role Required)**
- **Content Management**: CRUD operations for movies and cinemas
- **User Management**: View and manage user accounts
- **Booking Oversight**: Monitor all system bookings
- **System Analytics**: Dashboard with key metrics and statistics

## 🏢 Service Architecture

### **1. Gateway Service** (Port 5000)
```
Responsibilities:
- Single entry point for all client requests
- GraphQL schema aggregation from all services
- Request routing and load balancing
- Authentication token validation
- Static file serving for frontend
```

### **2. User Service** (Port 3012)
```
Responsibilities:
- User registration and authentication
- JWT token generation and validation
- User profile management
- Role-based access control
- Password security and validation
```

### **3. Movie Service** (Port 3010)
```
Responsibilities:
- Movie catalog management
- Movie metadata (title, genre, duration, rating)
- Poster image management
- Public movie browsing API
- Admin movie CRUD operations
```

### **4. Cinema Service** (Port 3008)
```
Responsibilities:
- Cinema location management
- Auditorium and seating configuration
- Cinema capacity management
- Geographic location data
- Facility information management
```

### **5. Booking Service** (Port 3007)
```
Responsibilities:
- Ticket booking workflow
- Seat selection and reservation
- Booking status management
- Showtime scheduling
- Booking history tracking
```

### **6. Payment Service** (Port 3011)
```
Responsibilities:
- Payment processing workflow
- Multiple payment method support
- Transaction status tracking
- Payment history and receipts
- Refund processing capabilities
```

### **7. Coupon Service** (Port 3009)
```
Responsibilities:
- Promotional coupon management
- Discount calculation logic
- Coupon validation and usage tracking
- Expiration date management
- Usage limit enforcement
```

## 📊 System Flow & User Journey

### **Public User Flow**
```
1. Landing Page → Browse Movies/Cinemas
2. View Details → Check Showtimes
3. Login Prompt → Registration/Authentication
4. Authenticated Access → Full Booking Features
```

### **Booking Process Flow**
```
1. User Authentication (User Service)
2. Movie Selection (Movie Service)
3. Cinema & Showtime Selection (Cinema Service)
4. Seat Selection (Booking Service)
5. Coupon Application (Coupon Service)
6. Payment Processing (Payment Service)
7. Booking Confirmation (Booking Service)
8. Email/SMS Notification
```

### **Admin Management Flow**
```
1. Admin Authentication
2. Dashboard Access
3. Content Management (Movies/Cinemas)
4. User Management
5. Booking Oversight
6. System Analytics
```

## 🛠️ Database Schema

### **Database Structure**
```
- user_db: Users, authentication, roles
- movie_db: Movies, ratings, metadata
- cinema_db: Cinemas, auditoriums, seating
- booking_db: Bookings, tickets, showtimes
- payment_db: Transactions, payment methods
- coupon_db: Coupons, usage tracking
```

### **Inter-Service Relationships**
```
Bookings → Users (user_id)
Bookings → Movies (movie_id)  
Bookings → Cinemas (auditorium_id)
Payments → Bookings (booking_id)
Coupon Usage → Users (user_id)
```

## 🚀 Deployment & Setup

### **Prerequisites**
- Docker & Docker Compose
- Git
- Port 5000 available for gateway

### **Quick Start**
```bash
# Clone repository
git clone <repository-url>
cd cinema-microservices

# Start all services
docker-compose up --build

# Access application
open http://localhost:5000
```

### **Service Health Monitoring**
- Each service includes health check endpoints
- Automatic service discovery and registration
- Graceful failure handling and recovery

## 🔒 Security Implementation

### **Authentication & Authorization**
- JWT tokens with configurable expiration
- Role-based access control (RBAC)
- Password hashing and validation
- Session management

### **Network Security**
- Internal Docker network isolation
- No direct database access from external networks
- Service-to-service communication encryption
- API rate limiting and request validation

## 📱 Frontend Features

### **Responsive Design**
- Mobile-first responsive layout
- Progressive Web App capabilities
- Cross-browser compatibility
- Accessibility compliance (WCAG 2.1)

### **User Experience**
- Interactive seat selection
- Real-time availability updates
- Smooth animations and transitions
- Intuitive navigation and flow

### **Admin Dashboard**
- Comprehensive analytics dashboard
- Real-time data visualization
- Bulk operations support
- Export capabilities for reports

## 🔧 Development & Maintenance

### **Code Organization**
- Modular service architecture
- Consistent coding standards across services
- Comprehensive error handling
- Detailed logging and monitoring

### **Testing Strategy**
- Unit tests for individual services
- Integration tests for service communication
- End-to-end testing for complete user flows
- Performance testing for scalability

### **Monitoring & Observability**
- Health check endpoints for all services
- Centralized logging aggregation
- Performance metrics collection
- Error tracking and alerting

This cinema booking system demonstrates modern microservices architecture principles while providing a complete, production-ready application for cinema operations management.
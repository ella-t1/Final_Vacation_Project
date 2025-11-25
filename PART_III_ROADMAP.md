# Part III Implementation Roadmap - Statistics Website

## Overview
This roadmap provides a step-by-step guide to implement the statistics website (`stats_website`) as Part III of the project. The project will include a separate backend (Flask) and frontend (React) that connects to the same PostgreSQL database and provides statistics accessible only to Admin users.

---

## Phase 1: Project Structure Setup

### Step 1.1: Create Directory Structure
```
stats_website/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── dal/
│   │   │   ├── __init__.py
│   │   │   ├── base_dao.py
│   │   │   ├── user_dao.py
│   │   │   ├── vacation_dao.py
│   │   │   ├── like_dao.py
│   │   │   └── role_dao.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   └── statistics_service.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── app.py
│   │       └── routes.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Nav/
│   │   │   │   ├── Nav.tsx
│   │   │   │   └── Nav.scss
│   │   │   └── ProtectedRoute/
│   │   │       └── ProtectedRoute.tsx
│   │   ├── pages/
│   │   │   ├── Home/
│   │   │   │   ├── Home.tsx
│   │   │   │   └── Home.scss
│   │   │   ├── Login/
│   │   │   │   ├── Login.tsx
│   │   │   │   └── Login.scss
│   │   │   ├── Statistics/
│   │   │   │   ├── Statistics.tsx
│   │   │   │   └── Statistics.scss
│   │   │   └── About/
│   │   │       ├── About.tsx
│   │   │       └── About.scss
│   │   ├── store/
│   │   │   ├── authSlice.ts
│   │   │   └── store.ts
│   │   ├── utils/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
└── docker-compose.yml (at project root)
```

### Step 1.2: Initialize Backend Project
- Create `stats_website/backend/` directory
- Set up Python virtual environment structure
- Create `requirements.txt` with Flask dependencies

### Step 1.3: Initialize Frontend Project
- Create `stats_website/frontend/` directory
- Initialize React + TypeScript + Vite project
- Install dependencies (React Router, Redux Toolkit, Axios, etc.)

---

## Phase 2: Backend Implementation

### Step 2.1: Database Configuration
**File: `stats_website/backend/src/config.py`**
- Copy and adapt database configuration from `website_vacations/backend/src/config.py`
- Use same database connection settings (same PostgreSQL database)
- Ensure environment variables are properly configured

### Step 2.2: Data Access Layer (DAL)
**Files: `stats_website/backend/src/dal/*.py`**
- Copy `base_dao.py` from vacations project
- Copy and adapt DAOs:
  - `user_dao.py` - for user queries
  - `vacation_dao.py` - for vacation queries
  - `like_dao.py` - for likes queries
  - `role_dao.py` - for role queries
- Add new methods needed for statistics:
  - `VacationDAO.get_vacations_by_date_range()` - categorize by past/ongoing/future
  - `LikeDAO.get_distribution_by_destination()` - group likes by vacation destination
  - `UserDAO.count_total()` - count all users
  - `LikeDAO.count_total()` - count all likes

### Step 2.3: Business Logic Layer (Services)
**File: `stats_website/backend/src/services/auth_service.py`**
- Implement authentication service:
  - `login(username, password)` - verify credentials and check Admin role
  - `logout()` - handle session cleanup
  - `is_admin(user_id)` - verify admin status

**File: `stats_website/backend/src/services/statistics_service.py`**
- Implement statistics service:
  - `get_vacation_stats()` - returns past/ongoing/future counts
  - `get_total_users()` - returns total user count
  - `get_total_likes()` - returns total likes count
  - `get_likes_distribution()` - returns likes grouped by destination

### Step 2.4: API Routes
**File: `stats_website/backend/src/api/routes.py`**
- Implement routes:
  - `POST /login` - Admin login only
  - `POST /logout` - Logout
  - `GET /vacations/stats` - Returns `{pastVacations, ongoingVacations, futureVacations}`
  - `GET /users/total` - Returns `{totalUsers}`
  - `GET /likes/total` - Returns `{totalLikes}`
  - `GET /likes/distribution` - Returns `[{destination, likes}, ...]`
- Add authentication middleware to protect statistics routes

**File: `stats_website/backend/src/api/app.py`**
- Create Flask app instance
- Configure CORS for frontend
- Register routes
- Set up error handlers

**File: `stats_website/backend/src/main.py`**
- Entry point for running the Flask app
- Configure host, port, debug mode

### Step 2.5: Session Management
- Implement session-based authentication
- Store admin session after login
- Validate session on protected routes
- Clear session on logout

### Step 2.6: Backend Testing
- Test all API endpoints
- Test authentication flow
- Test statistics calculations
- Verify Admin-only access

---

## Phase 3: Frontend Implementation

### Step 3.1: Project Setup
- Initialize React + TypeScript + Vite project
- Install dependencies:
  - `react-router-dom` - for routing
  - `@reduxjs/toolkit` + `react-redux` - for state management
  - `axios` - for API calls
  - `sass` - for styling

### Step 3.2: State Management
**File: `stats_website/frontend/src/store/authSlice.ts`**
- Create Redux slice for authentication:
  - `isAuthenticated` - boolean
  - `user` - user object
  - `login()` - async thunk for login
  - `logout()` - action for logout

**File: `stats_website/frontend/src/store/store.ts`**
- Configure Redux store
- Export typed hooks (`useAppDispatch`, `useAppSelector`)

### Step 3.3: API Utilities
**File: `stats_website/frontend/src/utils/api.ts`**
- Create axios instance with base URL
- Configure interceptors for authentication
- Create API functions:
  - `login(username, password)`
  - `logout()`
  - `getVacationStats()`
  - `getTotalUsers()`
  - `getTotalLikes()`
  - `getLikesDistribution()`

### Step 3.4: Components

**Navigation Component: `stats_website/frontend/src/components/Nav/Nav.tsx`**
- Create navigation menu
- Links to: Home, Login, Statistics, About
- Show/hide links based on authentication status
- Logout button for authenticated users

**Protected Route Component: `stats_website/frontend/src/components/ProtectedRoute/ProtectedRoute.tsx`**
- Create wrapper component for protected routes
- Redirect to login if not authenticated
- Render children if authenticated

### Step 3.5: Pages

**Home Page: `stats_website/frontend/src/pages/Home/Home.tsx`**
- Display title
- Show statistics-related image
- Explain the system
- Include navigation menu

**Login Page: `stats_website/frontend/src/pages/Login/Login.tsx`**
- Username and password form
- Handle login submission
- Display error messages for non-admin users
- Redirect to Statistics page on success

**Statistics Page: `stats_website/frontend/src/pages/Statistics/Statistics.tsx`**
- Protected route (only for logged-in users)
- Fetch and display all statistics:
  - Vacation statistics (past/ongoing/future)
  - Total users
  - Total likes
  - Likes distribution (with destination names)
- Display data in an aesthetic, clear format
- **Bonus**: Add charts/graphs (using Chart.js or Recharts)
- **Bonus**: Add filtering widgets

**About Page: `stats_website/frontend/src/pages/About/About.tsx`**
- Display developer information
- Personal details

**Page Not Found: `stats_website/frontend/src/pages/NotFound/NotFound.tsx`**
- Create 404 page component

### Step 3.6: Routing
**File: `stats_website/frontend/src/App.tsx`**
- Set up React Router:
  - `/` - Home page (default route)
  - `/login` - Login page
  - `/statistics` - Statistics page (protected)
  - `/about` - About page
  - `/*` - Page not found (404)
- Wrap protected routes with `ProtectedRoute` component

### Step 3.7: Styling
- Create SCSS files for each component/page
- Implement modern, aesthetic design
- Ensure responsive layout
- Use consistent color scheme and typography

### Step 3.8: Frontend Testing (Bonus)
- Write tests for:
  - Home page rendering
  - Login page functionality
  - Statistics page data display
  - Protected route behavior

---

## Phase 4: Docker Setup

### Step 4.1: Backend Dockerfile
**File: `stats_website/backend/Dockerfile`**
- Use Python base image
- Set working directory
- Copy requirements.txt and install dependencies
- Copy source code
- Expose port (e.g., 5001)
- Set CMD to run Flask app

### Step 4.2: Frontend Dockerfile
**File: `stats_website/frontend/Dockerfile`**
- Use Node.js base image for build stage
- Build React app
- Use nginx or serve static files
- Expose port (e.g., 3000 or 80)

### Step 4.3: Docker Compose
**File: `docker-compose.yml` (at project root)**
- Define services:
  - `postgres` - PostgreSQL database (shared)
  - `vacations-backend` - Existing vacations backend
  - `vacations-frontend` - Existing vacations frontend
  - `stats-backend` - New statistics backend
  - `stats-frontend` - New statistics frontend
- Configure:
  - Environment variables
  - Port mappings
  - Volume mounts
  - Network configuration
  - Dependencies (stats services depend on postgres)
- Add initialization script to load initial data

### Step 4.4: Test Docker Setup Locally
- Build all images: `docker-compose build`
- Start all services: `docker-compose up`
- Verify all services are running
- Test API endpoints
- Test frontend access

---

## Phase 5: Cloud Deployment (AWS)

### Step 5.1: Prepare Docker Images
- Ensure all Dockerfiles are production-ready
- Optimize image sizes
- Test images locally

### Step 5.2: Push to Docker Hub
- Create Docker Hub account (if not exists)
- Tag images:
  - `yourusername/vacations-backend:latest`
  - `yourusername/vacations-frontend:latest`
  - `yourusername/stats-backend:latest`
  - `yourusername/stats-frontend:latest`
- Push images: `docker push <image-name>`

### Step 5.3: AWS Setup
- Create AWS account
- Set up EC2 instance or ECS
- Install Docker and Docker Compose on AWS instance
- Configure security groups (open ports for services)

### Step 5.4: Deploy on AWS
- Pull images from Docker Hub: `docker pull <image-name>`
- Copy `docker-compose.yml` to AWS instance
- Update environment variables for cloud environment
- Run: `docker-compose up -d`
- Verify all services are running

### Step 5.5: Configure Domain/URLs (Optional)
- Set up domain names or use AWS public IPs
- Configure reverse proxy (nginx) if needed
- Test public access

---

## Phase 6: Documentation & Finalization

### Step 6.1: Update README.md
**File: `README.md` (at project root)**
- Add student full name
- Instructions for running entire project with `docker-compose`
- Project structure overview
- Environment variables documentation
- Additional notes/comments

### Step 6.2: Requirements Files
- Ensure `stats_website/backend/requirements.txt` contains all dependencies (`pip freeze`)
- Ensure `website_vacations/backend/requirements.txt` is up to date

### Step 6.3: Code Quality
- Add docstrings to all functions and classes
- Add type hints
- Ensure clean code:
  - Fields start with lowercase
  - Classes start with uppercase
  - Separate classes into different files
- Remove any debug code

### Step 6.4: Git Repository
- Ensure `.gitignore` excludes:
  - `venv/`
  - `node_modules/`
  - `__pycache__/`
  - `.env` files
- Commit all changes
- Push to GitHub
- Verify repository structure matches requirements

---

## Phase 7: Testing & Validation

### Step 7.1: Functional Testing
- Test Admin login flow
- Test non-admin login rejection
- Test all statistics endpoints
- Test logout functionality
- Test protected routes
- Test navigation between pages

### Step 7.2: Integration Testing
- Test full flow: Login → View Statistics → Logout
- Test error handling
- Test API connectivity
- Test database queries

### Step 7.3: Docker Testing
- Test local Docker Compose setup
- Verify all containers start correctly
- Test inter-service communication
- Test database initialization

### Step 7.4: Cloud Testing
- Test AWS deployment
- Verify public access
- Test all endpoints from cloud
- Monitor logs for errors

---

## Implementation Order Summary

1. **Week 1: Backend Foundation**
   - Phase 1: Project Structure
   - Phase 2: Backend Implementation (Steps 2.1-2.4)

2. **Week 2: Frontend & Integration**
   - Phase 2: Backend Testing (Step 2.6)
   - Phase 3: Frontend Implementation

3. **Week 3: Docker & Deployment**
   - Phase 4: Docker Setup
   - Phase 5: Cloud Deployment

4. **Week 4: Polish & Submit**
   - Phase 6: Documentation
   - Phase 7: Testing & Validation

---

## Key Requirements Checklist

- [ ] Separate project from vacations website
- [ ] Connects to same PostgreSQL database
- [ ] Flask backend with all required API routes
- [ ] React frontend with all required pages
- [ ] Admin-only authentication
- [ ] Statistics endpoints return correct data
- [ ] Docker setup for all components
- [ ] Docker Compose for entire system
- [ ] Images pushed to Docker Hub
- [ ] Deployed on AWS Cloud
- [ ] README.md with instructions
- [ ] Clean, documented code
- [ ] Git repository properly structured

---

## Notes

- Use the same database connection approach as the vacations project
- Reuse DAO patterns from vacations project where possible
- Ensure Admin role check is robust (role_id = 1 or role name = "Admin")
- Statistics calculations must be accurate (past = end_date < today, ongoing = start_date <= today <= end_date, future = start_date > today)
- Likes distribution should join with vacations table to get destination names
- Frontend should handle loading states and errors gracefully
- All routes should be properly protected

---

## Submission Deadline
**01/09/2025**

Good luck! 🚀


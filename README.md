# InterLeet 🚀

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)

A comprehensive **AI-powered interview preparation and coding challenge platform** that helps developers and job seekers master technical interviews through intelligent mock interviews, coding problems, and system design challenges.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture Overview](#-architecture-overview)
- [MNC Scalability & Good Practices](#-mnc-scalability--good-practices)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Environment Setup](#-environment-setup)
- [Running the Application](#-running-the-application)
- [Build Instructions](#-build-instructions)
- [Deployment](#-deployment)
- [API Overview](#-api-overview)
- [Authentication Flow](#-authentication-flow)
- [State Management](#-state-management)
- [Available Scripts](#-available-scripts)
- [Key Dependencies](#-key-dependencies)
- [Development Guide](#-development-guide)
- [Contribution Guidelines](#-contribution-guidelines)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Features

| Feature | Description |
|---------|-------------|
| **AI-Powered Mock Interviews** | Real-time adaptive interview simulation with LLM-based question generation, evaluation, and feedback |
| **Coding Challenges** | Extensive problem repository with multiple difficulty levels and domain categories |
| **System Design Challenges** | Advanced architecture and system design practice problems |
| **Live Interview Sessions** | WebSocket-based real-time interview experience with streaming responses |
| **Interview Reports** | Comprehensive performance analysis with topic coverage, evaluation metrics, and improvement areas |
| **Resume Parser** | Intelligent resume analysis to extract skills, experience, and technologies |
| **Leaderboard** | Competitive ranking system to track user progress and achievements |
| **User Profiles** | Detailed profile pages showcasing statistics, achievements, and submission history |
| **Multi-Auth Support** | Email/OTP, Google OAuth, and GitHub OAuth authentication |
| **Admin Dashboard** | Administrative tools for platform management and analytics |
| **Recruiter Portal** | Dedicated interface for recruiters to review candidate profiles and mock interview results |

### 🤖 AI & Interview System

- **Multi-Provider LLM Support**: Seamless integration with multiple AI providers (OpenAI, Anthropic, Google AI, Groq, DeepSeek)
- **Provider Fallback**: Automatic fallback to secondary AI provider if primary fails
- **Adaptive Difficulty**: Interview difficulty dynamically adjusts based on candidate performance
- **Topic Coverage Tracking**: Intelligent system to ensure comprehensive topic coverage during interviews
- **Real-time Evaluation**: Instant feedback on answers with detailed evaluation criteria
- **Voice Integration**: Text-to-speech support for interviewer messages (ready for TTS)
- **Session Persistence**: Interview state persisted with configurable session TTL

---

## 🛠 Tech Stack

### Frontend

```
React 19              → Modern reactive UI with hooks
Vite 7               → Lightning-fast build tool and dev server
React Router v6      → Client-side routing and navigation
Redux Toolkit        → State management and data flow
React-Redux          → Redux bindings for React
Tailwind CSS 4       → Utility-first CSS framework
Radix UI             → Unstyled, accessible UI component library
React Hook Form      → Performant, flexible form handling
Zod                  → TypeScript-first schema validation
Recharts             → Composable charting library
Lucide Icons         → Beautiful, consistent icon set
Sonner               → Toast notification system
```

### Backend

```
FastAPI              → Modern async Python web framework
Motor                → Async MongoDB driver
MongoDB              → NoSQL database
Pydantic             → Data validation using Python type annotations
AuthLib              → OAuth 2.0 & OpenID Connect client
LangChain            → LLM framework and provider abstraction
Redis                → Session and cache store
Python 3.9+          → Programming language
Uvicorn              → ASGI web server
```

### AI & ML Services

- **LLM Providers**: OpenAI GPT, Anthropic Claude, Google Gemini, Groq, DeepSeek
- **Provider Management**: Dynamic provider selection with fallback mechanism
- **Graph-Based State**: Interview state managed through LLM graph architecture
- **Resume Processing**: Intelligent resume parsing and extraction

---

## 🏗 Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Redux)               │
│  ┌──────────────────┬──────────────┬──────────────────┐   │
│  │   Challenges     │  Dashboard   │  AI Interviews   │   │
│  │   System Design  │  Leaderboard │  Live Sessions   │   │
│  │   Profiles       │  Analytics   │  Reports         │   │
│  └──────────────────┴──────────────┴──────────────────┘   │
│                         (Redux Store)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ User | Challenges | Interviews | Activity | System  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕️ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + Async)                 │
│  ┌──────────────────┬──────────────┬──────────────────┐   │
│  │   Auth Router    │  Resume      │ Interview        │   │
│  │   (JWT + OAuth)  │  Parser      │ Handler          │   │
│  │   Google/GitHub  │              │ (WebSocket)      │   │
│  └──────────────────┴──────────────┴──────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │              AI Interview Engine                   │   │
│  │  ┌──────────────┬──────────────┬────────────────┐ │   │
│  │  │ Graph-based  │ Multi-LLM    │ Evaluation    │ │   │
│  │  │ State Mgmt   │ Provider Mgmt│ System        │ │   │
│  │  │ Interview    │ with Fallback│              │ │   │
│  │  │ Nodes        │              │              │ │   │
│  │  └──────────────┴──────────────┴────────────────┘ │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         ↕️ Async Drivers & Connections
┌─────────────────────────────────────────────────────────────┐
│                   Data & Services Layer                     │
│  ┌──────────────┬──────────────┬──────────────────┐        │
│  │  MongoDB     │   Redis      │   AI Providers   │        │
│  │  (persistent)│  (sessions)  │   (LLMs)         │        │
│  └──────────────┴──────────────┴──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **User Authentication**: OAuth or email/OTP verification
2. **Session Creation**: User session established with JWT token
3. **Interview Initiation**: Payload with role, skills, job description
4. **State Graph Execution**: LLM generates questions through graph nodes
5. **Answer Evaluation**: LLM evaluates answers and generates feedback
6. **Report Generation**: Comprehensive report created upon completion
7. **State Persistence**: Interview state saved to Redis with MongoDB backup

---

## 📈 MNC Scalability & Good Practices

Designed with production-grade reliability, secure isolation, and decoupled components, InterLeet is architected to align with the core software engineering principles practiced at large-scale technology enterprises (FAANG/MNCs).

### 🚀 1. Architectural Scalability & System Design

To handle heavy, concurrent user actions without degradation, the backend employs three primary design patterns:
* **Decoupled Sandbox Isolation (Untrusted Code Execution):** Executing arbitrary user code poses critical security and performance risks. InterLeet isolates execution into ephemeral, resource-constrained **Docker Sandboxes** running as non-root users. The main API thread never compiles or runs code; instead, it delegates tasks, protecting the host system from memory exhaustion (OOM), infinite loops (timeout limits), and malicious system calls.
* **Asynchronous Task Processing:** Heavily CPU-bound tasks—such as AST parsing for mutation testing and sandbox execution—are processed asynchronously. This prevents thread starvation at the ASGI (Uvicorn) web server level, ensuring the API remains highly responsive for other active users.
* **Distributed Caching & Real-Time Persistence (Redis + MongoDB):** 
  * **Redis** acts as a ultra-low-latency state cache for real-time WebSocket interview sessions, OTP management, and rate-limiting.
  * **MongoDB (Motor Driver)** handles non-blocking async writes for persistent data (user statistics, submissions, interview reports), preventing database lockups under high write volume.

### 🛡️ 2. Production-Grade Good Practices & Code Quality

Large-scale engineering demands automated quality control. The project implements advanced testing and security safeguards:
* **Automated Challenge Validation Framework (Quality Gate):** Before any coding challenge is published, it must pass a strict three-layer validation pipeline:
  * **AST-Based Mutation Testing:** Programmatically synthesizes mutant solutions (e.g. replacing constants, removing statements, hardcoding outputs) to verify if the test suite successfully fails them (preventing weak test cases).
  * **Differential Testing:** Automatically tests user submissions against pre-verified reference solutions in parallel.
  * **Coverage Analysis:** Traces statement and branch coverage inside the sandboxes to ensure test inputs cover all logical execution paths.
* **Zero-Trust Security & Modern Auth:** 
  * **WebAuthn (Passkeys):** Integrated hardware-bound passwordless authentication (biometrics/FIDO2 keys), mitigating phishing and credential stuffing attacks.
  * **JWT Session Protection:** Stateless authentication tokens with strict signature validation, enabling seamless scaling across stateless load-balanced backend instances.
* **Decoupled UI State Management:** The frontend uses **Redux Toolkit** to strictly decouple API state from components. Page transitions are snappy, client-side caching prevents redundant network requests, and visual performance remains optimal.

---

## 📁 Project Structure

```
interleet/
├── frontend/                          # React + Vite frontend application
│   ├── public/                        # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                    # Radix UI components (buttons, dialogs, etc.)
│   │   │   ├── layout/                # AppShell, navigation components
│   │   │   ├── domain/                # Domain-specific components (ChallengeCard, etc.)
│   │   │   ├── auth/                  # Authentication components (AuthShell)
│   │   │   ├── brand/                 # Branding components (Logo)
│   │   │   ├── marketing/             # Landing page, marketing components
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── app/                   # App route pages
│   │   │   │   ├── dashboard.jsx      # User dashboard
│   │   │   │   ├── challenges/        # Challenges browse page
│   │   │   │   ├── editor.$id.jsx     # Code editor page
│   │   │   │   ├── interviews/        # Interview management pages
│   │   │   │   ├── system-design.jsx  # System design challenges
│   │   │   │   ├── leaderboard.jsx    # Leaderboard page
│   │   │   │   ├── profile/           # User profile pages
│   │   │   │   └── settings.jsx       # User settings
│   │   │   ├── index.jsx              # Landing page
│   │   │   ├── login.jsx              # Login page
│   │   │   ├── signup.jsx             # Signup page
│   │   │   ├── recruiter.jsx          # Recruiter dashboard
│   │   │   ├── admin.jsx              # Admin panel
│   │   │   ├── forgot.jsx             # Password reset
│   │   │   └── NotFound.jsx           # 404 page
│   │   ├── hooks/
│   │   │   └── use-mobile.jsx         # Mobile detection hook
│   │   ├── lib/
│   │   │   ├── mock.js                # Mock data
│   │   │   └── utils.js               # Utility functions
│   │   ├── redux/
│   │   │   ├── index.js               # Redux store configuration
│   │   │   ├── slices/
│   │   │   │   ├── userSlice.js       # User state (auth, profile)
│   │   │   │   ├── challengesSlice.js # Challenges state
│   │   │   │   ├── interviewsSlice.js # Interviews state
│   │   │   │   ├── leaderboardSlice.js# Leaderboard state
│   │   │   │   ├── activitySlice.js   # Activity feed state
│   │   │   │   ├── systemDesignSlice.js # System design state
│   │   │   │   └── candidatesSlice.js # Candidates state (recruiter)
│   │   │   └── hooks.js               # Typed Redux hooks
│   │   ├── routes/
│   │   │   └── AppRoutes.jsx          # Route configuration
│   │   ├── styles.css                 # Global Tailwind styles
│   │   ├── main.jsx                   # React entry point
│   │   └── index.html                 # HTML entry point
│   ├── package.json                   # Frontend dependencies and scripts
│   ├── vite.config.js                 # Vite configuration
│   ├── jsconfig.json                  # JavaScript config with path aliases
│   └── README.md                      # Frontend-specific documentation
│
├── backend/                           # FastAPI backend application
│   ├── .venv/                         # Python virtual environment
│   ├── main.py                        # FastAPI application entry point
│   ├── google.json                    # Google OAuth credentials
│   ├── app/
│   │   ├── __init__.py
│   │   ├── ai/                        # AI & Interview system
│   │   │   ├── graph/
│   │   │   │   ├── interview_graph.py # Core interview state graph
│   │   │   │   ├── state.py          # Interview state definition
│   │   │   │   └── nodes/            # Graph node implementations
│   │   │   │       ├── question_node.py      # Question generation
│   │   │   │       ├── evaluation_node.py    # Answer evaluation
│   │   │   │       ├── difficulty_node.py    # Difficulty adjustment
│   │   │   │       ├── completion_node.py    # Interview completion
│   │   │   │       └── context_node.py       # Context management
│   │   │   ├── prompts/              # LLM prompt templates
│   │   │   │   ├── system_prompt.py   # System instructions
│   │   │   │   ├── question_prompt.py # Question generation prompts
│   │   │   │   └── evaluation_prompt.py# Evaluation prompts
│   │   │   ├── providers/            # LLM provider implementations
│   │   │   │   ├── base.py           # Base provider interface
│   │   │   │   └── langchain_provider.py # LangChain providers
│   │   │   ├── services/             # Interview services
│   │   │   │   ├── ai_client.py      # Multi-provider AI client
│   │   │   │   ├── session_service.py # Session management
│   │   │   │   ├── report_service.py # Report generation
│   │   │   │   └── report_repository.py # Report persistence
│   │   │   ├── resume/               # Resume parsing
│   │   │   │   └── resume_parser.py  # Resume extraction logic
│   │   │   ├── schemas/              # Data schemas
│   │   │   │   └── interview.py      # Interview state schema
│   │   │   └── voice/                # Voice features (TTS ready)
│   │   │       └── text_to_speech.py # Text-to-speech implementation
│   │   ├── controllers/              # Business logic controllers
│   │   │   ├── user.py               # User controller (auth, profile)
│   │   │   └── Problems.py           # Problem controller
│   │   ├── core/                     # Core configuration & setup
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # Environment configuration
│   │   │   ├── db.py                 # Database connection
│   │   │   ├── oauth.py              # OAuth configuration
│   │   │   ├── ai_client.py          # AI client setup
│   │   │   └── security/             # Security utilities
│   │   ├── models/                   # Database models (MongoDB schemas)
│   │   │   ├── __init__.py
│   │   │   ├── users.py              # User model & auth schemas
│   │   │   ├── problems.py           # Problem/challenge model
│   │   │   ├── submissions.py        # User submissions
│   │   │   ├── test_cases.py         # Test case model
│   │   │   ├── interview_sessions.py # Interview session model
│   │   │   ├── interview_messages.py # Interview message history
│   │   │   ├── interview_reports.py  # Interview reports
│   │   │   ├── mock_tests.py         # Mock test configuration
│   │   │   ├── contests.py           # Contest/competition model
│   │   │   ├── contest_participants.py# Contest participants
│   │   │   ├── leaderboards.py       # Leaderboard model
│   │   │   ├── notifications.py      # Notification model
│   │   │   ├── discussions.py        # Discussion/forum model
│   │   │   ├── system_design_challenges.py # System design problems
│   │   │   ├── user_statistics.py    # User stats model
│   │   │   ├── problem_tags.py       # Problem tags/categories
│   │   │   └── execution_jobs.py     # Code execution jobs
│   │   ├── routers/                  # API route handlers
│   │   │   ├── interview.py          # Interview endpoints
│   │   │   ├── user.py               # User & auth endpoints
│   │   │   └── resume.py             # Resume parsing endpoints
│   │   ├── lib/                      # Utility libraries
│   │   │   ├── redis.py              # Redis client
│   │   │   └── generateOTP.py        # OTP generation
│   │   ├── middleware/               # Custom middleware
│   │   │   └── user.py               # User middleware (token verification)
│   │   └── utils/                    # Utility functions
│   │       ├── JWT.py                # JWT token handling
│   │       └── OTP.py                # OTP utility functions
│   └── requirements.txt              # Python dependencies (assumed)
│
└── README.md                          # Project documentation (this file)
```

### Key Directory Functions

| Directory | Purpose |
|-----------|---------|
| `frontend/components` | Reusable UI components built with Radix UI + Tailwind |
| `frontend/pages` | Top-level page components for routing |
| `frontend/redux/slices` | Redux state management per domain |
| `backend/app/ai` | Core interview engine and LLM integration |
| `backend/app/models` | MongoDB data models and schemas |
| `backend/app/routers` | FastAPI route handlers and endpoints |

---

## 📦 Prerequisites

### System Requirements

- **Node.js**: 18+ (with npm 9+)
- **Python**: 3.9+ (with pip)
- **MongoDB**: 4.4+ (local or cloud instance like MongoDB Atlas)
- **Redis**: 6+ (optional, for session caching)
- **Git**: For version control

### API Keys & Credentials Required

```
GOOGLE_CLIENT_ID                 # Google OAuth credentials
GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID                 # GitHub OAuth credentials
GITHUB_CLIENT_SECRET
OPENAI_API_KEY                   # AI Provider keys (one or more required)
ANTHROPIC_API_KEY
GOOGLE_API_KEY
GROQ_API_KEY
DEEPSEEK_API_KEY
MONGO_URI                        # MongoDB connection string
DB_NAME                          # MongoDB database name
SESSION_SECRET_KEY               # Session middleware secret
JWT_SECRET                       # JWT signing secret
JWT_ALGORITHM                    # JWT algorithm (e.g., HS256)
REDIS_HOST                       # Redis host (optional)
REDIS_PORT                       # Redis port (optional)
```

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/santusht06/interleet.git
cd interleet
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies (assuming requirements.txt exists)
pip install -r requirements.txt
# Or install manually if needed:
# pip install fastapi uvicorn motor pydantic authlib python-dotenv langchain
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install
```

---

## ⚙️ Environment Setup

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Environment
PROJECT_ENVIRONMENT=DEVELOPMENT

# Database
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=interleet

# Session & JWT
SESSION_SECRET_KEY=your_session_secret_key_here
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRES=7

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379

# OAuth - Google
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret

# OAuth - GitHub
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# AI Providers (setup at least one)
# Groq (recommended for testing - free tier available)
GROQ_API_KEY=your_groq_api_key
AI_PROVIDER=groq
AI_MODEL=llama-3.3-70b-versatile

# Alternative Providers
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_ai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# Fallback Provider
AI_FALLBACK_PROVIDER=openai
AI_FALLBACK_MODEL=gpt-3.5-turbo

# AI Configuration
AI_REQUEST_TIMEOUT_SECONDS=30
AI_MAX_RETRIES=2

# Interview Configuration
INTERVIEW_SESSION_TTL_SECONDS=21600  # 6 hours
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory (optional for development):

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=InterLeet
```

---

## 🏃 Running the Application

### Option 1: Run Backend Only

```bash
cd backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python main.py
```

Backend will start at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs` (Swagger UI)

### Option 2: Run Frontend Only

```bash
cd frontend
npm run dev
```

Frontend will start at: `http://localhost:5173`

### Option 3: Run Both (Recommended Development Setup)

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access the application at: `http://localhost:5173`

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/

# Check API documentation
open http://localhost:8000/docs

# Check frontend
open http://localhost:5173
```

---

## 🏗 Build Instructions

### Frontend Build

```bash
cd frontend

# Production build
npm run build

# Output: dist/ directory with optimized bundles
# Size: Typically 300-500KB gzipped

# Preview production build locally
npm run preview
```

### Backend Build

FastAPI doesn't require compilation. For production deployment:

```bash
cd backend

# Install production dependencies
pip install -r requirements.txt --only-binary :all:

# Run with production ASGI server (gunicorn + uvicorn)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 🚢 Deployment

### Frontend Deployment (Vercel/Netlify)

```bash
cd frontend

# Build
npm run build

# Deploy to Vercel (requires vercel CLI)
vercel deploy --prod

# Or deploy to Netlify
netlify deploy --prod --dir=dist
```

### Backend Deployment (Heroku/Railway/Render)

```bash
cd backend

# Deploy to Railway (recommended)
railway up

# Or Render
# Push to GitHub and connect repository to Render dashboard

# Or Heroku
heroku create interleet-api
git push heroku main
```

### Docker Deployment (Optional)

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔌 API Overview

### Interview Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/interview/start` | Start a new interview session |
| `POST` | `/interview/answer` | Submit answer to current question |
| `GET` | `/interview/{session_id}` | Retrieve interview session state |
| `GET` | `/interview/{session_id}/report` | Get interview report after completion |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/send-otp` | Send OTP to email |
| `POST` | `/auth/verify-otp` | Verify OTP and create session |
| `GET` | `/auth/google/login` | Initiate Google OAuth |
| `GET` | `/auth/google/callback` | Google OAuth callback |
| `GET` | `/auth/github/login` | Initiate GitHub OAuth |
| `GET` | `/auth/github/callback` | GitHub OAuth callback |
| `POST` | `/auth/logout` | Logout user |

### Resume Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/resume/parse` | Parse and extract resume data |

### Request/Response Examples

**Start Interview:**
```bash
curl -X POST http://localhost:8000/interview/start \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Senior Software Engineer",
    "interview_type": "technical",
    "difficulty": "medium",
    "skills": ["Python", "FastAPI", "React"],
    "technologies": ["MongoDB", "Redis", "AWS"],
    "jd": "Looking for experienced full-stack engineer...",
    "max_questions": 8
  }'
```

**Answer Question:**
```bash
curl -X POST http://localhost:8000/interview/answer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "answer": "I would design this using microservices...",
    "topic": "System Design"
  }'
```

---

## 🔐 Authentication Flow

### Diagram

```
User → Login Page
  ↓
Choose Auth Method:
  ├→ Email/OTP
  │  ├→ Enter Email
  │  ├→ Send OTP
  │  ├→ Verify OTP
  │  └→ Create JWT Session
  │
  ├→ Google OAuth
  │  ├→ Redirect to Google
  │  ├→ Google Callback
  │  ├→ Verify Token
  │  └→ Create Session
  │
  └→ GitHub OAuth
     ├→ Redirect to GitHub
     ├→ GitHub Callback
     ├→ Verify Token
     └→ Create Session
  ↓
User Profile Set (from parsed data)
  ↓
JWT Token in Cookie/localStorage
  ↓
Authenticated User Access
```

### Security Features

- **JWT Tokens**: Stateless authentication with expiration (default 7 days)
- **Session Middleware**: Secure session management with secrets
- **OAuth Integration**: Secure third-party authentication
- **OTP Verification**: Email-based one-time password for registration
- **Token Dependency**: Protected routes require valid JWT token

---

## 🎛 State Management

### Redux Store Structure

```javascript
store: {
  user: {
    isAuthenticated: boolean,
    profile: { name, email, avatar, statistics },
    token: string,
    settings: { theme, notifications, privacy }
  },
  challenges: {
    list: [],
    current: {},
    filters: { difficulty, topic, language },
    submissions: []
  },
  interviews: {
    sessions: [],
    current: { sessionId, state, messages },
    reports: [],
    loading: boolean
  },
  leaderboard: {
    users: [],
    currentUserRank: number,
    timeframe: 'week' | 'month' | 'all'
  },
  activity: {
    feed: [],
    notifications: []
  },
  systemDesign: {
    challenges: [],
    current: {},
    submissions: []
  },
  candidates: {
    list: [],
    selectedCandidate: {}
  }
}
```

### Redux Slices

Each domain has a dedicated Redux slice:

| Slice | Manages | Key Actions |
|-------|---------|-------------|
| `userSlice` | Auth state, profile, settings | LOGIN, LOGOUT, UPDATE_PROFILE |
| `challengesSlice` | Problems, submissions | FETCH_CHALLENGES, SUBMIT_CODE |
| `interviewsSlice` | Interview sessions, reports | START_INTERVIEW, ANSWER_QUESTION |
| `leaderboardSlice` | Rankings, scores | FETCH_LEADERBOARD, UPDATE_RANK |
| `activitySlice` | Feed, notifications | ADD_ACTIVITY, FETCH_NOTIFICATIONS |
| `systemDesignSlice` | System design problems | FETCH_CHALLENGES, SUBMIT_SOLUTION |
| `candidatesSlice` | Candidate profiles (recruiter) | FETCH_CANDIDATES, VIEW_PROFILE |

### Data Flow

```
User Action (UI Event)
  ↓
Redux Action Dispatcher
  ↓
Reducer Updates State
  ↓
Component Re-renders
  ↓
Updated UI
```

---

## 📜 Available Scripts

### Frontend Scripts

```bash
npm run dev         # Start development server (Vite)
npm run build       # Build for production
npm run preview     # Preview production build locally
npm run lint        # Run ESLint on source files
```

### Backend Scripts

```bash
# Start development server
python main.py

# With reload on file changes
python main.py --reload

# Production with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Run tests (when available)
pytest tests/ -v
```

---

## 📚 Key Dependencies Explained

### Frontend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **React** | 19 | Core UI library |
| **React Router DOM** | 6.28 | Client-side routing |
| **Redux Toolkit** | 2.12 | State management |
| **React Redux** | 9.3 | Redux-React bindings |
| **Tailwind CSS** | 4.2 | Utility CSS framework |
| **Radix UI** | Latest | Accessible UI primitives |
| **React Hook Form** | 7.71 | Form state management |
| **Zod** | 3.24 | Schema validation |
| **Recharts** | 2.15 | Chart components |
| **Lucide React** | 0.575 | Icon library |
| **Sonner** | 2.0 | Toast notifications |
| **Vite** | 7.0 | Build tool |

### Backend Dependencies

```
fastapi               # Web framework
uvicorn              # ASGI server
motor                # Async MongoDB driver
pydantic             # Data validation
authlib              # OAuth 2.0 & OpenID
langchain            # LLM framework
python-dotenv        # Environment variables
requests             # HTTP client
```

### Why These Choices?

| Technology | Reason |
|------------|--------|
| **React + Vite** | Fast dev experience, modern tooling, industry standard |
| **Redux** | Predictable state, easier debugging, time-travel capability |
| **Tailwind + Radix** | Consistent design, accessible components, rapid development |
| **FastAPI** | High performance async framework, auto-generated API docs |
| **Motor** | Seamless async MongoDB integration for non-blocking I/O |
| **LangChain** | Unified LLM interface, easy provider switching |

---

## 🛠 Development Guide

### Adding a New Feature

1. **Backend**:
   - Add data model in `backend/app/models/`
   - Create router in `backend/app/routers/`
   - Add business logic in `backend/app/controllers/`
   - Test endpoints via `/docs`

2. **Frontend**:
   - Create Redux slice in `frontend/src/redux/slices/`
   - Create page component in `frontend/src/pages/app/`
   - Add UI components using Radix UI + Tailwind
   - Add route in `frontend/src/routes/AppRoutes.jsx`

### Adding a New API Endpoint

**Backend Example:**
```python
# backend/app/routers/new_router.py
from fastapi import APIRouter

router = APIRouter(prefix="/new-feature", tags=["New Feature"])

@router.post("/action")
async def perform_action(payload: dict):
    # Implementation
    return {"status": "success"}

# Add to main.py
app.include_router(new_router)
```

**Frontend Example:**
```javascript
// frontend/src/redux/slices/newFeatureSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const performAction = createAsyncThunk(
  'newFeature/performAction',
  async (payload) => {
    const response = await fetch('/api/new-feature/action', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    return response.json();
  }
);

const newFeatureSlice = createSlice({
  name: 'newFeature',
  initialState: { data: null, loading: false },
  extraReducers: (builder) => {
    builder.addCase(performAction.fulfilled, (state, action) => {
      state.data = action.payload;
    });
  }
});

export default newFeatureSlice.reducer;
```

### Running Tests

```bash
# Backend tests (when available)
cd backend
pytest tests/ -v --cov

# Frontend tests (setup needed)
cd frontend
npm run test
```

### Code Style & Linting

```bash
# Frontend linting
cd frontend
npm run lint
npm run lint -- --fix  # Auto-fix issues

# Backend linting (setup needed)
cd backend
black .
flake8 app/
```

---

## 🤝 Contribution Guidelines

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **Frontend**: Follow React best practices, use functional components with hooks
- **Backend**: Follow PEP 8 Python conventions, use type hints
- **Commits**: Use clear, descriptive commit messages
- **Testing**: Add tests for new features
- **Documentation**: Update README and code comments

### Issue Reporting

Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if UI-related
- Environment details (OS, Node/Python version)

---

## 🗺 Roadmap

### Phase 1: Core Platform ✅
- [x] User authentication (Email/OTP, OAuth)
- [x] Coding challenges
- [x] AI mock interviews
- [x] Basic leaderboard

### Phase 2: Advanced Features (In Progress)
- [ ] System design interviews with whiteboarding
- [ ] Video interview recording and playback
- [ ] Real-time collaborative coding
- [ ] Advanced analytics dashboard
- [ ] Recruiter CRM features

### Phase 3: Enterprise Features (Planned)
- [ ] Company accounts and team management
- [ ] Custom question banks
- [ ] Integration with ATS systems
- [ ] API access for hiring platforms
- [ ] Advanced reporting and compliance

### Phase 4: AI Enhancements (Future)
- [ ] Voice-based interviews with speech recognition
- [ ] Computer vision for on-screen verification
- [ ] Personalized learning paths
- [ ] Interview coaching with ML feedback
- [ ] Behavioral interview simulations

---

## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

```
MIT License

Copyright (c) 2024 InterLeet Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙋 Support & Community

### Getting Help

- **Documentation**: Check this README and code comments
- **Issues**: File GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: contact@interleet.dev

### Connected Resources

| Resource | Link |
|----------|------|
| **API Docs** | `http://localhost:8000/docs` |
| **GitHub** | [santusht06/interleet](https://github.com/santusht06/interleet) |
| **Issue Tracker** | GitHub Issues |
| **Demo** | [interleet.dev](https://interleet.dev) |

---

## 🙏 Acknowledgments

- **React** and **FastAPI** communities for excellent frameworks
- **Radix UI** for accessible component primitives
- **LangChain** for LLM abstraction
- All **contributors** and **users** who make this project possible

---

## 📊 Project Statistics

- **Lines of Code**: ~15,000+
- **Frontend Components**: 50+
- **API Endpoints**: 15+
- **Database Collections**: 13
- **Supported AI Providers**: 5
- **Languages Supported**: Python, JavaScript, TypeScript

---

## 🔄 Version History

| Version | Date | Highlights |
|---------|------|-----------|
| v0.1.0 | 2024 | Initial release with core features |
| v0.2.0 (In Dev) | 2024 Q2 | System design, advanced analytics |
| v0.3.0 (Planned) | 2024 Q3 | Video interviews, recruiter CRM |

---

**Last Updated**: June 2024  
**Status**: Active Development  
**Maintained By**: InterLeet Team

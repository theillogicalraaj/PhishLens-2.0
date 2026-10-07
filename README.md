# PhishLens 2.0

## Security Awareness Simulation & Behavioral Risk Intelligence Platform

PhishLens is a defensive cybersecurity platform for running **authorized, safe phishing-awareness simulations** and turning simulation behavior into actionable security-awareness intelligence.

The platform is intentionally designed around a strict safety boundary:

> **No credential harvesting. No password collection. No real phishing delivery in the default application.**

Instead, it measures events such as delivered, opened, clicked, reported, and training-completed, then uses analytics and an interpretable machine-learning baseline to estimate campaign risk and identify where awareness interventions may be useful.

---

## Why this is portfolio-grade

PhishLens is designed as a real full-stack security product rather than a simple phishing-email generator.

### Product capabilities

- Full-stack React + TypeScript frontend
- FastAPI backend
- JWT authentication
- scrypt password hashing using Python's standard cryptographic primitives
- Analyst/admin roles
- Campaign management
- Synthetic recipient management
- CSV bulk recipient import
- Simulation event tracking
- Campaign lifecycle management
- Dashboard analytics
- Click/report/completion metrics
- Department-aware recipient metadata
- Explainable behavioral risk scoring
- Synthetic-data Logistic Regression baseline
- PDF campaign reports
- Audit logging
- Hashed IP storage for simulation events
- Lightweight API rate limiting
- SQLite for zero-friction development
- PostgreSQL via Docker Compose
- Dockerized deployment
- GitHub Actions CI scaffolding
- Threat model and security documentation

---

# Core Problem

Security-awareness teams need a controlled way to answer questions such as:

- Which simulation cohorts are most vulnerable?
- How often do users report suspicious simulations?
- Which groups repeatedly click simulations?
- Is training completion improving after an intervention?
- Which campaigns create the highest measured behavioral risk?

Traditional projects often stop at "send a phishing email and count clicks".

PhishLens goes further:

```text
Simulation
    ↓
Behavior Events
    ↓
Feature Engineering
    ↓
Analytics
    ↓
Risk Model
    ↓
Analyst Interpretation
    ↓
Training Intervention
    ↓
Measure Again
```

---

# Safety Boundary

PhishLens is an **authorized security-awareness simulation platform**.

The default product deliberately avoids dangerous capabilities:

- No password fields in the simulation flow
- No credential capture
- No credential storage
- No credential replay
- No authentication bypass
- No real phishing mail delivery
- No malicious attachment generation
- No account impersonation workflow

Simulation events are recorded by the application itself.

For a real organizational deployment, campaign scope, notification policy, legal approval, privacy requirements, and mail infrastructure must be controlled by the organization running the exercise.

---

# Architecture

```text
                         ┌──────────────────────────┐
                         │      React Frontend      │
                         │   TypeScript + Vite      │
                         └────────────┬─────────────┘
                                      │
                                  REST + JWT
                                      │
                         ┌────────────▼─────────────┐
                         │     FastAPI Backend      │
                         ├──────────────────────────┤
                         │ Authentication           │
                         │ Campaign Engine          │
                         │ Recipient Management     │
                         │ Event Tracking           │
                         │ Analytics Engine         │
                         │ Risk Model               │
                         │ PDF Reporting            │
                         │ Audit Logging            │
                         └────────────┬─────────────┘
                                      │
                  ┌───────────────────┼───────────────────┐
                  │                   │                   │
            ┌─────▼─────┐       ┌────▼─────┐       ┌────▼──────┐
            │ SQLite /  │       │  Report  │       │   Audit   │
            │ PostgreSQL│       │   PDF    │       │   Events   │
            └───────────┘       └──────────┘       └───────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │ Behavioral Risk Model    │
                         │ Synthetic Logistic       │
                         │ Regression Baseline     │
                         └──────────────────────────┘
```

---

# Technology Stack

## Frontend

- React
- TypeScript
- Vite
- React Router
- Responsive CSS UI

## Backend

- Python
- FastAPI
- SQLAlchemy
- JWT
- scrypt
- Pydantic

## Data Science

- NumPy
- scikit-learn
- Logistic Regression
- Feature engineering
- Behavioral risk scoring

## Database

Local:

```text
SQLite
```

Docker / production-oriented:

```text
PostgreSQL
```

## DevOps

- Docker
- Docker Compose
- GitHub Actions
- Automated backend tests

---

# Windows Quick Start — Double Click

You do **not** need VS Code.

You do **not** need to manually activate the Python virtual environment.

You only need:

- Python 3.11+
- Node.js LTS

After extracting the project, the root folder should look like:

```text
phishlens-2.0/
│
├── START-PHISHLENS.cmd
├── START-HERE.txt
├── README.md
├── SECURITY.md
├── backend/
├── frontend/
├── docs/
└── sample-data/
```

### Launch

Double-click:

```text
START-PHISHLENS.cmd
```

The launcher will:

1. Check Python.
2. Check Node.js.
3. Create `backend\.venv` if required.
4. Install backend dependencies.
5. Install frontend dependencies if required.
6. Open the backend PowerShell window.
7. Open the frontend PowerShell window.
8. Start the application.

Open:

```text
http://localhost:5173
```

If Vite selects another port such as `5174`, use the URL shown in the frontend PowerShell window.

---

# First Demo

After launching:

### 1. Create analyst account

Open the registration screen and create an analyst account.

### 2. Create a campaign

Use:

```text
Name:
Q4 Password Reset Drill

Scenario:
Password Reset
```

The application includes a safe training-oriented message template.

### 3. Add the demo recipient

The new campaign page automatically adds a synthetic test recipient.

### 4. Simulate behavior

Open the campaign and use:

```text
Simulate click
Simulate report
Complete training
```

These actions create internal training events.

### 5. View the analytics

The campaign dashboard will update:

```text
Recipients
Clicks
Reports
Completed training
Risk score
```

### 6. Generate the report

Click:

```text
Generate PDF
```

---

# Bulk Recipient Import

Campaigns support CSV import.

Required columns:

```text
display_name,email,department
```

Example:

```csv
display_name,email,department
Alex Morgan,alex@example.test,Engineering
Maya Singh,maya@example.test,Finance
Samir Khan,samir@example.test,HR
Priya Nair,priya@example.test,Sales
Jordan Lee,jordan@example.test,Operations
```

The included demo file is:

```text
sample-data/demo_recipients.csv
```

The API limits a single import to 500 valid rows and 1 MB.

---

# Behavioral Analytics

PhishLens records events such as:

```text
Delivered
Opened
Clicked
Reported
Completed Training
```

From these events it calculates behavioral rates.

Example:

```text
Click Rate  = Unique Clickers / Recipients
Report Rate = Unique Reporters / Recipients
```

The dashboard exposes these metrics without storing passwords or authentication data.

---

# Machine Learning Layer

PhishLens includes an intentionally transparent ML baseline.

The current release uses a **Logistic Regression classifier trained on synthetic educational data**.

The input features include:

```text
Open rate
Click rate
Report rate
Repeat-click rate
Training completion rate
```

The model produces:

```text
Risk score
Severity
Explanation
```

Example:

```text
Risk score: 68.4 / 100
Severity: HIGH

Reasons:
- High simulation click rate
- Low reporting rate
- Training completion is low
```

### Important ML limitation

The included model is a portfolio/demo baseline trained on synthetic data.

It must **not** be presented as a validated enterprise behavioral prediction model.

A real organizational deployment should train, calibrate, validate, and monitor models against approved organizational data with privacy and fairness review.

---

# Risk Severity

The score is mapped to:

```text
0–34   LOW
35–59  MEDIUM
60–79  HIGH
80–100 CRITICAL
```

The score is intended for **prioritization**, not punishment or automatic employee decisions.

---

# Analyst Workflow

```text
1. Create campaign
       ↓
2. Add/import authorized recipients
       ↓
3. Run the approved simulation
       ↓
4. Record behavior events
       ↓
5. Inspect campaign analytics
       ↓
6. Review risk score
       ↓
7. Identify awareness intervention
       ↓
8. Complete training
       ↓
9. Re-measure behavior
       ↓
10. Generate report
```

---

# Dashboard

The command center provides:

- Campaign count
- Recipient count
- Click count
- Report count
- Training completion count
- Click rate
- Report rate
- Event distribution
- Simulation safety boundary

---

# Campaign Management

A campaign contains:

```text
Campaign name
Scenario
Subject
Safe simulation body
Status
Recipients
Events
Risk analytics
```

Campaign states:

```text
DRAFT
ACTIVE
COMPLETED
ARCHIVED
```

---

# PDF Reporting

Campaign reports contain:

```text
Campaign identity
Scenario
Status
Recipient count
Open count
Click count
Report count
Training completion count
Risk score
Risk severity
Model information
Safety boundary
```

Reports are designed for analyst documentation and portfolio demonstrations.

---

# Authentication

Authentication uses:

```text
JWT
```

Passwords are hashed using:

```text
scrypt
```

No plain-text passwords are stored.

---

# Audit Logging

Important actions are recorded for traceability, including:

```text
User registration
User login
Campaign creation
Campaign status changes
```

Administrative audit access is restricted through the admin role.

---

# API Rate Limiting

The development API includes a lightweight in-memory rate limiter.

Default:

```text
120 requests / IP / 60 seconds
```

This is intentionally simple for local development.

### Production recommendation

Use a shared rate-limiting layer such as a reverse proxy or API gateway with Redis/shared state for multi-instance deployments.

---

# Privacy-Oriented Event Logging

Simulation event records store a SHA-256 hash of the source IP rather than the raw IP address.

User agents may be retained for simulation diagnostics.

Production organizations should define:

- Data retention periods
- Access policies
- Employee transparency requirements
- Privacy/legal review
- Data deletion workflows

---

# API Surface

## Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

## Campaigns

```text
POST /api/v1/campaigns
GET  /api/v1/campaigns
GET  /api/v1/campaigns/{id}
PATCH /api/v1/campaigns/{id}/case
```

## Recipients

```text
POST /api/v1/campaigns/{id}/recipients
POST /api/v1/campaigns/{id}/recipients/import
```

## Simulation Events

```text
POST /api/v1/campaigns/{id}/simulate
```

Supported event types:

```text
delivered
opened
clicked
reported
completed
```

## Reports

```text
GET /api/v1/campaigns/{id}/report
```

## Dashboard

```text
GET /api/v1/dashboard
```

## Administration

```text
GET /api/v1/admin/audit
```

---

# Manual Windows PowerShell Setup

If you do not want to use the double-click launcher:

## Backend

```powershell
cd C:\path\to\phishlens-2.0\backend

py -m venv .venv

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Frontend

Open a second PowerShell:

```powershell
cd C:\path\to\phishlens-2.0\frontend

npm.cmd install
npm.cmd run dev
```

Frontend:

```text
http://localhost:5173
```

Using `npm.cmd` avoids PowerShell's common `npm.ps1` execution-policy problem.

---

# Docker

Run:

```powershell
cd C:\path\to\phishlens-2.0

docker compose up --build
```

The Docker deployment provides:

```text
PostgreSQL
FastAPI
Nginx-served frontend
```

Frontend:

```text
http://localhost:8080
```

Backend:

```text
http://localhost:8000
```

---

# Configuration

Copy:

```text
backend\.env.example
```

to:

```text
backend\.env
```

Example:

```env
DATABASE_URL=sqlite:///./phishlens.db
JWT_SECRET=replace-with-a-long-random-secret
BOOTSTRAP_ADMIN_EMAIL=admin@example.com
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:5175,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5175
```

For production, use a real secret-management system and a cryptographically random JWT secret.

---

# Testing

Run backend tests:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

The test suite covers:

- Behavioral risk scoring
- Low/high behavior model behavior
- API health
- Registration
- Login
- Authenticated user lookup

---

# Repository Structure

```text
phishlens-2.0/
│
├── START-PHISHLENS.cmd
├── START-HERE.txt
├── README.md
├── SECURITY.md
├── .gitignore
├── compose.yaml
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   ├── deps.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── main.tsx
│   │   └── styles.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT_PLAN.md
│   └── THREAT_MODEL.md
│
├── sample-data/
│   └── demo_recipients.csv
│
└── .github/
    └── workflows/
```

---

# CI/CD

GitHub Actions scaffolding is included for repeatable checks.

Recommended pipeline stages:

```text
Install dependencies
       ↓
Backend tests
       ↓
Frontend build
       ↓
Docker build
       ↓
Security / dependency checks
```

---

# Scalability Roadmap

A production-scale version can evolve toward:

```text
React
  ↓
API Gateway
  ↓
FastAPI
  ↓
Message Queue
  ↓
Background Analytics Workers
  ↓
PostgreSQL
  ↓
Object / Report Storage
  ↓
SIEM / Awareness Analytics
```

---

# Research Extensions

Potential future work:

1. Calibrated ML models trained on approved organizational data.
2. Department/cohort benchmarking.
3. Time-to-report analytics.
4. Repeat-click behavioral modeling.
5. Training intervention effectiveness measurement.
6. Enterprise SSO and fine-grained RBAC.
7. Distributed background workers.
8. Redis-backed rate limiting.
9. SIEM integration.
10. Privacy-preserving analytics.
11. Model drift monitoring.
12. Fairness and bias evaluation.
13. Multi-tenant architecture.
14. Retention and deletion controls.
15. Security-awareness recommendation engine.

---

# What Makes This Different From a Basic Phishing Project?

A basic implementation is:

```text
Create email
    ↓
Track click
    ↓
Show result
```

PhishLens is:

```text
Campaign Design
      ↓
Authorized Cohort
      ↓
Safe Simulation
      ↓
Behavior Event Collection
      ↓
Feature Engineering
      ↓
ML Risk Estimation
      ↓
Explainable Findings
      ↓
Training Intervention
      ↓
Re-measurement
      ↓
Executive / Analyst Report
```

This demonstrates:

```text
Cybersecurity
        +
Data Science
        +
Machine Learning
        +
Full-Stack Development
        +
Database Engineering
        +
Security Engineering
        +
DevOps
```

---

# Resume Version

**PhishLens — Security Awareness Simulation & Behavioral Risk Intelligence Platform**

Developed a full-stack defensive cybersecurity platform using React, TypeScript, FastAPI and PostgreSQL/SQLite to run authorized phishing-awareness simulations without collecting credentials. Implemented campaign management, synthetic recipient cohorts, behavioral event analytics, CSV import, explainable risk scoring, a synthetic-data Logistic Regression baseline, audit logging, PDF reporting, JWT authentication, scrypt password hashing, Docker deployment and CI scaffolding.

## Skills Demonstrated

```text
Python
FastAPI
React
TypeScript
REST APIs
SQLAlchemy
SQLite
PostgreSQL
JWT
scrypt
Cybersecurity
Security Awareness
Behavioral Analytics
Data Science
Machine Learning
Feature Engineering
Logistic Regression
Docker
Docker Compose
GitHub Actions
CI/CD
API Security
Privacy-Aware Analytics
```

---

# Portfolio Demo Flow

Use this sequence when presenting the project:

```text
1. Launch PhishLens
2. Register analyst
3. Open Command Center
4. Create campaign
5. Add/import recipients
6. Show safe simulation preview
7. Simulate click
8. Simulate report
9. Complete training
10. Refresh analytics
11. Explain risk score
12. Show ML model label
13. Generate PDF
14. Explain privacy/safety boundary
15. Show Docker architecture
```

---

# Project Goals

PhishLens demonstrates practical capabilities across:

```text
Cybersecurity
Digital Security Awareness
Data Science
Machine Learning
Backend Engineering
Frontend Engineering
Database Design
API Security
Privacy Engineering
DevOps
Reporting
```

---

# Development Philosophy

## 1. Measure behavior, not credentials

Awareness testing should focus on safe behavioral signals rather than collecting secrets.

## 2. Make the model explainable

Risk scores should be connected to observable behavioral indicators.

## 3. Keep the experiment authorized

Real-world awareness testing requires explicit organizational authorization and appropriate privacy controls.

## 4. Improve users rather than punish users

Simulation data should be used to identify training opportunities and measure improvement.

---

# Disclaimer

PhishLens is a defensive cybersecurity and security-awareness project intended for authorized educational, research, and organizational use.

Do not use the platform to target people or systems without appropriate authorization.

The default implementation intentionally does not collect credentials or send real phishing emails.

The included ML model is a synthetic-data demonstration and is not a validated employee-risk predictor.

---

# Author

**Rajeev Ranjan**

Cybersecurity | Full-Stack Development | Data Science | Machine Learning

GitHub:

```text
https://github.com/theillogicalraaj
```

---

# Project Status

```text
Version: 2.0
Status: Active Development
Focus: Defensive Cybersecurity + Data Science + Machine Learning
Architecture: Full Stack
Deployment: Local + Docker
```

---

## PhishLens 2.0

**Simulate safely. Measure behavior. Improve security awareness.**

---

# Windows ML Installation Troubleshooting

PhishLens uses scikit-learn for its behavioral-risk baseline. The Windows launcher installs the ML dependencies from pre-built binary wheels so Visual Studio, `cl.exe`, `gcc`, and other C/C++ compilers are not required for a normal setup.

If a previous installation attempted to build scikit-learn from source and failed with messages mentioning `cl`, `gcc`, `clang`, or `WinError 2`, close the launcher windows and delete the project virtual environment:

```powershell
Remove-Item -Recurse -Force .\backend\.venv
```

Then double-click:

```text
START-PHISHLENS.cmd
```

The launcher will create a fresh environment and install the pinned Windows-compatible binary releases.

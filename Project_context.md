# Project Context — Vidyapath AI Academic Planner

## Project Type
Agentic AI based Academic Planning System

## Architecture

Frontend (React)  ← next phase
Backend (Node.js + Express)
AI Layer (Python + FastAPI)
Database (MongoDB)

---

## AI Layer Status

Planner Agent ✅
Replanning Agent ✅
Monitoring Agent v1 ✅
Monitoring Agent v2 (weighted reliability) ✅
Confidence Score Modeling ✅
Risk Level Prediction ✅
Explainable Planning ✅
Loop Guard / Stability Fix ✅

Priority formula:

priority =
urgency *
difficulty *
performanceBoost *
(1 + (1 - reliability))

Confidence = avg reliability of tasks
Risk = based on confidence

LOW >= 0.75
MEDIUM >= 0.5
HIGH < 0.5

---

## FastAPI Integration

POST /generate-plan/{user_id}
GET /studyplan/{user_id}
GET /studyplan/latest/{user_id}
GET /progress/{user_id}
GET /subjects/{user_id}
GET /tasks/{user_id}
POST /activitylog

FastAPI connected to Node backend
Backend connected to MongoDB
Planner connected to monitoring logs

---

## Monitoring System

activitylogs collection

action:
completed
missed

Used for:

performance boost
reliability
confidence
risk

---

## Database Collections

users
subjects
tasks
studyplans
activitylogs

---

## Backend Status

Planner working
Monitoring working
Adaptive planning working
Confidence working
Risk prediction working
APIs working
FastAPI working
Mongo working

Backend = COMPLETE

---

## Next Phase

Frontend (React)

Dashboard
Study Plan UI
Progress UI
Risk Indicator
Confidence Display
# Vidyapath Project Context

## System Overview
Vidyapath is an AI-based academic planning system that generates adaptive study schedules using user tasks, subjects, deadlines, and behavioral history.

Architecture:

Frontend (to be built)
↓
Node.js Backend (API Layer)
↓
FastAPI AI Layer (Planning Engine)
↓
MongoDB (Data Layer)

---

# Database Collections

users
subjects
tasks
activitylogs
studyplans

---

# Backend (Node.js)

## Core APIs Implemented
Subjects API
- Create subject
- Fetch subjects by user

Tasks API
- Create task
- Update task status
- Fetch tasks

Activity Logs API
- Log task actions (completed / missed)

Study Plan API
- Save study plan
- Fetch study plan

AI Trigger API
POST /api/ai/generate-plan/:userId

This endpoint calls the AI layer to generate a plan.

---

# AI Layer (FastAPI)

## Agents Implemented

### Planning Agent
Generates study schedules based on:
- task deadlines
- subject difficulty
- user daily study hours

### Monitoring Agent
Reads activitylogs to track:
- completed tasks
- missed tasks

### Replanning Agent
If tasks are missed, the system redistributes workload.

### Explainability Layer
Each task allocation includes explanation:
- difficulty
- urgency
- performance boost
- reliability score
- final priority

---

# Adaptive Learning (NEW)

The planner now learns from user behavior.

### Reliability Score
Computed from activity logs:

reliability = completed / (completed + missed)

Range:
0 → user always misses
0.5 → neutral
1 → always completes

### Adaptive Priority

priority = urgency × difficulty × performanceBoost × (1 + (1 − reliability))

Meaning:
Tasks frequently missed are prioritized earlier.

---

# Confidence Prediction (NEW)

The planner estimates the probability that a user will complete the daily plan.

Daily confidence:

confidence = average reliability of tasks scheduled that day

Example output:

{
 "2026-03-06": {
   "tasks": [...],
   "confidence": 0.72
 }
}

Confidence meaning:

0.90 → Very likely to complete  
0.70 → Moderate probability  
0.50 → Risky plan  
0.30 → Very unlikely  

Confidence is stored in MongoDB inside `studyplans`.

---

# Current Development Stage

Completed:

- Database schema
- Backend APIs
- AI planning engine
- Monitoring agent
- Replanning agent
- Explainability layer
- Backend ↔ AI integration
- Adaptive reliability learning
- Confidence prediction

---

# Next Phase

Remaining backend work:

- Risk detection for failing study plans
- Confidence analytics API
- System evaluation metrics

After backend completion:
Frontend development will begin.
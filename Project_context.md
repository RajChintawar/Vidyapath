# Vidyapath – AI-Based Smart Academic Planner

## Project Overview

Vidyapath is an AI-driven academic planning system that generates, adapts, and stores personalized study schedules for students based on:

- Study hours per day
- Subject difficulty
- Assignment deadlines
- Examination dates
- Task completion behavior (activity logs)

The system follows an Agentic AI architecture with planning, monitoring, and replanning components.

---

## Tech Stack

### Backend
- Node.js (Express)
- MongoDB (NoSQL)
- Mongoose

### AI Layer
- Python
- PyMongo
- Modular agent structure:
  - planning
  - monitoring
  - replanning
  - explaining
  - common (config, db, utils)

---

## Database: academic_planner

Collections:

- users
- subjects
- tasks
- activitylogs
- studyplans

### Data Relationships

User  
└── Subject  
  └── Task  
    └── ActivityLog  

StudyPlan:
- Generated per user per date
- Stores allocated tasks and hours

---

## Current Implementation Status

### Completed

- MongoDB connection fixed (case-sensitive collection issue resolved)
- Users visible from Python and Node
- Planning Agent v1 implemented
- Study plan generation based on:
  - pending tasks
  - estimated hours
  - user studyHoursPerDay
- Study plan persistence implemented
- Duplicate study plans prevented (update instead of insert)

---

## Planning Agent v1 Logic

1. Fetch user
2. Fetch pending tasks sorted by deadline
3. Allocate daily study hours
4. Generate date-wise schedule
5. Save into studyplans collection
   - Update if plan already exists for that user and date
   - Insert otherwise

---

## Next Development Milestones

### Short-Term
- Add priority weighting (deadline proximity + difficulty)
- Prevent allocation beyond exam date
- Improve scheduling distribution logic


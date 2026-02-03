# Agentic AI–Based Smart Academic Planner

This project aims to build an intelligent, agentic AI system that autonomously plans, monitors, replans, and explains academic study schedules for students.

The system is designed as a full-stack web application with a modular architecture separating frontend, backend, AI reasoning, and data persistence layers.

---

##  Project Objective

- Automate academic study planning
- Adapt schedules dynamically based on student progress
- Monitor missed tasks and deviations
- Provide explainable AI-based decisions
- Reduce academic stress and improve time management

---

##  System Architecture Overview

The system follows a layered architecture:

- **Frontend (React)** – User interaction and visualization
- **Backend (Node.js / Express)** – API orchestration and data management
- **AI Layer (Python)** – Agentic decision-making
- **Database (MongoDB)** – Persistent academic data storage

---

##  Repository Structure
│
├── frontend/ # React UI
├── backend/ # Node.js backend APIs
├── ai-layer/ # Python-based AI agents
├── dataset/ # Synthetic and sample data
├── docs/ # Diagrams and documentation
└── README.md

##  Project Workflow

1. User enters subjects, syllabus, deadlines, and study hours
2. Backend stores data in MongoDB
3. Planning Agent generates a study plan
4. User updates task status (completed/missed)
5. Monitoring Agent detects deviations
6. Replanning Agent updates schedules if required
7. Explanation Agent explains changes to the user

---

##  Technology Stack

- **Language:** Python, JavaScript
- **Frontend:** React.js
- **Backend:** Node.js + Express
- **Database:** MongoDB
- **AI Layer:** Python + LangChain / CrewAI
- **LLM:** OpenAI / Gemini
- **Visualization:** Calendar-based UI

---

##  Environment Setup

- `.env` files are excluded from version control
- Use `.env.example` to configure environment variables
- Run `npm install` inside `backend/` and `frontend/`

---

##  Collaboration Guidelines

- Follow modular folder structure
- Do not commit `node_modules/` or `.env`
- Push feature-specific changes with clear commit messages
- Coordinate AI logic changes with backend APIs

---

##  Current Development Phase

**Phase 1:**  
✔ System architecture  
✔ Database models  
✔ Backend setup  

Next: Task APIs → AI Planning Agent → Frontend integration
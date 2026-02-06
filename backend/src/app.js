const express = require("express");
require("dotenv").config();
const mongoose = require("mongoose");
const cors = require("cors");


// 1. Initialize app FIRST
const app = express();

// 2. Middleware
app.use(cors());
app.use(express.json());

// 3. Routes (AFTER app is defined)
const taskRoutes = require("./routes/taskRoutes");
app.use("/api/tasks", taskRoutes);

//4. Study Plan Routes
const studyPlanRoutes = require("./routes/planRoutes");
app.use("/api/study-plans", studyPlanRoutes);

// 4. Test route
app.get("/", (req, res) => {
  res.send("AI-Based Academic Planner Backend Running");
});

// 5. DB connection
console.log("MONGO_URI:", process.env.MONGO_URI);

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.error(err));

// 6. Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

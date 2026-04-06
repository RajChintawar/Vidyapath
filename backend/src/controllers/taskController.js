const Task = require("../models/Task");
const Subject = require("../models/Subject");
const ActivityLog = require("../models/ActivityLog");

// 1. Create a new task
exports.createTask = async (req, res) => {
  try {
    const { subjectId, topic, deadline, estimatedHours } = req.body;

    const subjectExists = await Subject.findById(subjectId);
    if (!subjectExists) {
      return res.status(404).json({ message: "Subject not found" });
    }

    const task = await Task.create({
      subjectId,
      topic,
      deadline,
      estimatedHours
    });

    res.status(201).json(task);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// 2. Get all tasks for a user
exports.getTasksByUser = async (req, res) => {
  try {
    const { userId } = req.params;

    const tasks = await Task.find()
      .populate({
        path: "subjectId",
        match: { userId }
      });

    const filteredTasks = tasks.filter(t => t.subjectId !== null);
    res.json(filteredTasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// 3. Update task status (completed / missed)
exports.updateTaskStatus = async (req, res) => {
  try {
    const { taskId } = req.params;
    const { status } = req.body;

    if (!["completed", "missed"].includes(status)) {
      return res.status(400).json({ message: "Invalid status" });
    }

    const task = await Task.findByIdAndUpdate(
      taskId,
      { status },
      { new: true }
    );

    if (!task) {
      return res.status(404).json({ message: "Task not found" });
    }

    await ActivityLog.create({
      taskId: task._id,
      action: status
    });

    res.json(task);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};


exports.markTaskComplete = async (req, res) => {
  try {
    const { taskId } = req.body;

    await ActivityLog.create({
      taskId,
      action: "completed",
      timestamp: new Date()
    });

    res.json({ message: "Task marked complete" });

  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
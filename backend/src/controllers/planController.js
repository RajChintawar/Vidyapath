const StudyPlan = require("../models/StudyPlan");

// 1. Create / Save study plan
exports.createStudyPlan = async (req, res) => {
  try {
    const { userId, date, tasks } = req.body;

    // overwrite plan if already exists for same date
    const plan = await StudyPlan.findOneAndUpdate(
      { userId, date },
      { userId, date, tasks },
      { upsert: true, new: true }
    );

    res.status(201).json(plan);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// 2. Get study plan for a user on a date
exports.getStudyPlanByDate = async (req, res) => {
  try {
    const { userId, date } = req.params;

    const plan = await StudyPlan.findOne({ userId, date })
      .populate("tasks.taskId");

    if (!plan) {
      return res.status(404).json({ message: "Study plan not found" });
    }

    res.json(plan);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
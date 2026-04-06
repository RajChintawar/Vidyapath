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

// 3. Get latest study plan for a user 


exports.getLatestPlan = async (req, res) => {
  try {
    const { userId } = req.params;

    const plan = await StudyPlan.findOne({ userId })
      .sort({ createdAt: -1 }) // latest plan
      .populate("tasks.taskId"); // 🔥 THIS is for task names

    if (!plan) {
      return res.status(404).json({ message: "No plan found" });
    }

    res.json(plan);

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.generatePlan = async (req, res) => {
  try {
    res.json({ message: "Generate Plan route working" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
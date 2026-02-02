const mongoose = require("mongoose");

const studyPlanSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },
    date: {
      type: Date,
      required: true
    },
    tasks: [
      {
        taskId: {
          type: mongoose.Schema.Types.ObjectId,
          ref: "Task"
        },
        allocatedHours: {
          type: Number
        }
      }
    ]
  },
  { timestamps: true }
);

module.exports = mongoose.model("StudyPlan", studyPlanSchema);

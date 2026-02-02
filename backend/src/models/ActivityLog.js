const mongoose = require("mongoose");

const activityLogSchema = new mongoose.Schema(
  {
    taskId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Task",
      required: true
    },
    action: {
      type: String,
      enum: ["completed", "missed"],
      required: true
    },
    timestamp: {
      type: Date,
      default: Date.now
    }
  }
);

module.exports = mongoose.model("ActivityLog", activityLogSchema);

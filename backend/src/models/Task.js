const mongoose = require("mongoose");

const taskSchema = new mongoose.Schema(
  {
    subjectId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Subject",
      required: true
    },
    topic: {
      type: String,
      required: true
    },
    deadline: {
      type: Date,
      required: true
    },
    estimatedHours: {
      type: Number,
      required: true
    },
    status: {
      type: String,
      enum: ["pending", "completed", "missed"],
      default: "pending"
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Task", taskSchema);

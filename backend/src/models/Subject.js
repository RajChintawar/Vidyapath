const mongoose = require("mongoose");

const subjectSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },
    subjectName: {
      type: String,
      required: true
    },
    difficulty: {
      type: String,
      enum: ["Low", "Medium", "High"],
      default: "Medium"
    },
    examDate: {
      type: Date,
      required: true
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Subject", subjectSchema);

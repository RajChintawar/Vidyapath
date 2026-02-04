const express = require("express");
const router = express.Router();
const {
  createTask,
  getTasksByUser,
  updateTaskStatus
} = require("../controllers/taskController");

router.post("/", createTask);
router.get("/user/:userId", getTasksByUser);
router.patch("/:taskId/status", updateTaskStatus);

module.exports = router;

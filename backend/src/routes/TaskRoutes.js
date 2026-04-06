const express = require("express");
const router = express.Router();
const {
  createTask,
  getTasksByUser,
  updateTaskStatus
} = require("../controllers/taskController");
const { markTaskComplete } = require("../controllers/taskController");

router.post("/", createTask);
router.get("/user/:userId", getTasksByUser);
router.patch("/:taskId/status", updateTaskStatus);
router.post("/mark-complete", markTaskComplete);


module.exports = router;

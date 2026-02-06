const express = require("express");
const router = express.Router();

const {
  createStudyPlan,
  getStudyPlanByDate
} = require("../controllers/planController");

router.post("/", createStudyPlan);
router.get("/:userId/:date", getStudyPlanByDate);

module.exports = router;
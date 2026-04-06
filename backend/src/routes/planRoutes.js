const express = require("express");
const router = express.Router();
const { generatePlan } = require("../controllers/planController");


const {
  createStudyPlan,
  getStudyPlanByDate,
  getLatestPlan
} = require("../controllers/planController");


console.log("StudyPlan routes loaded");
router.post("/generate-plan/:userId", generatePlan);
router.post("/", createStudyPlan);
router.get("/latest/:userId", getLatestPlan);
router.get("/:userId/:date", getStudyPlanByDate);

module.exports = router;
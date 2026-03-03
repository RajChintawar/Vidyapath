const express = require("express");
const router = express.Router();
const aiController = require("../controllers/aiController");

router.post("/generate-plan/:userId", aiController.generatePlan);

module.exports = router;
const axios = require("axios");

exports.generatePlan = async (req, res) => {
  try {
    const { userId } = req.params;

   const response = await axios.post(
  `http://localhost:8000/generate-plan/${userId}`
);

    return res.status(200).json(response.data);

  } catch (error) {
    console.error("AI Service Error:", error.message);
    return res.status(500).json({
      error: "Failed to generate study plan"
    });
  }
};
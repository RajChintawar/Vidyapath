import { useEffect, useState } from "react";
import { getLatestPlan } from "../api/studyplanApi";
import { getProgress } from "../api/progressApi";
import axios from "axios";

import "./dashboard.css";

function Dashboard() {

  const userId = "698579cbefbf271b6d5933d0";

  const [plan, setPlan] = useState(null);
  const [progress, setProgress] = useState(null);

  useEffect(() => {

    getLatestPlan(userId)
      .then(res => setPlan(res.data))
      .catch(err => console.log(err));

    getProgress(userId)
      .then(res => setProgress(res.data))
      .catch(err => console.log(err));

  }, []);

  const riskClass = (risk) => {
    if (risk === "HIGH") return "risk-high";
    if (risk === "MEDIUM") return "risk-medium";
    return "risk-low";
  };

  const generatePlan = () => {

  axios
    .post(
      "http://localhost:8000/generate-plan/698579cbefbf271b6d5933d0"
    )
    .then(() => {

      alert("Plan generated");

      // window.location.reload();

    })
    .catch(err => console.log(err));

};


const replan = async () => {

  try {

    await axios.post(
      "http://localhost:8000/replan/698579cbefbf271b6d5933d0"
    );

    const res = await axios.get(
      "http://localhost:8000/studyplan/latest/698579cbefbf271b6d5933d0"
    );

    setPlan(res.data);

    alert("Replanned");

  } catch (err) {

    console.log(err);

  }

};

  return (

    <div>

      <div className="header">
        Vidyapath Dashboard
      </div>

      <div className="container">

         <button
  onClick={generatePlan}
  style={{
    padding: 10,
    marginBottom: 20,
    background: "#0ea5e9",
    color: "white",
    border: "none",
    borderRadius: 6,
    cursor: "pointer"
  }}
>
  Generate Plan
</button>

<button onClick={replan}
  style={{
    padding: 10,
    marginBottom: 50,
    background: "#0ea5e9",
    color: "white",
    border: "none",
    borderRadius: 6,
    cursor: "pointer"
  }}>
  Replan
</button>
        <div className="grid">

          


          {/* PLAN CARD */}

          {plan && (

            <div className="card">

              <h2>Latest Plan</h2>

              <p>Date: {plan.date}</p>

              <p>Confidence: {plan.confidence}</p>

              <p>
                Risk:
                <span className={riskClass(plan.risk)}>
                  {" "}{plan.risk}
                </span>
              </p>

            </div>

          )}


          {/* PROGRESS CARD */}

          {progress && (

            <div className="card">

              <h2>Progress</h2>

              <p>Total: {progress.totalTasks}</p>
              <p>Completed: {progress.completed}</p>
              <p>Missed: {progress.missed}</p>
              <p>Pending: {progress.pending}</p>
              <p>Avg Confidence: {progress.avgConfidence}</p>
              <p>Risk: {progress.latestRisk}</p>

            </div>

          )}

        </div>


        {/* TASK LIST */}

        {plan && (

          <div className="card task-list">

  <h2>Tasks</h2>

  {plan.tasks.map((t, i) => (

    <div key={i} className="task-item">
      {t.taskId} — {t.allocatedHours} hrs
    </div>

  ))}

</div>

        )}

      </div>

    </div>

  );

}

export default Dashboard;
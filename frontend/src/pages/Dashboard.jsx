import { useEffect, useState } from "react";
import { getLatestPlan } from "../api/studyplanApi";
import { getProgress } from "../api/progressApi";

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

  return (

    <div>

      <div className="header">
        Vidyapath Dashboard
      </div>

      <div className="container">

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
import { useEffect, useState } from "react";
import { getLatestPlan } from "../api/studyplanApi";
import { getProgress } from "../api/progressApi";
import axios from "axios";

import "./dashboard.css";

function Dashboard() {

  const userId = "698579cbefbf271b6d5933d0";

  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState(null);
  const [progress, setProgress] = useState(null);

  useEffect(() => {
// console.log("PLAN DATA:", plan);
//     console.log("RENDERING DASHBOARD");

   getLatestPlan(userId)
  .then(async (res) => {
    if (res.data) {
      setPlan(res.data);
    } else {
      // auto-generate if no plan
      await axios.post(`http://localhost:5000/api/study-plans/generate-plan/${userId}`);
      const newRes = await axios.get(
        `http://localhost:5000/api/study-plans/latest/${userId}`
      );
      setPlan(newRes.data);
    }
  })
  .catch(err => console.error(err));

    getProgress(userId)
      .then(res => setProgress(res.data))
      .catch(err => console.log(err));

  }, []);

  const riskClass = (risk) => {
    if (risk === "HIGH") return "risk-high";
    if (risk === "MEDIUM") return "risk-medium";
    return "risk-low";
  };

  const generatePlan = async () => {
    if (loading) return;

    try {
      setLoading(true);

const resPost = await axios.post(`http://localhost:5000/api/study-plans/generate-plan/${userId}`);
console.log("POST RESPONSE:", resPost.data);
      const res = await axios.get(
        `http://localhost:5000/api/study-plans/latest/${userId}`
      );

setPlan(null); // clear old plan

setTimeout(() => {
  setPlan(res.data);
  alert("New Plan Generated");
}, 100);

    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const replan = async () => {
    try {
      setLoading(true);

      await axios.post(`http://localhost:5000/api/study-plans/generate-plan/${userId}`);

      const res = await axios.get(
  `http://localhost:5000/api/study-plans/latest/${userId}`
);

setPlan(null);
setTimeout(() => {
  setPlan(res.data);
  alert("Replanned Successfully");
}, 100);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (


    

    <div className="dashboard">


      {loading && (
  <div className="overlay">
    Generating new plan...
  </div>
)}

      {/* HEADER */}
      <div className="header">
        Vidyapath Dashboard
      </div>

      <div className="container">

        {/* ACTION BUTTONS */}
        <div className="actions">
          <button onClick={generatePlan} disabled={loading}>
            {loading ? "Generating..." : "Generate Plan"}
          </button>

          <button onClick={replan} className="replan-btn" disabled={loading}>
            Replan
          </button>
        </div>

        {/* CARDS */}
        <div className="grid">

          {plan && (
            <div className="card">
              <h2>Latest Plan</h2>
              <p><b>Date:</b> {plan.date}</p>
              <p><b>Confidence:</b> {plan.confidence}</p>
              <p>
                <b>Risk:</b>
                <span className={riskClass(plan.risk)}>
                  {plan.risk}
                </span>
              </p>
            </div>
          )}

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
<input 
  type="checkbox"
  onChange={async (e) => {
    if (e.target.checked) {
      try {
        await axios.post("http://localhost:5000/api/tasks/mark-complete", {
          taskId: t.taskId?._id
        });
        console.log("Task marked complete");
      } catch (err) {
        console.error(err);
      }
    }
  }}
/>
  <span>{t.taskId?.topic || "Task"}</span>
  
  <span>{t.allocatedHours} hrs</span>
</div>
            ))}

          </div>
        )}

      </div>

    </div>
  );
}

export default Dashboard;
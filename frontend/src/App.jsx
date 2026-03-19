import { useEffect, useState } from "react";
import { getLatestPlan } from "./api/studyplanApi";

function App() {

  const [plan, setPlan] = useState(null);

  const userId = "698579cbefbf271b6d5933d0";

  useEffect(() => {

    getLatestPlan(userId)
      .then(res => {
        setPlan(res.data);
      })
      .catch(err => {
        console.log(err);
      });

  }, []);

  return (
    <div>

      <h1>Vidyapath Dashboard</h1>

      {plan && (
        <div>
          <h2>Date: {plan.date}</h2>
          <h3>Confidence: {plan.confidence}</h3>
          <h3>Risk: {plan.risk}</h3>
        </div>
      )}

    </div>
  );
}

export default App;
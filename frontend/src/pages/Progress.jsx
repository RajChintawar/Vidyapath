import { useEffect, useState } from "react";
import axios from "axios";

function Progress() {

  const [data, setData] = useState(null);

  useEffect(() => {

    axios
      .get(
        "http://localhost:8000/progress/698579cbefbf271b6d5933d0"
      )
      .then(res => setData(res.data))
      .catch(err => console.log(err));

  }, []);

  if (!data) return <div>Loading...</div>;

  return (

    <div style={{ padding: 20 }}>

      <h2>Progress</h2>

      <p>Total Tasks: {data.totalTasks}</p>
      <p>Completed: {data.completed}</p>
      <p>Pending: {data.pending}</p>
      <p>Missed: {data.missed}</p>

      <p>Avg Confidence: {data.avgConfidence}</p>
      <p>Latest Risk: {data.latestRisk}</p>

    </div>

  );

}

export default Progress;
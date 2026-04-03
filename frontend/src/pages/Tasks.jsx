import { useEffect, useState } from "react";
import axios from "axios";

function Tasks() {

  const [tasks, setTasks] = useState([]);

  const loadTasks = () => {

    axios
      .get("http://localhost:8000/tasks/698579cbefbf271b6d5933d0")
      .then(res => setTasks(res.data))
      .catch(err => console.log(err));

  };

  useEffect(() => {
    loadTasks();
  }, []);


  const sendLog = (taskId, action) => {

    axios.post(
      "http://localhost:8000/activitylog",
      {
        taskId: taskId,
        action: action
      }
    )
    .then(() => {
      alert("Logged");
    })
    .catch(err => console.log(err));

  };


  const updateTask = async (taskId, action) => {

  try {

    await axios.post("http://localhost:8000/activitylog", {
      taskId: taskId,
      action: action
    });

    alert(action + " logged");

  } catch (err) {
    console.log(err);
  }

};


  return (

    <div style={{ padding: 20 }}>

      <h2>Tasks</h2>

      {tasks.map(t => (

        <div
          key={t._id}
          style={{
            border: "1px solid gray",
            padding: 10,
            marginBottom: 10,
            borderRadius: 6
          }}
        >

          <b>{t.topic}</b> <br />

          Hours: {t.estimatedHours} <br />

          Status: {t.status} <br />

          Deadline: {t.deadline} <br /><br />


          <button onClick={() => updateTask(t._id, "completed")}>
  Complete
</button>

<button onClick={() => updateTask(t._id, "missed")}>
  Missed
</button>

        </div>

      ))}

    </div>

  );

}

export default Tasks;
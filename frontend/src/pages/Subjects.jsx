import { useEffect, useState } from "react";
import axios from "axios";

function Subjects() {

  const [subjects, setSubjects] = useState([]);

  useEffect(() => {

    axios
      .get("http://localhost:8000/subjects/698579cbefbf271b6d5933d0")
      .then(res => setSubjects(res.data))
      .catch(err => console.log(err));

  }, []);

  return (

    <div style={{ padding: 20 }}>

      <h2>Subjects</h2>

      {subjects.map(s => (

        <div
          key={s._id}
          style={{
            border: "1px solid gray",
            padding: 10,
            marginBottom: 10,
            borderRadius: 6
          }}
        >
          <b>{s.subjectName}</b> <br />
          Difficulty: {s.difficulty} <br />
          Exam: {s.examDate}
        </div>

      ))}

    </div>
  );
}

export default Subjects;
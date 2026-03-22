import { BrowserRouter, Routes, Route } from "react-router-dom";
import Tasks from "./pages/Tasks";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Subjects from "./pages/Subjects";
import Progress from "./pages/Progress";

function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>
        <Route path="/" element={<Dashboard />} />
         <Route path="/subjects" element={<Subjects />} />
         <Route path="/tasks" element={<Tasks />} />
<Route path="/progress" element={<Progress />} />
      </Routes>

    </BrowserRouter>
  );
}

export default App;
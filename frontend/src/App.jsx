import { BrowserRouter, Routes, Route } from "react-router-dom";
import Tasks from "./pages/Tasks";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Subjects from "./pages/Subjects";

function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>
        <Route path="/" element={<Dashboard />} />
         <Route path="/subjects" element={<Subjects />} />
         <Route path="/tasks" element={<Tasks />} />
      </Routes>

    </BrowserRouter>
  );
}

export default App;
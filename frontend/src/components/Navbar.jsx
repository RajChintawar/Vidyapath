import { Link, useLocation } from "react-router-dom";

function Navbar() {

  const location = useLocation();

  const linkStyle = (path) => ({
    color: location.pathname === path ? "#38bdf8" : "white",
    textDecoration: "none",
    fontWeight: "bold",
    padding: "6px 12px",
    borderRadius: "6px",
    background:
      location.pathname === path ? "#1e293b" : "transparent"
  });

  return (
    <div
      style={{
        background: "#0f172a",
        padding: "12px",
        display: "flex",
        gap: "12px",
        alignItems: "center"
      }}
    >
      <Link to="/" style={linkStyle("/")}>
        Dashboard
      </Link>

      <Link to="/subjects" style={linkStyle("/subjects")}>
        Subjects
      </Link>

      <Link to="/tasks" style={linkStyle("/tasks")}>
        Tasks
      </Link>

      <Link to="/progress" style={linkStyle("/progress")}>
        Progress
      </Link>
    </div>
  );
}

export default Navbar;
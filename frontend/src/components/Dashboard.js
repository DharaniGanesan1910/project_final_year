import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();

  const backgroundStyle = {
backgroundImage: `linear-gradient(rgba(2, 6, 23, 0.2), rgba(2, 6, 23, 0.2)), url(${process.env.PUBLIC_URL}/home2.jpg)`,  };

  useEffect(() => {
    fetch("http://127.0.0.1:5000/recent_predictions")
      .then((res) => res.json())
      .catch(() => console.log("Backend offline - using UI mode"));
  }, []);

  const menuItems = [
    { title: "Analyze", icon: "🔍", path: "/analyze", desc: "Detect texts real time" },
    { title: "Features", icon: "🧠", path: "/features", desc: "Display the extracted features" },
    { title: "Structures", icon: "📐", path: "/structures", desc: "Display the mined pattern" },
    { title: "Dataset", icon: "📊", path: "/dataset", desc: "Data Insights" }
  ];

  return (
    <div className="dashboard-wrapper" style={backgroundStyle}>
      {/* FULL TOP NAVIGATION BAR */}
      <nav className="navbar">
        <div className="logo" onClick={() => navigate('/')} style={{cursor: 'pointer'}}>
          🛡️ Shield<span>AI</span>
        </div>
        
        <div className="nav-links">
          <span className="nav-item" onClick={() => navigate("/")}>Home</span>
          {menuItems.map((item) => (
            <span 
              key={item.path}
              className={`nav-item ${location.pathname === item.path ? "active" : ""}`} 
              onClick={() => navigate(item.path)}
            >
              {item.title}
            </span>
          ))}
        </div>
        
        <button className="exit-btn" onClick={() => navigate('/')}>Logout</button>
      </nav>

      <main className="main-content">
        {/* QUOTE SECTION */}
        {/* QUOTE SECTION */}
<section className="quote-container">
  <div className="quote-box">
    <h1 className="title">
“No fixed grammar. No fixed patterns. Still, we detect.”</h1>    <div className="accent-bar"></div>
    <p className="subtitle">
      Linguistic Analysis Framework for Tamil-English Code-Mixed Text
    </p>
  </div>
</section>

        {/* FEATURE GRID */}
        <section className="feature-grid">
          {menuItems.map((item, i) => (
            <div key={i} className="feature-card" onClick={() => navigate(item.path)}>
              <div className="card-icon">{item.icon}</div>
              <h3>{item.title}</h3>
              <p>{item.desc}</p>
            </div>
          ))}
        </section>
      </main>

      <footer className="footer">
        <p><strong>Dharani G</strong> | MCA | Anna University | © 2026</p>
      </footer>
    </div>
  );
}

export default Dashboard;
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Homepage.css';

function Homepage() {
  const navigate = useNavigate();

  const backgroundStyle = {
    // Keeping your home2.jpg reference
    backgroundImage: `linear-gradient(rgba(2, 6, 23, 0.5), rgba(2, 6, 23, 0.6)), url(${process.env.PUBLIC_URL}/home2.jpg)`,
  };

  return (
    <div className="homepage-container" style={backgroundStyle}>
      <nav className="navbar">
        <div className="logo" onClick={() => navigate('/')} style={{cursor:'pointer'}}>
          🛡️ Shield<span>AI</span>
        </div>
        
        <div className="nav-links">
          <button className="nav-text-btn" onClick={() => navigate('/about')}>
            About 
          </button>
          <button className="nav-btn-outline" onClick={() => navigate('/dashboard')}>
            Get Started
          </button>
        </div>
      </nav>

      <main className="main-content">
        <div className="hero-text">
          <h1>
            A Feature-Fusion Framework for Offensive Language Detection and Structural Analysis in Tamil-English Code-Mixed Text
          </h1>
          <p>
            Decode linguistic patterns. Detect toxicity. Defend digital spaces.
          </p>
          <button className="btn-primary" onClick={() => navigate('/dashboard')}>
            Launch 
          </button>
        </div>
      </main>

      <footer className="footer">
        <p><strong>Dharani G</strong> | MCA | Anna University | © 2026</p>
      </footer>
    </div>
  );
}

export default Homepage;
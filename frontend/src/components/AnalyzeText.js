import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./AnalyzeText.css";

function AnalyzeText() {
  const navigate = useNavigate();
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState([]);

  // Background Style
  const backgroundStyle = {
    backgroundImage: `linear-gradient(rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.85)), url(${process.env.PUBLIC_URL}/home_image.jpg)`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundAttachment: 'fixed',
  };

  const fetchPredictions = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/recent_predictions");
      const data = await response.json();
      setPredictions(data);
    } catch (error) {
      console.error("Error fetching predictions:", error);
    }
  };

  useEffect(() => {
    fetchPredictions();
  }, []);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/predict", { text: text });
      setResult(response.data);
      fetchPredictions();
    } catch (error) {
      console.error("Backend Error:", error);
    }
    setLoading(false);
  };

  // Logic to highlight words: Offensive (Red), Safe (Green), Others (White)
  const renderHighlightedText = (inputText, prediction) => {
    if (!inputText) return null;
    const words = inputText.split(" ");
    
    return (
      <div className="highlight-box">
        {words.map((word, index) => {
          let wordColor = "#ffffff"; // Default White
          
          if (prediction === "Offensive") {
            wordColor = "#dc2626"; // Red
          } else if (prediction === "Non-Offensive") {
            wordColor = "#16a34a"; // Green
          }

          return (
            <span key={index} style={{ color: wordColor, fontWeight: "500", marginRight: "6px" }}>
              {word}
            </span>
          );
        })}
      </div>
    );
  };

  return (
    <div className="analyze-wrapper" style={backgroundStyle}>
      {/* TOP NAVIGATION */}
      <nav className="navbar">
        <div className="logo" onClick={() => navigate('/')}>🛡️ Shield<span>AI</span></div>
        <div className="nav-links">
          <span className="nav-item" onClick={() => navigate("/")}>Home</span>
          <span className="nav-item" onClick={() => navigate("/dashboard")}>Portal</span>
          <span className="nav-item active">Analyze</span>
        </div>
      </nav>

      {/* PAGE CONTENT */}
      <div className="analyze-page">
        
        {/* LEFT PANEL */}
        <div className="analyze-container">
          <h1 className="title">Offensive Text Analyzer</h1>
          <p className="subtitle">Detecting toxicity in Tamil-English code-mixed data.</p>

          <textarea
            className="text-input"
            placeholder="Type your text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />

          <button className="analyze-btn" onClick={handleAnalyze}>
            {loading ? "Analyzing Engine..." : "Analyze Text"}
          </button>

          {result && (
            <div className="result-box">
              <h2 className={result.prediction === "Offensive" ? "prediction offensive" : "prediction safe"}>
                {result.prediction === "Offensive" ? "⚠ Offensive" : "✔ Non-Offensive"}
              </h2>

              <div className="confidence-box">
                <strong>Confidence Score:</strong> <span className="score">{result.confidence}</span>
              </div>

              
            </div>
          )}
        </div>

        {/* RIGHT PANEL */}
        <div className="recent-panel">
          <h2>Recent History</h2>
          <div className="recent-list">
            {predictions.length === 0 ? <p>No data yet.</p> : 
              predictions.map((p, index) => (
                <div key={index} className="recent-item">
                  <span className="recent-text">{p.text}</span>
                  <span className={`tag ${p.prediction === "Offensive" ? "offensive" : "safe"}`}>
                    {p.prediction}
                  </span>
                </div>
              ))
            }
          </div>
        </div>

      </div>
    </div>
  );
}

export default AnalyzeText;
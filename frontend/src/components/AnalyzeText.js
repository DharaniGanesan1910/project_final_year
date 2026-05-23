import React, { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./AnalyzeText.css";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

function AnalyzeText() {
  const navigate = useNavigate();

  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState([]);

  const backgroundStyle = {
    backgroundImage: `linear-gradient(rgba(2,6,23,0.85), rgba(2,6,23,0.85)), url(${process.env.PUBLIC_URL}/home_image.jpg)`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundAttachment: "fixed"
  };

  /* -------------------------------- */
  /* Toxic Words */
  /* -------------------------------- */
  const toxicWords = [
    "waste",
    "idiot",
    "stupid",
    "loser",
    "poda",
    "dei",
    "dummy",
    "loosu",
    "kiruku",
    "useless",
    "fool"
  ];

  const highlightToxicWords = (sentence) => {
    if (!sentence) return "";

    return sentence.split(" ").map((word, i) => {
      const clean = word.toLowerCase().replace(/[^\w]/g, "");

      if (toxicWords.includes(clean)) {
        return (
          <span key={i} className="toxic-word">
            {word}{" "}
          </span>
        );
      }

      return word + " ";
    });
  };

  /* -------------------------------- */
  /* Fetch History */
  /* -------------------------------- */
  const fetchPredictions = async () => {
    try {
      const res = await fetch(
        "http://127.0.0.1:5000/recent_predictions"
      );

      const data = await res.json();
      setPredictions(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPredictions();
  }, []);

  /* -------------------------------- */
  /* Analyze */
  /* -------------------------------- */
  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setLoading(true);

    try {
      const res = await axios.post(
        "http://localhost:5000/predict",
        { text }
      );

      setResult(res.data);
      fetchPredictions();
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  /* -------------------------------- */
  /* Language Ratio */
  /* -------------------------------- */
  const tamilCount = Number(
    result?.features?.tamil_tokens || 0
  );

  const englishCount = Number(
    result?.features?.english_tokens || 0
  );

  const total = tamilCount + englishCount;

  const tamilRatio = total
    ? ((tamilCount / total) * 100).toFixed(1)
    : 0;

  const englishRatio = total
    ? ((englishCount / total) * 100).toFixed(1)
    : 0;

  const doughnutData = {
    labels: ["Tamil", "English"],
    datasets: [
      {
        data: [tamilCount, englishCount],
        backgroundColor: ["#ef4444", "#3b82f6"],
        borderWidth: 0
      }
    ]
  };

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#ffffff"
        }
      }
    },
    cutout: "65%"
  };

  /* -------------------------------- */
  /* Severity */
  /* -------------------------------- */
  const getSeverity = () => {
    if (!result) return "Low";

    if (result.prediction === "Non-Offensive")
      return "Safe";

    const toxic = Number(
      result?.features?.total_offensive || 0
    );

    if (toxic >= 3) return "High";
    if (toxic >= 1) return "Moderate";

    return "Low";
  };

  const severity = getSeverity();

  const getRiskPosition = () => {
    if (severity === "Safe") return 10;
    if (severity === "Low") return 35;
    if (severity === "Moderate") return 65;
    return 90;
  };

  const riskPosition = getRiskPosition();

  /* -------------------------------- */
  /* Merge Tokens */
  /* -------------------------------- */
  const mergedAttention = useMemo(() => {
    if (!result?.attention_scores) return [];

    const merged = [];

    result.attention_scores.forEach((item) => {
      const token = item.token;
      const score = Number(item.score);

      if (token.startsWith("▁")) {
        merged.push({
          token: token.replace("▁", ""),
          score
        });
      } else {
        if (merged.length > 0) {
          merged[merged.length - 1].token += token;

          merged[merged.length - 1].score =
            Math.max(
              merged[merged.length - 1].score,
              score
            );
        } else {
          merged.push({
            token,
            score
          });
        }
      }
    });

    return merged;
  }, [result]);

  return (
    <div
      className="analyze-wrapper"
      style={backgroundStyle}
    >
      {/* NAVBAR */}
      <nav className="navbar">
        <div
          className="logo"
          onClick={() => navigate("/")}
        >
          🛡️ Shield<span>AI</span>
        </div>

        <div className="nav-links">
          <span onClick={() => navigate("/")}>
            Home
          </span>

          <span
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Portal
          </span>

          <span className="active">
            Analyze
          </span>
        </div>
      </nav>

      {/* MAIN */}
      <div className="analyze-page">
        {/* LEFT */}
        <div className="analyze-container">
          <h1 className="title">
            Offensive Text Analyzer
          </h1>

          <textarea
            className="text-input"
            value={text}
            onChange={(e) =>
              setText(e.target.value)
            }
            placeholder="Type Tamil-English mixed text..."
          />

          <button
            className="analyze-btn"
            onClick={handleAnalyze}
          >
            {loading
              ? "Analyzing..."
              : "Analyze"}
          </button>

          {result && (
            <div className="result-box">
              <h2
                className={
                  result.prediction ===
                  "Offensive"
                    ? "prediction offensive"
                    : "prediction safe"
                }
              >
                {result.prediction}
              </h2>

              {result.reason && (
                <div className="reason-box">
                  Reason:{" "}
                  <span>
                    {result.reason}
                  </span>
                </div>
              )}

              <div className="confidence-section">
                <div className="confidence-label">
                  Confidence:{" "}
                  {(
                    result.confidence * 100
                  ).toFixed(1)}
                  %
                </div>

                <div className="confidence-bar-bg">
                  <div
                    className="confidence-bar-fill"
                    style={{
                      width: `${
                        result.confidence *
                        100
                      }%`
                    }}
                  ></div>
                </div>
              </div>

              <div className="severity-box">
                Severity:
                <span
                  className={
                    severity === "High"
                      ? "sev-high"
                      : severity ===
                        "Moderate"
                      ? "sev-medium"
                      : "sev-low"
                  }
                >
                  {" "}
                  {severity}
                </span>
              </div>

              <div className="risk-meter-box">
                <h3>Risk Meter</h3>

                <div className="risk-scale">
                  <div className="risk-line"></div>

                  <div
                    className="risk-pointer"
                    style={{
                      left: `${riskPosition}%`
                    }}
                  >
                    ▲
                  </div>

                  <div className="risk-labels">
                    <span>SAFE</span>
                    <span>LOW</span>
                    <span>MEDIUM</span>
                    <span>HIGH</span>
                  </div>
                </div>

                <p className="risk-value">
                  Severity Level:{" "}
                  {severity}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT */}
        <div className="features-panel scrollable-right">
          {result?.processed_text && (
            <div className="processed-box">
              <h3>Processed Text</h3>

              <p>
                {highlightToxicWords(
                  result.processed_text
                )}
              </p>
            </div>
          )}

          {result?.token_languages && (
            <div className="token-box">
              <h3>
                Tokens with Language
              </h3>

              <div className="token-list">
                {result.token_languages.map(
                  (t, i) => (
                    <span
                      key={i}
                      className={`token ${t.language.toLowerCase()}`}
                    >
                      {t.token} (
                      {t.language})
                    </span>
                  )
                )}
              </div>
            </div>
          )}

          {result?.code_switching && (
            <div className="codeswitch-box">
              <h3>
                Code Switching
              </h3>

              {Object.entries(
                result.code_switching
              ).map(([k, v]) => (
                <div
                  key={k}
                  className="cs-item"
                >
                  <span>{k}</span>
                  <span>{v}</span>
                </div>
              ))}
            </div>
          )}

          {result?.features && (
            <div className="ratio-card">
              <h3>Language Ratio</h3>

              <div
                style={{
                  width: "240px",
                  margin: "auto"
                }}
              >
                <Doughnut
                  data={doughnutData}
                  options={doughnutOptions}
                />
              </div>

              <p className="ratio-text">
                Tamil: {tamilRatio}% |
                English:{" "}
                {englishRatio}%
              </p>
            </div>
          )}

          <h2>Sample Features</h2>

          {result && (
            <div className="features-grid">
              {Object.entries(
                result.features || {}
              ).map(([k, v]) => (
                <div
                  key={k}
                  className="feature-item"
                >
                  <div className="feature-value">
                    {v}
                  </div>

                  <div className="feature-key">
                    {k}
                  </div>
                </div>
              ))}

              {result?.code_switching_position &&
                Object.entries(
                  result.code_switching_position
                ).map(
                  ([k, v], i) => (
                    <div
                      key={i}
                      className="feature-item highlight"
                    >
                      <div className="feature-value">
                        {v}
                      </div>

                      <div className="feature-key">
                        {k}
                      </div>
                    </div>
                  )
                )}
            </div>
          )}

          {/* Attention */}
          {mergedAttention.length > 0 && (
            <div className="attention-bert-box">
              <h3>
                Attention Visualization
              </h3>

              <div className="bert-token-wrap">
                {(() => {
                  const maxScore =
                    Math.max(
                      ...mergedAttention.map(
                        (x) =>
                          Number(
                            x.score
                          )
                      ),
                      0.001
                    );

                  return mergedAttention.map(
                    (item, i) => {
                      const raw =
                        Number(
                          item.score
                        );

                      const score =
                        raw /
                        maxScore;

                      return (
                        <div
                          key={i}
                          className="bert-token"
                          style={{
                            backgroundColor: `rgba(220,38,38,${
                              0.15 +
                              score *
                                0.85
                            })`,
                            color:
                              score >
                              0.55
                                ? "#fff"
                                : "#111"
                          }}
                        >
                          <span className="token-word">
                            {
                              item.token
                            }
                          </span>

                          <span className="token-score">
                            {raw.toFixed(
                              3
                            )}
                          </span>
                        </div>
                      );
                    }
                  );
                })()}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* HISTORY */}
      <div className="recent-panel-bottom">
        <h2>Recent History</h2>

        <div className="recent-list">
          {predictions.map((p, i) => (
            <div
              key={i}
              className={`recent-item ${
                p.prediction ===
                "Offensive"
                  ? "offensive"
                  : "safe"
              }`}
            >
              <span className="recent-text">
                {p.text}
              </span>

              <span className="tag">
                {p.prediction}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AnalyzeText;
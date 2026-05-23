import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Pattern.css";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar, Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function Pattern() {
  const navigate = useNavigate();
  const [selectedPattern, setSelectedPattern] = useState(null);

  /* ------------------------------ */
  /* PATTERN DATA */
  /* ------------------------------ */
  const patterns = [
    { name: "SOV", count: 20173 },
    { name: "SOV-NEG", count: 8948 },
    { name: "SOVA", count: 1640 },
    { name: "UNKNOWN", count: 1081 },
    { name: "SVC", count: 1074 },
    { name: "SV", count: 932 },
    { name: "ASOV", count: 700 },
    { name: "IMP", count: 500 },
  ];

  const total = 35139;

  /* ------------------------------ */
  /* METHODOLOGY */
  /* ------------------------------ */
  const methodology = [
    {
      name: "SpaCy",
      desc: "Used for English tokenization and POS tagging.",
      example: "You are idiot → PRON + VERB + NOUN",
    },
    {
      name: "Stanza",
      desc: "Used for Tamil dependency parsing.",
      example: "naan varen → Subject + Verb",
    },
    {
      name: "Rule-Based System",
      desc: "Custom grammar rules for SOV, SVC, IMP detection.",
      example: "poda dei → Imperative + insult",
    },
  ];

  /* ------------------------------ */
  /* PATTERN DETAILS */
  /* ------------------------------ */
  const patternDetails = {
    SOV: {
      examples: ["naan activity mudichiten"],
      offensive: 4200,
      non_offensive: 15973,
      toxicity: 0.28,
    },
    "SOV-NEG": {
      examples: [ "ava message anupala"],
      offensive: 3100,
      non_offensive: 5848,
      toxicity: 0.35,
    },
    SOVA: {
      examples: ["avan office vandhan nethu"],
      offensive: 900,
      non_offensive: 740,
      toxicity: 0.38,
    },
    UNKNOWN: {
      examples: ["random sentence", "unclear structure"],
      offensive: 500,
      non_offensive: 581,
      toxicity: 0.30,
    },
    SVC: {
      examples: [ "you are idiot"],
      offensive: 800,
      non_offensive: 274,
      toxicity: 0.76,
    },
    SV: {
      examples: ["naan varuven"],
      offensive: 300,
      non_offensive: 632,
      toxicity: 0.25,
    },
    ASOV: {
      examples: ["nalaiku naan college poren"],
      offensive: 200,
      non_offensive: 500,
      toxicity: 0.22,
    },
    IMP: {
      examples: [ "shut up"],
      offensive: 1500,
      non_offensive: 300,
      toxicity: 0.88,
    },
  };

  const stats = {
    total,
    unique:7,
    dominant: patterns.reduce((a, b) => (a.count > b.count ? a : b)).name,
    least: patterns.reduce((a, b) => (a.count < b.count ? a : b)).name,
  };

  /* ------------------------------ */
  /* GRAPHS */
  /* ------------------------------ */

  // 1. Pattern Frequency
  const frequencyData = {
    labels: patterns.map((p) => p.name),
    datasets: [
      {
        label: "Pattern Count",
        data: patterns.map((p) => p.count),
        backgroundColor: "#38bdf8",
        borderRadius: 6,
      },
    ],
  };

  // 2. Structure vs Toxicity
  const toxicityData = {
    labels: Object.keys(patternDetails),
    datasets: [
      {
        label: "Toxicity Score",
        data: Object.values(patternDetails).map((p) => p.toxicity),
        backgroundColor: "#ef4444",
      },
    ],
  };

  // 3. Offensive vs Non-Offensive
  const offenseData = {
    labels: Object.keys(patternDetails),
    datasets: [
      {
        label: "Offensive",
        data: Object.values(patternDetails).map((p) => p.offensive),
        backgroundColor: "#ef4444",
      },
      {
        label: "Non-Offensive",
        data: Object.values(patternDetails).map((p) => p.non_offensive),
        backgroundColor: "#22c55e",
      },
    ],
  };

  // 4. Toxicity Trend
  const trendData = {
    labels: Object.keys(patternDetails),
    datasets: [
      {
        label: "Toxicity Trend",
        data: Object.values(patternDetails).map((p) => p.toxicity),
        borderColor: "#38bdf8",
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="pattern-wrapper">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo" onClick={() => navigate("/")}>
          🛡️ Shield<span>AI</span>
        </div>
        <div className="nav-links">
          <span onClick={() => navigate("/")}>Home</span>
          <span onClick={() => navigate("/dashboard")}>Portal</span>
          <span className="active">Structures</span>
        </div>
      </nav>

      <main className="pattern-main">


        {/* HERO */}
        <section className="hero">
          <h1>Code-Mixed Pattern Intelligence</h1>
          <p>Structural + toxicity analysis of Tamil-English dataset</p>
        </section>


        {/* ================= METHODOLOGY ================= */}
        <section className="methodology-box">
          <h2>Methodology</h2>
          <div className="method-grid">
            {methodology.map((m, i) => (
              <div key={i} className="method-card">
                <h3>{m.name}</h3>
                <p>{m.desc}</p>
                <small>{m.example}</small>
              </div>
            ))}
          </div>
        </section>

        {/* STATS */}
        <section className="stats-grid">
          <div className="card"><h3>{stats.total}</h3><p>Total Sentences</p></div>
          <div className="card"><h3>{stats.unique}</h3><p>Unique Patterns</p></div>
          <div className="card"><h3>{stats.dominant}</h3><p>Dominant Pattern</p></div>
          <div className="card"><h3>{stats.least}</h3><p>Least Pattern</p></div>
        </section>

        {/* ================= GRAPHS ================= */}
        <section className="chart-grid">

          <div className="chart-box">
            <h2>Pattern Frequency</h2>
            <Bar data={frequencyData} />
          </div>

          <div className="chart-box">
            <h2>Structure vs Toxicity</h2>
            <Bar data={toxicityData} />
          </div>

          <div className="chart-box">
            <h2>Offensive vs Non-Offensive</h2>
            <Bar data={offenseData} />
          </div>

          <div className="chart-box">
            <h2>Toxicity Trend</h2>
            <Line data={trendData} />
          </div>

        </section>

        {/* TABLE */}
        <section className="table-box">
          <h2>Pattern Count Analysis</h2>

          <table>
            <thead>
              <tr>
                <th>Pattern</th>
                <th>Count</th>
                <th>%</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {patterns.map((p, i) => (
                <tr key={i}>
                  <td>{p.name}</td>
                  <td>{p.count}</td>
                  <td>{((p.count / total) * 100).toFixed(2)}%</td>
                  <td>
                    <button onClick={() => setSelectedPattern(p.name)}>
                      Analyze
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* ANALYSIS */}
        {selectedPattern && (
          <section className="analysis-box">
            <h2>{selectedPattern} Analysis</h2>

            <ul>
              {patternDetails[selectedPattern].examples.map((e, i) => (
                <li key={i}>{e}</li>
              ))}
            </ul>

            <p>Offensive: {patternDetails[selectedPattern].offensive}</p>
            <p>Non-Offensive: {patternDetails[selectedPattern].non_offensive}</p>
            <p>Toxicity: {patternDetails[selectedPattern].toxicity}</p>

            <button onClick={() => setSelectedPattern(null)}>
              Close
            </button>
          </section>
        )}

      </main>
    </div>
  );
}

export default Pattern;
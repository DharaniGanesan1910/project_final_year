import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Pattern.css";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Pattern() {
  const navigate = useNavigate();

  const [chartData, setChartData] = useState(null);
  const [patterns, setPatterns] = useState([]);
  const [allPatterns, setAllPatterns] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    offensive: 0,
    nonOffensive: 0,
    unique: 0
  });

  useEffect(() => {
    axios.get("http://localhost:5000/pattern-data")
      .then((res) => {
        const { labels, values, total, offensive, non_offensive } = res.data;

        const patternList = labels.map((label, i) => ({
          name: label,
          count: values[i]
        })).sort((a, b) => b.count - a.count);

        setPatterns(patternList.slice(0, 3));
        setAllPatterns(patternList);

        setStats({
          total: total,
          offensive: offensive,
          nonOffensive: non_offensive,
          unique: labels.length
        });

        setChartData({
          labels: labels,
          datasets: [{
            label: "Sentences",
            data: values,
            backgroundColor: "rgba(56, 189, 248, 0.5)",
            borderColor: "#38bdf8",
            borderWidth: 2,
            borderRadius: 6
          }]
        });
      })
      .catch(err => console.error(err));
  }, []);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: "Sentence Structure Distribution",
        color: "#f8fafc"
      }
    },
    scales: {
      y: {
        ticks: { color: "#94a3b8" },
        grid: { color: "rgba(255,255,255,0.05)" }
      },
      x: {
        ticks: { color: "#94a3b8" },
        grid: { display: false }
      }
    }
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

      <main className="pattern-viewport">

        {/* HEADER */}
        <header className="pattern-header">
          <h2>Sentence Structure Analysis</h2>
          <p>
            Code-mixed language has no fixed grammar, yet hidden patterns emerge
            through data-driven analysis.
          </p>
        </header>

        {/* 🔧 TECHNIQUES */}
        <section className="techniques">
          <h3>Techniques Used</h3>
          <ul>
            <li><b>spaCy:</b> English dependency parsing</li>
            <li><b>Stanza:</b> Tamil and multilingual processing</li>
            <li><b>Rule-Based Logic:</b> Roman tamil words</li>
          </ul>
        </section>

        {/* 📊 STATS */}
        <div className="stats-grid">
          <div className="mini-card">
            <span>Total Sentences</span>
            <p>{stats.total}</p>
          </div>
          
          <div className="mini-card">
            <span>Unique Patterns</span>
            <p>7</p>
          </div>
        </div>

        {/* 📈 CHART */}
        <div className="chart-box">
          {chartData
            ? <Bar data={chartData} options={options} />
            : <div className="loader">Analyzing...</div>}
        </div>

        {/* 🏆 TOP 3 */}
        <section className="top-patterns">
          <h3>Dominant Structure</h3>
          <div className="rank-grid">
            <h4>SOV</h4>
            <p>20173 sentences</p>
          </div>
        </section>

        {/* 📋 TABLE */}
        <section className="pattern-table">
          <h3>All Pattern Counts</h3>
          <table>
            <thead>
              <tr>
                <th>Pattern</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {allPatterns.map((p, i) => (
                <tr key={i}>
                  <td>{p.name}</td>
                  <td>{p.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* 🧾 EXAMPLES */}
        <section className="examples">
          <h3>Example Sentences</h3>

          <div className="example-card">
            <p>naan activity mudichiten</p>
            <span>SOV</span>
          </div>

          <div className="example-card">
            <p>ava message anupala</p>
            <span>SOV (NEG)</span>
          </div>

          <div className="example-card">
            <p>indha padam super</p>
            <span>SVC</span>
          </div>
        </section>

        {/* 🧠 INSIGHTS */}
        <section className="insights">
         
         
  <h3>Insights</h3>
 <p className="insight-note">
These insights are derived from analyzing sentence structures in the training dataset and help explain how linguistic patterns contribute
 to offensive language detection.</p>
  <div className="insight-card">
    <p><b>Direct Targeting:</b> Offensive sentences often target second-person pronouns.</p>
    <ul>
      <li>you are useless</li>
      <li>nee romba worst</li>
    </ul>
  </div>

  <div className="insight-card">
    <p><b>Short & Aggressive:</b> Short, direct structures dominate aggressive language.</p>
    <ul>
      <li>shut up</li>
      <li>poda</li>
    </ul>
  </div>

  <div className="insight-card">
    <p><b>Code-Mixed Patterns:</b> Even without fixed grammar, repeated structures appear.</p>
    <ul>
      <li>nee waste fellow</li>
      <li>avan sema genius</li>
      <li>indha game worst</li>
    </ul>
  </div>

</section>

      </main>
    </div>
  );
}

export default Pattern;
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";
import "./DatasetInsights.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

function DatasetInsights() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/dataset_insights")
      .then(res => res.json())
      .then(d => {
        console.log("API DATA:", d); // Debug
        setData(d);
      })
      .catch(err => console.error(err));
  }, []);

  // ✅ Safe loading check
  if (!data || !data.language_composition) {
    return <div className="loader-screen">Mining Dataset Analytics...</div>;
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: "#f8f9fa", font: { size: 10 } }
      }
    },
    scales: {
      y: {
        ticks: { color: "#f8f9fa" },
        grid: { color: "rgba(255,255,255,0.05)" }
      },
      x: {
        ticks: { color: "#f8f9fa" }
      }
    }
  };

  return (
    <div className="dataset-wrapper">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo" onClick={() => navigate('/')}>
          🛡️ Shield<span>AI</span>
        </div>
        <div className="nav-links">
          <span onClick={() => navigate("/")}>Home</span>
          <span onClick={() => navigate("/dashboard")}>Portal</span>
          <span className="active">Dataset</span>
        </div>
      </nav>

      <main className="dataset-viewport">

        {/* HEADER */}
        <header className="dataset-header">
          <h1>Dataset Analytics</h1>
          <p>Statistical distribution of the Tamil-English Code-Mixed corpus.</p>
        </header>

        {/* SUMMARY */}
        <div className="summary-cards">
          <div className="mini-card">
            <span>Total Sentences</span>
            <p>{data.total_sentences || 0}</p>
          </div>
          <div className="mini-card">
            <span>Avg Length</span>
            <p>{data.avg_length || 0} words</p>
          </div>
        </div>

        <div className="insight-grid">

          {/* 1️⃣ Language Composition */}
          <div className="insight-card">
            <h3>Language Composition</h3>
            <div className="chart-box">
              <Bar
                options={chartOptions}
                data={{
                  labels: data.language_composition?.labels || [],
                  datasets: [{
                    label: "Word Count",
                    data: data.language_composition?.values || [],
                    backgroundColor: ["#38bdf8", "#818cf8"],
                    borderRadius: 5
                  }]
                }}
              />
            </div>
            <p className="observation">
              Tamil words dominate, reflecting native code-mixed usage.
            </p>
          </div>

          {/* 2️⃣ Sentence Length */}
          <div className="insight-card">
            <h3>Sentence Length</h3>
            <div className="chart-box">
              <Bar
                options={chartOptions}
                data={{
                  labels: data.sentence_length?.labels || [],
                  datasets: [{
                    label: "Sentence Count",
                    data: data.sentence_length?.values || [],
                    backgroundColor: "#f43f5e",
                    borderRadius: 5
                  }]
                }}
              />
            </div>
            <p className="observation">
Most sentences are medium to long, reflecting expressive user-generated content.            </p>
          </div>

          {/* 3️⃣ Code Switching */}
          <div className="insight-card">
            <h3>Code Switching</h3>
            <div className="chart-box pie-adjust">
              <Pie
                data={{
                  labels: data.code_switching?.labels || [],
                  datasets: [{
                    data: data.code_switching?.values || [],
                    backgroundColor: ["#0ea5e9", "#10b981", "#f59e0b"]
                  }]
                }}
              />
            </div>
            <p className="observation">
              High mixing shows informal bilingual communication.
            </p>
          </div>

          

          {/* 5️⃣ Top Offensive Words */}
          <div className="insight-card">
            <h3>Top Offensive Terms</h3>
            <div className="chart-box">
              <Bar
                options={chartOptions}
                data={{
                  labels: data.top_offensive_words?.labels || [],
                  datasets: [{
                    label: "Frequency",
                    data: data.top_offensive_words?.values || [],
                    backgroundColor: "#fb7185"
                  }]
                }}
              />
            </div>
            <p className="observation">
Recurring tokens significantly influence offensive classification patterns.            </p>
          </div>

          {/* 6️⃣ Structure vs Offensiveness */}
          <div className="insight-card">
            <h3>Structure vs Offensiveness</h3>
            <div className="chart-box">
              <Bar
                options={chartOptions}
                data={{
                  labels: data.structure_offense?.labels || [],
                  datasets: [{
                    label: "Offensive %",
                    data: data.structure_offense?.values || [],
                    backgroundColor: "#a78bfa"
                  }]
                }}
              />
            </div>
            <p className="observation">
              Certain sentence structures show higher offensive likelihood.
            </p>
          </div>

          {/* 7️⃣ Sample Sentences */}
          <div className="insight-card">
            <h3>Sample Data</h3>
            <ul>
              {(data.samples || []).map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

        </div>

      </main>
    </div>
  );
}

export default DatasetInsights;
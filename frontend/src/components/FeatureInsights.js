import React, { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./FeatureInsights.css";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from "chart.js";

import { Radar } from "react-chartjs-2";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

/* Put inside component */
const radarData = {
  labels: [
    "Code-Switch",
    "Lexical",
    "Structural",
    "Stylometric",
    "Offensive"
  ],
  datasets: [
    {
      label: "Offensive %",
      data: [56, 55, 60, 59, 74], // avg values
      backgroundColor: "rgba(239,68,68,0.25)",
      borderColor: "#ef4444",
      pointBackgroundColor: "#ef4444",
      borderWidth: 2
    },
    {
      label: "Non-Offensive %",
      data: [44, 45, 40, 41, 26],
      backgroundColor: "rgba(59,130,246,0.18)",
      borderColor: "#3b82f6",
      pointBackgroundColor: "#3b82f6",
      borderWidth: 2
    }
  ]
};

const radarOptions = {
  responsive: true,
  plugins: {
    legend: {
      labels: { color: "#fff" }
    }
  },
  scales: {
    r: {
      min: 0,
      max: 100,
      ticks: {
        color: "#cbd5e1",
        backdropColor: "transparent"
      },
      grid: {
        color: "rgba(255,255,255,0.12)"
      },
      angleLines: {
        color: "rgba(255,255,255,0.12)"
      },
      pointLabels: {
        color: "#ffffff",
        font: { size: 12 }
      }
    }
  }
};

function FeatureInsights() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [sort, setSort] = useState("high");

  const features = [
    // CODE-SWITCH
    { feature:"num_ta", off:57.58, non:42.42, category:"Code-Switch", obs:"Offensive comments contain slightly more Tamil words." },
    { feature:"num_en", off:47.55, non:52.45, category:"Code-Switch", obs:"Non-offensive comments contain slightly more English tokens." },
    { feature:"ta_ratio", off:58.12, non:41.88, category:"Code-Switch", obs:"Higher Tamil ratio often appears in offensive text." },
    { feature:"en_ratio", off:46.75, non:53.25, category:"Code-Switch", obs:"Higher English ratio often appears in non-offensive text." },
    { feature:"language_dominance", off:59.03, non:40.97, category:"Code-Switch", obs:"Tamil-dominant sentences more often offensive." },
    { feature:"num_switches", off:56.14, non:43.86, category:"Code-Switch", obs:"More language switching in abusive comments." },
    { feature:"switch_density", off:55.09, non:44.91, category:"Code-Switch", obs:"Dense Tamil-English switching detected." },
    { feature:"switch_beginning", off:52.68, non:47.32, category:"Code-Switch", obs:"Switching sometimes starts early." },
    { feature:"switch_middle", off:55.22, non:44.78, category:"Code-Switch", obs:"Most switching occurs mid-sentence." },
    { feature:"switch_end", off:53.31, non:46.69, category:"Code-Switch", obs:"Switching can occur at sentence end." },
    { feature:"ta_to_en_switch", off:56.49, non:43.51, category:"Code-Switch", obs:"Tamil to English transitions are common." },
    { feature:"en_to_ta_switch", off:55.01, non:44.99, category:"Code-Switch", obs:"English to Tamil transitions also common." },

    // LEXICAL
    { feature:"total_tokens", off:54.87, non:45.13, category:"Lexical", obs:"Offensive comments are slightly longer." },
    { feature:"char_length", off:54.02, non:45.98, category:"Lexical", obs:"Offensive text tends to be longer in characters." },
    { feature:"avg_word_length", off:51.63, non:48.37, category:"Lexical", obs:"Minimal difference in average word length." },
    { feature:"tamil_script_count", off:56.21, non:43.79, category:"Lexical", obs:"Tamil script count higher in offensive text." },
    { feature:"tamil_script_ratio", off:56.78, non:43.22, category:"Lexical", obs:"Higher Tamil script ratio correlates with offense." },
    { feature:"tamil_suffix_count", off:57.93, non:42.07, category:"Lexical", obs:"Tamil suffix usage higher in abuse." },
    { feature:"english_target_pronouns", off:58.14, non:41.86, category:"Lexical", obs:"Target pronouns like 'you' appear more often." },

    // STRUCTURAL
    { feature:"has_subject", off:48.92, non:51.08, category:"Structural", obs:"Subject presence has low distinction." },
    { feature:"has_object", off:61.33, non:38.67, category:"Structural", obs:"Offensive comments target a person/entity." },
    { feature:"has_verb", off:52.10, non:47.90, category:"Structural", obs:"Verbs common in both classes." },
    { feature:"has_complement", off:57.45, non:42.55, category:"Structural", obs:"Complements carry descriptive insults." },
    { feature:"has_adverb", off:54.89, non:45.11, category:"Structural", obs:"Adverbs slightly intensify abuse." },
    { feature:"verb_position", off:55.67, non:44.33, category:"Structural", obs:"Flexible verb positioning in offensive text." },
    { feature:"verb_final", off:58.11, non:41.89, category:"Structural", obs:"Tamil-style verb-final pattern common." },
    { feature:"verb_initial", off:53.22, non:46.78, category:"Structural", obs:"Commands often begin with verbs." },
    { feature:"adverb_initial", off:52.98, non:47.02, category:"Structural", obs:"Adverbs may appear initially for emphasis." },
    { feature:"adverb_final", off:54.12, non:45.88, category:"Structural", obs:"Sentence-final adverbs intensify tone." },
    { feature:"structure_length", off:56.84, non:43.16, category:"Structural", obs:"Offensive text has slightly richer structure." },
    { feature:"argument_count", off:60.25, non:39.75, category:"Structural", obs:"Higher arguments indicate targeted insults." },
    { feature:"is_transitive", off:62.77, non:37.23, category:"Structural", obs:"Transitive verbs often target others." },
    { feature:"is_copular", off:59.14, non:40.86, category:"Structural", obs:"'You are...' patterns common in insults." },
    { feature:"is_imperative", off:66.35, non:33.65, category:"Structural", obs:"Commands strongly linked with abuse." },
    { feature:"has_negation", off:63.84, non:36.16, category:"Structural", obs:"Negation common in criticism." },

    // STYLOMETRIC
    { feature:"exclamation_count", off:59.84, non:40.16, category:"Stylometric", obs:"Exclamation marks emphasize anger." },
    { feature:"question_count", off:56.22, non:43.78, category:"Stylometric", obs:"Questions may indicate sarcasm/aggression." },
    { feature:"punctuation_count", off:57.14, non:42.86, category:"Stylometric", obs:"More punctuation in offensive text." },
    { feature:"uppercase_count", off:58.77, non:41.23, category:"Stylometric", obs:"Capital letters imply shouting." },
    { feature:"uppercase_ratio", off:59.16, non:40.84, category:"Stylometric", obs:"Uppercase emphasis stronger in abuse." },
    { feature:"emoji_count", off:61.32, non:38.68, category:"Stylometric", obs:"Emojis reinforce emotional tone." },
    { feature:"repeated_char_words", off:64.90, non:35.10, category:"Stylometric", obs:"Repeated chars intensify insults." },
    { feature:"elongated_english_words", off:62.41, non:37.59, category:"Stylometric", obs:"Elongated English words amplify tone." },
    { feature:"digit_count", off:49.21, non:50.79, category:"Stylometric", obs:"Digits have minimal effect." },

    // OFFENSIVE
    { feature:"offensive_at_beginning", off:74.55, non:25.45, category:"Offensive", obs:"Many insults begin immediately." },
    { feature:"offensive_at_end", off:72.81, non:27.19, category:"Offensive", obs:"Abusive endings common." },
    { feature:"consecutive_offensive_words", off:76.93, non:23.07, category:"Offensive", obs:"Multiple abusive words clustered." },
    { feature:"tamil_offensive_count", off:79.28, non:20.72, category:"Offensive", obs:"Strongest indicator overall." },
    { feature:"english_offensive_count", off:63.00, non:37.00, category:"Offensive", obs:"English abuse also contributes." },
    { feature:"total_offensive", off:77.44, non:22.56, category:"Offensive", obs:"More abusive tokens in toxic text." },
    { feature:"offensive_ratio", off:76.11, non:23.89, category:"Offensive", obs:"High offensive density strongly predictive." },
    { feature:"tamil_offensive_ratio", off:77.78, non:22.22, category:"Offensive", obs:"Tamil abusive ratio highly predictive." },
    { feature:"english_offensive_ratio", off:60.91, non:39.09, category:"Offensive", obs:"English abusive ratio moderately predictive." }
  ];

  const categories = ["All", "Code-Switch", "Lexical", "Structural", "Stylometric", "Offensive"];

  const filtered = useMemo(() => {
    let data = [...features];

    if (category !== "All") {
      data = data.filter((f) => f.category === category);
    }

    if (search.trim()) {
      data = data.filter((f) =>
        f.feature.toLowerCase().includes(search.toLowerCase())
      );
    }

    data.sort((a, b) => (sort === "high" ? b.off - a.off : a.off - b.off));
    return data;
  }, [search, category, sort]);

  return (
    <div className="feature-page">
      <nav className="navbar">
        <div className="logo" onClick={() => navigate("/")}>
          🛡️ Shield<span>AI</span>
        </div>

        <div className="nav-links">
          <span className="nav-item" onClick={() => navigate("/")}>Home</span>
          <span className="nav-item" onClick={() => navigate("/dashboard")}>Portal</span>
          <span className="nav-item" onClick={() => navigate("/analyze")}>Analyze</span>
          <span className="nav-item active">Features</span>
        </div>
      </nav>

      <div className="content-container">
        <h1>Feature Explainability Dashboard</h1>
        <p className="para">
          All extracted features grouped into interpretable categories for offensive language detection.
        </p>

        <div className="filter-row">
          <input
            type="text"
            placeholder="Search feature..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {categories.map((c, i) => <option key={i}>{c}</option>)}
          </select>

          <select value={sort} onChange={(e) => setSort(e.target.value)}>
            <option value="high">Highest First</option>
            <option value="low">Lowest First</option>
          </select>
        </div>

        <div className="table-container">
          <table className="feature-table">
            <thead>
              <tr>
                <th>Feature</th>
                <th>Distribution</th>
                <th>Category</th>
                <th>Observation</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map((f, i) => (
                <tr key={i}>
                  <td className="feature-name"><code>{f.feature}</code></td>

                  <td className="stats-cell">
                    <div className="bar-wrapper">
                      <div className="bar offensive-bar" style={{ width: `${f.off}%` }}>
                        {f.off}%
                      </div>
                      <div className="bar safe-bar" style={{ width: `${f.non}%` }}>
                        {f.non}%
                      </div>
                    </div>
                  </td>

                  <td>{f.category}</td>
                  <td className="obs-text">{f.obs}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="chart-box">
  <h2> Category-wise Radar Map</h2>
  <Radar data={radarData} options={radarOptions} />
</div>

    </div>
  );
}

export default FeatureInsights;
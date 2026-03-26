import React from "react";
import { useNavigate } from "react-router-dom"; // Added for navigation
import "./FeatureInsights.css";

function FeatureInsights() {
  const navigate = useNavigate();

  const features = [

{
feature:"tamil_offensive_count",
off:79.28,
non:20.72,
obs:"Tamil abusive words are the strongest indicator of offensive sentences."
},

{
feature:"english_offensive_count",
off:63.00,
non:37.00,
obs:"English abusive words also contribute to offensive content but less than Tamil."
},

{
feature:"total_offensive",
off:77.44,
non:22.56,
obs:"Total offensive tokens are significantly higher in offensive sentences."
},

{
feature:"offensive_ratio",
off:76.11,
non:23.89,
obs:"Higher proportion of abusive words strongly correlates with offensive classification."
},

{
feature:"tamil_offensive_ratio",
off:77.78,
non:22.22,
obs:"Tamil offensive words dominate code-mixed abusive comments."
},

{
feature:"english_offensive_ratio",
off:60.91,
non:39.09,
obs:"English offensive words are present but less dominant."
},

{
feature:"num_ta",
off:57.58,
non:42.42,
obs:"Offensive sentences contain slightly more Tamil words."
},

{
feature:"num_en",
off:47.55,
non:52.45,
obs:"Non-offensive sentences contain slightly more English tokens."
},

{
feature:"total_tokens",
off:54.87,
non:45.13,
obs:"Offensive comments tend to be slightly longer."
},

{
feature:"num_switches",
off:56.14,
non:43.86,
obs:"Offensive text shows more language switching."
},

{
feature:"switch_ratio",
off:55.37,
non:44.63,
obs:"Code-mixing behavior is slightly higher in offensive comments."
},

{
feature:"switch_density",
off:55.09,
non:44.91,
obs:"Frequent Tamil-English switching appears in abusive speech."
},

{
feature:"switch_beginning",
off:52.68,
non:47.32,
obs:"Language switching sometimes occurs at the start of offensive sentences."
},

{
feature:"switch_middle",
off:55.22,
non:44.78,
obs:"Most code switching occurs in the middle of sentences."
},

{
feature:"switch_end",
off:53.31,
non:46.69,
obs:"Language switching can also appear toward sentence endings."
},

{
feature:"ta_to_en_switch",
off:56.49,
non:43.51,
obs:"Switching from Tamil to English is slightly more common in offensive text."
},

{
feature:"en_to_ta_switch",
off:55.01,
non:44.99,
obs:"English to Tamil switching also occurs frequently in abusive comments."
},

{
feature:"char_length",
off:54.02,
non:45.98,
obs:"Offensive comments tend to be slightly longer in characters."
},

{
feature:"avg_word_length",
off:51.63,
non:48.37,
obs:"Average word length difference is minimal between classes."
},

{
feature:"exclamation_count",
off:59.84,
non:40.16,
obs:"Exclamation marks are frequently used to emphasize anger or insults."
},

{
feature:"question_count",
off:56.22,
non:43.78,
obs:"Question marks may indicate sarcastic or aggressive questioning."
},

{
feature:"punctuation_count",
off:57.14,
non:42.86,
obs:"Offensive comments often contain more punctuation marks."
},

{
feature:"uppercase_count",
off:58.77,
non:41.23,
obs:"Capital letters are sometimes used to express shouting or anger."
},

{
feature:"uppercase_ratio",
off:59.16,
non:40.84,
obs:"Uppercase emphasis is more common in offensive comments."
},

{
feature:"tamil_script_count",
off:56.21,
non:43.79,
obs:"Tamil script usage is slightly higher in offensive sentences."
},

{
feature:"tamil_script_ratio",
off:55.60,
non:44.40,
obs:"Tamil script dominates in many offensive code-mixed messages."
},

{
feature:"tamil_suffix_count",
off:57.93,
non:42.07,
obs:"Tamil morphological suffixes appear more in offensive speech."
},

{
feature:"elongated_english_words",
off:62.41,
non:37.59,
obs:"Users elongate English words to intensify insults."
},

{
feature:"english_target_pronouns",
off:58.14,
non:41.86,
obs:"Target pronouns like 'you' appear more in offensive comments."
},

{
feature:"emoji_count",
off:61.32,
non:38.68,
obs:"Emojis are often used to reinforce emotions in abusive messages."
},

{
feature:"repeated_char_words",
off:64.90,
non:35.10,
obs:"Repeated characters emphasize insults or sarcasm."
},

{
feature:"offensive_at_beginning",
off:74.55,
non:25.45,
obs:"Many offensive sentences start directly with abusive words."
},

{
feature:"offensive_at_end",
off:72.81,
non:27.19,
obs:"Offensive terms also frequently appear at the end of sentences."
},

{
feature:"consecutive_offensive_words",
off:76.93,
non:23.07,
obs:"Multiple abusive words often occur consecutively."
},

{
feature:"has_negation",
off:63.84,
non:36.16,
obs:"Negation is commonly used in offensive criticism."
},

{
feature:"is_imperative",
off:66.35,
non:33.65,
obs:"Imperative sentences often express commands or insults."
}

];

  return (
    <div className="feature-page">
      {/* 1. Consistent Navbar */}
      <nav className="navbar">
        <div className="logo" onClick={() => navigate('/')}>🛡️ Shield<span>AI</span></div>
        <div className="nav-links">
          <span className="nav-item" onClick={() => navigate("/")}>Home</span>
          <span className="nav-item" onClick={() => navigate("/dashboard")}>Portal</span>
          <span className="nav-item" onClick={() => navigate("/analyze")}>Analyze</span>
          <span className="nav-item active">Features</span>
        </div>
      </nav>

      <div className="content-container">
        <h2>Feature Correlation Analysis</h2>
        <p className="para">
          This insights table highlights how specific linguistic features influence the model's classification. 
        </p>

        <div className="table-container">
          <table className="feature-table">
            <thead>
              <tr>
                <th>Linguistic Feature</th>
                <th>Distribution (Off vs Non)</th>
                <th>Observation</th>
              </tr>
            </thead>
            <tbody>
              {features.map((f, i) => (
                <tr key={i}>
                  <td className="feature-name"><code>{f.feature}</code></td>
                  <td className="stats-cell">
                    <div className="bar-wrapper">
                      <div className="bar offensive-bar" style={{ width: `${f.off}%` }}>{f.off}%</div>
                      <div className="bar safe-bar" style={{ width: `${f.non}%` }}>{f.non}%</div>
                    </div>
                  </td>
                  <td className="obs-text">{f.obs}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default FeatureInsights;
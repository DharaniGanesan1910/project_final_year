import React from "react";
import "./Stylometry.css";

function Stylometry() {
  return (
    <div className="page-container">
      <h2>Stylometric Feature Extraction</h2>

      <ul className="feature-list">
        <li>Average word length</li>
        <li>Capital letter ratio</li>
        <li>Special character frequency</li>
        <li>Offensive word density</li>
        <li>Code-mixing index</li>
      </ul>

      <p className="note">
        These features are extracted from the dataset to assist classification.
      </p>
    </div>
  );
}

export default Stylometry;

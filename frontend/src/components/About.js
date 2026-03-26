import React from "react";
import { useNavigate } from "react-router-dom";
import "./About.css";

function About() {
  const navigate = useNavigate();

  return (
    <div className="about-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate("/")}>
        ← Back to Home
      </button>

      <h1 className="about-title">About the Project</h1>

      <p>
        The rapid growth of digital communication platforms has significantly increased 
        the presence of offensive online content, including harassment, hate speech, 
        cyberbullying, and abusive expressions. Traditional moderation approaches such 
        as manual review and rule-based filtering are often inefficient due to high costs, 
        limited scalability, and the complex, context-dependent nature of language.
      </p>

       <p>
        This challenge becomes even more difficult in <strong>code-mixed text</strong>, 
        where multiple languages such as Tamil and English are combined within a single 
        sentence. Unlike formal languages, code-mixed language does not follow any fixed 
        grammatical structure or consistent pattern. It often includes slang, abbreviations, 
        misspellings, transliterations, and symbolic expressions, making it difficult for 
        conventional models to accurately detect offensive content.
      </p>

      <h2>Our Approach</h2>
      <p>
        This project presents an automated offensive content detection system designed 
        specifically for code-mixed text. The system extracts linguistic features, classifies 
        content, and performs detailed sentence structure and pattern analysis.
      </p>

      <ul>
        <li>Classifies text as offensive or non-offensive based on the extracted feature sets of different linguistic components</li>

        <li>Detects sentence structure and pattern analysis</li>
      </ul>

      <h2>Structural Analysis of Tamil-English Code-Mixed Text</h2>
      <p>
        The system analyzes syntactic roles, clause boundaries, discourse markers, and 
        language-switching behavior to identify underlying sentence structures in 
        multilingual communication.
      </p>

      <h2>Key Innovation</h2>
      <p>
        This framework combines category-specific feature extraction with structural 
        pattern analysis to capture both localized offensive cues and global linguistic 
        patterns.
      </p>

      <ul>
        <li>Detects localized offensive expressions</li>
        <li>Displays sentence structure and pattern analysis</li>
      </ul>

      <h2>Impact</h2>
      <p>
        The system provides a scalable and accurate solution for moderating online content 
        in multilingual environments while offering deeper insights into code-mixed text 
        structures.
      </p>

      <h2>Vision</h2>
      <p>
        To build intelligent AI systems capable of understanding real-world multilingual 
        communication and creating safer digital environments.
      </p>

    </div>
  );
}

export default About;
import { useState } from "react";
import { uploadResume, getResumeATS } from "../services/api";
import "./ResumeOnly.css";

export default function ResumeOnly() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleGenerateATS = async () => {
    if (!file) {
      setError("Please upload your resume");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      // 1️⃣ Upload resume
      const uploaded = await uploadResume(file);

      // 2️⃣ Get ATS score
      const atsResult = await getResumeATS(uploaded.id);

      setResult(atsResult);
    } catch (err) {
      setError("Something went wrong. Try again.");
    }

    setLoading(false);
  };
console.log("Result:", result);
  return (
    <div className="resume-ats-container">
      <div className="card slide-in">
        
        <button className="back-btn" onClick={() => window.history.back()}>
  ← Back
</button>
        <h1 className="title">Get Your ATS Score</h1>
        
        <p className="subtitle">
          Upload your resume and get an AI-powered ATS score instantly
        </p>

        <div className="upload-box">
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        <button
          className="generate-btn"
          onClick={handleGenerateATS}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Generate ATS"}
        </button>

        {error && <p className="error">{error}</p>}

        {loading && (
          <div className="loader">
            <div className="spinner"></div>
            <p>Scanning resume with AI...</p>
          </div>
        )}

        {result && (
          <div className="result fade-in">
            <h2>Your ATS Score</h2>

            <div className="score-circle">
              <span>{result.ats_score}</span>
            </div>

            <h3>Detected Skills</h3>
            <div className="skills">
              {result.skills.map((skill, index) => (
                <span key={index} className="skill-chip">
                  {skill}
                </span>
              ))}
            </div>

            <h3>Suggestions</h3>
            <ul>
              {result.suggestions.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>

            {result.llm_feedback && typeof result.llm_feedback === "object" && (
  <div className="ai-feedback">

    {/* Summary */}
    {Array.isArray(result.llm_feedback.summary) && (
      <>
        <h4>Summary</h4>
        <ul>
          {result.llm_feedback.summary.map((point, i) => (
            <li key={i}>• {point}</li>
          ))}
        </ul>
      </>
    )}

    {/* Strengths */}
    {Array.isArray(result.llm_feedback.strengths) &&
      result.llm_feedback.strengths.length > 0 && (
        <>
          <h4>Strengths</h4>
          <ul>
            {result.llm_feedback.strengths.map((point, i) => (
              <li key={i}>✔ {point}</li>
            ))}
          </ul>
        </>
      )}

    {/* Improvements */}
    {Array.isArray(result.llm_feedback.improvements) &&
      result.llm_feedback.improvements.length > 0 && (
        <>
          <h4>Improvements</h4>
          <ul>
            {result.llm_feedback.improvements.map((point, i) => (
              <li key={i}>⚠ {point}</li>
            ))}
          </ul>
        </>
      )}

  </div>
)}

          </div>
        )}
      </div>
    </div>
  );
}

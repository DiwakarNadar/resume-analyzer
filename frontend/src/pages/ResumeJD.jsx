import { useState } from "react";
import { uploadResume, getResumeJdATS } from "../services/api";
import "./ResumeJD.css";

export default function ResumeJD() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleCompare = async () => {
    if (!file || !jd.trim()) {
      setError("Please upload resume and paste job description");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      // 1️⃣ Upload resume
      const uploaded = await uploadResume(file);

      // 2️⃣ Resume + JD ATS
      const atsResult = await getResumeJdATS(uploaded.id, jd);
      setResult(atsResult);
    } catch (err) {
      setError("Something went wrong. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="resume-jd-container">
      <div className="card slide-in">
        <button className="back-btn" onClick={() => window.history.back()}>
  ← Back
</button>
        <h1>Compare Resume with Job Description</h1>

        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <textarea
          placeholder="Paste Job Description here..."
          value={jd}
          onChange={(e) => setJd(e.target.value)}
          rows={6}
        />

        <button onClick={handleCompare} disabled={loading}>
          {loading ? "Analyzing..." : "Compare ATS"}
        </button>

        {error && <p className="error">{error}</p>}

        {loading && (
          <div className="loader">
            <div className="spinner"></div>
            <p>Analyzing resume vs JD...</p>
          </div>
        )}

        {result && (
          <div className="result fade-in">
            <h2>ATS Score</h2>
            <div className="score-circle">
              <span>{result.ats_score}</span>
            </div>

            {/* Matched Skills */}
            {result.matched_skills && (
              <>
                <h3>Matched Skills</h3>
                <div className="skills">
                  {result.matched_skills.map((s, i) => (
                    <span key={i} className="skill-chip success">
                      {s}
                    </span>
                  ))}
                </div>
              </>
            )}

            {/* Missing Skills */}
            {result.missing_skills && (
              <>
                <h3>Missing Skills</h3>
                <div className="skills">
                  {result.missing_skills.map((s, i) => (
                    <span key={i} className="skill-chip danger">
                      {s}
                    </span>
                  ))}
                </div>
              </>
            )}

            {/* AI Feedback */}
            {result.llm_feedback && (
              <div className="ai-feedback">
                <h3>AI Feedback</h3>

                {Array.isArray(result.llm_feedback.summary) && (
                  <ul>
                    {result.llm_feedback.summary.map((p, i) => (
                      <li key={i}>• {p}</li>
                    ))}
                  </ul>
                )}

                {Array.isArray(result.llm_feedback.strengths) &&
                  result.llm_feedback.strengths.length > 0 && (
                    <>
                      <h4>Strengths</h4>
                      <ul>
                        {result.llm_feedback.strengths.map((p, i) => (
                          <li key={i}>✔ {p}</li>
                        ))}
                      </ul>
                    </>
                  )}

                {Array.isArray(result.llm_feedback.improvements) &&
                  result.llm_feedback.improvements.length > 0 && (
                    <>
                      <h4>Improvements</h4>
                      <ul>
                        {result.llm_feedback.improvements.map((p, i) => (
                          <li key={i}>⚠ {p}</li>
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

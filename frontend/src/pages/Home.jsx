import ATSCard from "../components/ATSCard";
import "./Home.css";

export default function Home() {
  return (
    <div className="home-container">
      <h1 className="home-title">Resume Analyzer</h1>

      <div className="card-container">
        <ATSCard
  title="Get Your ATS Score"
  description="Upload your resume and get ATS score with AI insights"
  buttonText="Analyze Resume"
  route="/resume-only"
/>

<ATSCard
  title="Compare Resume with JD"
  description="Match your resume against a job description"
  buttonText="Compare with JD"
  route="/resume-jd"
/>

      </div>
    </div>
  );
}

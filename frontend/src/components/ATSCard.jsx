import { useNavigate } from "react-router-dom";
import "./ATSCard.css";

export default function ATSCard({ title, description, buttonText, route }) {
  const navigate = useNavigate();

  return (
    <div className="ats-card">
      <h2>{title}</h2>
      <p>{description}</p>
      <button onClick={() => navigate(route)}>{buttonText}</button>
    </div>
  );
}

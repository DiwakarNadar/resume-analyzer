import "./ATSScore.css";

export default function ATSScore({ score }) {
  return (
    <div className="score-ring">
      <svg width="120" height="120">
        <circle cx="60" cy="60" r="50" />
        <circle
          cx="60"
          cy="60"
          r="50"
          style={{
            strokeDasharray: 314,
            strokeDashoffset: 314 - (314 * score) / 100
          }}
        />
      </svg>
      <span>{score}</span>
    </div>
  );
}

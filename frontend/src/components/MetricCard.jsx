import "./MetricCard.css";

function MetricCard({ title, value, details }) {
  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <div className="metric-value">{value}</div>
      <ul className="metric-details">
        {details.map((detail, i) => (
          <li key={i}>{detail}</li>
        ))}
      </ul>
    </div>
  );
}

export default MetricCard;

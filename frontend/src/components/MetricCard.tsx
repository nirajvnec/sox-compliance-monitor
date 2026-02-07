import "./MetricCard.css";

interface MetricCardProps {
  title: string;
  value: string;
  details: string[];
}

function MetricCard({ title, value, details }: MetricCardProps) {
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

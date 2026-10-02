
import { useEffect, useState } from "react";

function FraudDetection() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/fraud-detection/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        Accept: "*/*",
      },
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Failed to load fraud detection data");
        }

        return response.json();
      })
      .then((result) => {
        setData(result);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="page">
        <h1>Fraud Detection</h1>
        <p>Loading fraud detection analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <h1>Fraud Detection</h1>
        <p style={{ color: "red" }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Fraud Detection</h1>
          <p>Claims fraud and anomaly monitoring</p>
        </div>

        <div
          style={{
            padding: "8px 16px",
            borderRadius: "20px",
            fontWeight: "600",
            background:
              data.risk_level === "High"
                ? "#fee2e2"
                : data.risk_level === "Medium"
                ? "#fef3c7"
                : "#dcfce7",
            color:
              data.risk_level === "High"
                ? "#b91c1c"
                : data.risk_level === "Medium"
                ? "#92400e"
                : "#166534",
          }}
        >
          {data.risk_level} Risk
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Fraud Score</h3>
          <p>{data.fraud_score}</p>
        </div>

        <div className="stat-card">
          <h3>Total Claims</h3>
          <p>{data.total_claims}</p>
        </div>

        <div className="stat-card">
          <h3>High Value Claims</h3>
          <p>{data.high_value_claims}</p>
        </div>

        <div className="stat-card">
          <h3>Duplicate Claims</h3>
          <p>{data.duplicate_claims}</p>
        </div>

        <div className="stat-card">
          <h3>Invalid Customers</h3>
          <p>{data.invalid_customers}</p>
        </div>

        <div className="stat-card">
          <h3>Invalid Policies</h3>
          <p>{data.invalid_policies}</p>
        </div>
      </div>

      <div className="card">
        <h2>Fraud Detection Findings</h2>

        {data.reasons && data.reasons.length > 0 ? (
          <ul>
            {data.reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        ) : (
          <p>No detection findings available.</p>
        )}
      </div>
    </div>
  );
}

export default FraudDetection;


import React, { useEffect, useState } from "react";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [investigatorAlerts, setInvestigatorAlerts] = useState([]);
  const [slaAlerts, setSlaAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadAlerts();
  }, []);

  async function loadAlerts() {
    const token = localStorage.getItem("token");

    try {
      const [
        alertsResponse,
        investigatorResponse,
        slaResponse,
      ] = await Promise.all([
        fetch("http://127.0.0.1:8000/alerts/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }),

        fetch("http://127.0.0.1:8000/alerts/investigator", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }),

        fetch("http://127.0.0.1:8000/alerts/sla-breach", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }),
      ]);

      if (!alertsResponse.ok) {
        throw new Error("Failed to load alerts");
      }

      if (!investigatorResponse.ok) {
        throw new Error("Failed to load investigator alerts");
      }

      if (!slaResponse.ok) {
        throw new Error("Failed to load SLA breach alerts");
      }

      const alertsData = await alertsResponse.json();
      const investigatorData = await investigatorResponse.json();
      const slaData = await slaResponse.json();

      setAlerts(alertsData);
      setInvestigatorAlerts(investigatorData);
      setSlaAlerts(slaData);
      setLoading(false);
    } catch (error) {
      console.error("Alerts error:", error);
      setError(error.message);
      setLoading(false);
    }
  }

  async function acknowledgeAlert(claimId) {
    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/alerts/acknowledge/INV-${claimId}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to acknowledge alert");
      }

      alert("Alert acknowledged successfully");

      loadAlerts();
    } catch (error) {
      console.error("Acknowledge error:", error);
      alert(error.message);
    }
  }

  if (loading) {
    return <h2>Loading Alerts...</h2>;
  }

  if (error) {
    return <h2>{error}</h2>;
  }

  return (
    <div>
      <h1>Alerts</h1>

      <p>High-risk claims and investigation alerts</p>

      {/* INVESTIGATOR ASSIGNMENTS */}
      <div className="analytics-card">
        <h2>Investigator Assignments</h2>

        {investigatorAlerts.length === 0 ? (
          <p>No claims currently assigned to investigators.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Claim ID</th>
                <th>Policy ID</th>
                <th>Claim Amount</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Assigned To</th>
                <th>Workflow Status</th>
                <th>Trigger</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {investigatorAlerts.map((alert) => (
                <tr key={alert.claim_id}>
                  <td>{alert.claim_id}</td>
                  <td>{alert.policy_id}</td>
                  <td>
                    ₹{Number(alert.claim_amount).toLocaleString("en-IN")}
                  </td>
                  <td>{alert.risk_score}</td>
                  <td>
                    <strong>{alert.risk_level}</strong>
                  </td>
                  <td>{alert.assigned_to}</td>
                  <td>{alert.workflow_status}</td>
                  <td>{alert.trigger}</td>

                  <td>
                    {alert.workflow_status === "Assigned" ? (
                      <button
                        onClick={() => acknowledgeAlert(alert.claim_id)}
                      >
                        Acknowledge
                      </button>
                    ) : (
                      <span>Acknowledged</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* SLA BREACH ESCALATIONS */}
      <div className="analytics-card">
        <h2>SLA Breach Escalations</h2>

        {slaAlerts.length === 0 ? (
          <p>No SLA breaches detected.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Claim ID</th>
                <th>Policy ID</th>
                <th>Claim Amount</th>
                <th>SLA Deadline</th>
                <th>Assigned To</th>
                <th>Workflow Status</th>
                <th>Trigger</th>
              </tr>
            </thead>

            <tbody>
              {slaAlerts.map((alert) => (
                <tr key={alert.claim_id}>
                  <td>{alert.claim_id}</td>
                  <td>{alert.policy_id}</td>
                  <td>
                    ₹{Number(alert.claim_amount).toLocaleString("en-IN")}
                  </td>
                  <td>
                    {new Date(alert.sla_deadline).toLocaleString("en-IN")}
                  </td>
                  <td>{alert.assigned_to}</td>
                  <td>{alert.workflow_status}</td>
                  <td>{alert.trigger}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* RISK ALERTS */}
      <div className="analytics-card">
        <h2>Risk Alerts</h2>

        {alerts.length === 0 ? (
          <h3>No alerts available</h3>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Claim ID</th>
                <th>Policy ID</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Alert</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {alerts.map((alert, index) => (
                <tr key={index}>
                  <td>{alert.claim_id}</td>
                  <td>{alert.policy_id}</td>
                  <td>{alert.risk_score}</td>
                  <td>
                    <strong>{alert.risk_level}</strong>
                  </td>
                  <td>{alert.alert}</td>
                  <td>{alert.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Alerts;
import { useState } from "react";

function InvestigatorWorkbench() {
  const [claimId, setClaimId] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleInvestigate = async (e) => {
    e.preventDefault();

    if (!claimId.trim()) {
      setError("Please enter a Claim ID.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/claims/${claimId.trim()}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? JSON.stringify(data.detail)
            : "Claim investigation failed"
        );
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to connect to the API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="investigate-page">
      <h1>Claim Investigation</h1>

      <p>Enter a claim ID to view claim details.</p>

      <form onSubmit={handleInvestigate}>
        <label htmlFor="claimId">Claim ID</label>

        <input
          id="claimId"
          type="text"
          placeholder="Example: CLM001"
          value={claimId}
          onChange={(e) => setClaimId(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Start Investigation"}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="investigation-result">
          <h2>Claim Details</h2>

          <p>
            <strong>Claim ID:</strong> {result.claim_id}
          </p>

          <p>
            <strong>Customer ID:</strong> {result.customer_id}
          </p>

          <p>
            <strong>Policy ID:</strong> {result.policy_id}
          </p>

          <p>
            <strong>Claim Amount:</strong>{" "}
            ₹{Number(result.claim_amount).toLocaleString("en-IN")}
          </p>

          <p>
            <strong>Status:</strong> {result.status}
          </p>
        </div>
      )}
    </div>
  );
}

export default InvestigatorWorkbench;


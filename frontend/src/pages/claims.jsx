import React, { useEffect, useState } from "react";

function Claims() {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("${import.meta.env.VITE_API_URL}/claims/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch claims");
        }

        return response.json();
      })
      .then((data) => {
        setClaims(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h1>Claims Management</h1>

      <p>Insurance Claims & Risk Analytics</p>

      {loading && <p>Loading claims...</p>}

      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="claims-container">

          <h2>Total Claims: {claims.length}</h2>

          <table className="claims-table">
            <thead>
              <tr>
                <th>Claim ID</th>
                <th>Customer ID</th>
                <th>Policy ID</th>
                <th>Claim Amount</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {claims.map((claim) => (
                <tr key={claim.claim_id}>
                  <td>{claim.claim_id}</td>

                  <td>{claim.customer_id}</td>

                  <td>{claim.policy_id}</td>

                  <td>
                    ₹{Number(claim.claim_amount).toLocaleString("en-IN")}
                  </td>

                  <td>{claim.status}</td>
                </tr>
              ))}
            </tbody>
          </table>

        </div>
      )}
    </div>
  );
}

export default Claims;

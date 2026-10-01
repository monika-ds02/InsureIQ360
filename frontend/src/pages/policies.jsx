import { useEffect, useState } from "react";

function Policies() {
  const [policies, setPolicies] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("http://127.0.0.1:8000/policies/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("API request failed");
        }

        return response.json();
      })
      .then((data) => {
        setPolicies(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load policies");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <h2>Loading policies...</h2>;
  }

  if (error) {
    return <h2>{error}</h2>;
  }

  return (
    <div>
      <h1>Policy Management</h1>

      <p>Insurance Policies</p>

      <h2>Total Policies: {policies.length}</h2>

      <table className="claims-table">
        <thead>
          <tr>
            <th>Policy ID</th>
            <th>Customer ID</th>
            <th>Policy Type</th>
            <th>Premium</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {policies.map((policy) => (
            <tr key={policy.policy_id}>
              <td>{policy.policy_id}</td>

              <td>{policy.customer_id}</td>

              <td>{policy.policy_type}</td>

              <td>
                ₹{Number(policy.premium).toLocaleString("en-IN")}
              </td>

              <td>{policy.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Policies;
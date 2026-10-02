import React, { useEffect, useState } from "react";

function ReserveForecast() {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("${import.meta.env.VITE_API_URL}/reserve-forecast/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load reserve forecast");
        }

        return response.json();
      })
      .then((data) => {
        setForecast(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Reserve forecast error:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <h2>Loading Reserve Forecast...</h2>;
  }

  if (error) {
    return <h2>{error}</h2>;
  }

  const totalReserve = forecast.reduce(
    (sum, item) => sum + Number(item.forecast_amount || 0),
    0
  );

  const totalClaims = forecast.reduce(
    (sum, item) => sum + Number(item.expected_claims || 0),
    0
  );

  const predictedReserve =
    forecast.length > 0
      ? Number(forecast[0].forecast_amount || 0)
      : 0;

  return (
    <div>
      <h1>Reserve Forecast</h1>

      <p>Predicted claim reserve and financial exposure</p>

      <div className="cards">
        <div className="card">
          <h2>Total Reserve</h2>
          <h3>₹{totalReserve.toLocaleString("en-IN")}</h3>
        </div>

        <div className="card">
          <h2>Predicted Reserve</h2>
          <h3>₹{predictedReserve.toLocaleString("en-IN")}</h3>
        </div>

        <div className="card">
          <h2>Claims Forecast</h2>
          <h3>{totalClaims.toLocaleString("en-IN")}</h3>
        </div>
      </div>

      <h2>Forecast Details</h2>

      <table>
        <thead>
          <tr>
            <th>Period</th>
            <th>Expected Claims</th>
            <th>Forecast Amount</th>
          </tr>
        </thead>

        <tbody>
          {forecast.map((item, index) => (
            <tr key={index}>
              <td>{item.period}</td>
              <td>{item.expected_claims}</td>
              <td>
                ₹{Number(item.forecast_amount).toLocaleString("en-IN")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ReserveForecast;

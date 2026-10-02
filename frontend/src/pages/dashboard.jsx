import React, { useEffect, useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("${import.meta.env.VITE_API_URL}/claims/dashboard", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Dashboard API failed");
        }

        return response.json();
      })
      .then((data) => {
        setDashboard(data);
      })
      .catch((error) => {
        console.error("Dashboard error:", error);
        setError(error.message);
      });
  }, []);

  if (error) {
    return <h2>{error}</h2>;
  }

  if (!dashboard) {
    return <h2>Loading Dashboard...</h2>;
  }

  const summary = dashboard.summary || {};
  const customerSummary = dashboard.customer_summary || [];
  const policySummary = dashboard.policy_summary || [];

  return (
    <div>
      <h1>Claims Command Center</h1>

      {/* KPI CARDS */}
      <div className="dashboard-cards">

        <div className="card">
          <h3>Total Claims</h3>
          <p>{summary.total_claims ?? 0}</p>
        </div>

        <div className="card">
          <h3>Pending Claims</h3>
          <p>{summary.pending_claims ?? 0}</p>
        </div>

        <div className="card">
          <h3>Approved Claims</h3>
          <p>{summary.approved_claims ?? 0}</p>
        </div>

        <div className="card">
          <h3>Total Claim Amount</h3>
          <p>
            ₹{Number(summary.total_claim_amount ?? 0).toLocaleString("en-IN")}
          </p>
        </div>

      </div>

      {/* CLAIMS BY CUSTOMER */}
      <div className="analytics-card">
        <h2>Claims by Customer</h2>

        <ResponsiveContainer width="100%" height={350}>
          <BarChart
            data={customerSummary}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 20,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="customer_id"
              label={{
                value: "Customer",
                position: "insideBottom",
                offset: -10,
              }}
            />

            <YAxis
              label={{
                value: "Number of Claims",
                angle: -90,
                position: "insideLeft",
              }}
            />

            <Tooltip />

            <Bar
              dataKey="claim_count"
              name="Claims"
              barSize={60}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* CLAIM AMOUNT BY CUSTOMER */}
      <div className="analytics-card">
        <h2>Claim Amount by Customer</h2>

        <ResponsiveContainer width="100%" height={350}>
          <BarChart
            data={customerSummary}
            margin={{
              top: 20,
              right: 30,
              left: 30,
              bottom: 20,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="customer_id"
              label={{
                value: "Customer",
                position: "insideBottom",
                offset: -10,
              }}
            />

            <YAxis
              label={{
                value: "Claim Amount (₹)",
                angle: -90,
                position: "insideLeft",
              }}
            />

            <Tooltip
              formatter={(value) =>
                `₹${Number(value).toLocaleString("en-IN")}`
              }
            />

            <Bar
              dataKey="total_claim_amount"
              name="Claim Amount"
              barSize={60}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* CLAIMS BY POLICY */}
      <div className="analytics-card">
        <h2>Claims by Policy</h2>

        <ResponsiveContainer width="100%" height={350}>
          <BarChart
            data={policySummary}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 20,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="policy_id"
              label={{
                value: "Policy",
                position: "insideBottom",
                offset: -10,
              }}
            />

            <YAxis
              label={{
                value: "Number of Claims",
                angle: -90,
                position: "insideLeft",
              }}
            />

            <Tooltip />

            <Bar
              dataKey="claim_count"
              name="Claims"
              barSize={60}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

export default Dashboard;

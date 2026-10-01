import { useEffect, useState } from "react";

function LiveEvents() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  async function fetchEvents() {
    try {
      const token = localStorage.getItem("token");

      const response = await fetch("http://127.0.0.1:8000/events/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch events");
      }

      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.error("Kafka events error:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEvents();

    const interval = setInterval(fetchEvents, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Live Kafka Events</h1>
          <p>Real-time claim events received through Kafka</p>
        </div>

        <div className="live-indicator">
          🟢 Live
        </div>
      </div>

      {loading ? (
        <p>Loading events...</p>
      ) : events.length === 0 ? (
        <p>No Kafka events available.</p>
      ) : (
        <div className="table-card">
          <table>
            <thead>
              <tr>
                <th>Event ID</th>
                <th>Claim ID</th>
                <th>Event Type</th>
                <th>Customer</th>
                <th>Policy</th>
                <th>Claim Amount</th>
                <th>Status</th>
                <th>Received At</th>
              </tr>
            </thead>

            <tbody>
              {events.map((event) => (
                <tr key={event.event_id}>
                  <td>{event.event_id}</td>
                  <td>{event.claim_id}</td>
                  <td>{event.event_type}</td>
                  <td>{event.customer_id || "-"}</td>
                  <td>{event.policy_id || "-"}</td>
                  <td>
                    ₹{Number(event.claim_amount || 0).toLocaleString()}
                  </td>
                  <td>
                    <span className="status-badge">
                      {event.status}
                    </span>
                  </td>
                  <td>
                    {new Date(event.received_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default LiveEvents;
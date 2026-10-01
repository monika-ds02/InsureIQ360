import React from "react";

import React from "react";
function Sidebar({ setActivePage }) {
  return (
    <div className="sidebar">

      <h2>InsureIQ 360</h2>

      <button onClick={() => setActivePage("dashboard")}>
        Dashboard
      </button>

      <button onClick={() => setActivePage("claims")}>
        Claims
      </button>

      <button onClick={() => setActivePage("policies")}>
        Policies
      </button>

      <button onClick={() => setActivePage("investigator")}>
        Investigator Workbench
      </button>

      <button onClick={() => setActivePage("reserve")}>
        Reserve Forecast
      </button>

      <button onClick={() => setActivePage("alerts")}>
        Alerts
      </button>

    </div>
  );
}

export default Sidebar;
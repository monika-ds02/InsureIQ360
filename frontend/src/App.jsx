
import { useState } from "react";

import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Claims from "./pages/claims";
import Policies from "./pages/Policies";
import InvestigatorWorkbench from "./pages/InvestigatorWorkbench";
import ReserveForecast from "./pages/ReserveForecast";
import Alerts from "./pages/Alerts";
import Login from "./pages/Login";
import DataQuality from "./pages/DataQuality";
import RiskAnalytics from "./pages/RiskAnalytics";
import FraudDetection from "./pages/FraudDetection";

import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const [activePage, setActivePage] = useState("Dashboard");

  function handleLogin() {
    setIsLoggedIn(true);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
  }

  function renderPage() {
    switch (activePage) {
      case "Dashboard":
        return <Dashboard />;

      case "Claims":
        return <Claims />;

      case "Policies":
        return <Policies />;

      case "Investigator Workbench":
        return <InvestigatorWorkbench />;

      case "Reserve Forecast":
        return <ReserveForecast />;

      case "Alerts":
        return <Alerts />;

      case "Data Quality":
        return <DataQuality />;

      case "Risk Analytics":
        return <RiskAnalytics />;

      case "Fraud Detection":
        return <FraudDetection />;

      default:
        return <Dashboard />;
    }
  }

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <section className="main">
        <header className="topbar">
          <div>
            <h2>InsureIQ 360</h2>
            <p>Insurance Claims & Risk Analytics</p>
          </div>

          <div className="status">
            🟢 API Connected

            <button onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        <main className="content">
          {renderPage()}
        </main>
      </section>
    </div>
  );
}

export default App;
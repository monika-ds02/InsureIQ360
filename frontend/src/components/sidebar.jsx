
function Sidebar({ activePage, setActivePage }) {
  const menuItems = [
    "Dashboard",
    "Claims",
    "Policies",
    "Investigator Workbench",
    "Reserve Forecast",
    "Alerts",
    "Live Kafka Events",
    "Data Quality",
    "Risk Analytics",
    "Fraud Detection",
  ];

  return (
    <aside className="sidebar">
      <div className="logo">
        <h1>InsureIQ 360</h1>
        <p>Insurance Intelligence</p>
      </div>

      <nav>
        {menuItems.map((item) => (
          <button
            key={item}
            className={
              activePage === item
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setActivePage(item)}
          >
            {item}
          </button>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;

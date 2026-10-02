import { useEffect, useState } from "react";


function RiskAnalytics() {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);


  async function fetchRiskAnalytics() {

    try {

      const token = localStorage.getItem("token");


      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/risk-analytics/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );


      if (!response.ok) {
        throw new Error("Failed to fetch risk analytics");
      }


      const result = await response.json();

      setData(result);


    } catch(error) {

      console.error(
        "Risk analytics error:",
        error
      );

    } finally {

      setLoading(false);

    }

  }



  useEffect(() => {

    fetchRiskAnalytics();

  }, []);




  if (loading) {

    return (
      <p>
        Loading Risk Analytics...
      </p>
    );

  }




  return (

    <div>


      <div className="page-header">

        <div>

          <h1>
            Risk Analytics
          </h1>

          <p>
            Claims risk monitoring and analysis
          </p>

        </div>


        <div className="live-indicator">

          🟢 {data?.risk_level} Risk

        </div>


      </div>




      <div className="cards">


        <div className="card">

          <h3>
            Total Claims
          </h3>

          <h2>
            {data.total_claims}
          </h2>

        </div>



        <div className="card">

          <h3>
            Total Claim Amount
          </h3>

          <h2>
            ₹{data.total_claim_amount.toLocaleString()}
          </h2>

        </div>



        <div className="card">

          <h3>
            Average Claim
          </h3>

          <h2>
            ₹{data.average_claim_amount.toLocaleString()}
          </h2>

        </div>



        <div className="card">

          <h3>
            Pending Claims
          </h3>

          <h2>
            {data.pending_claims}
          </h2>

        </div>


      </div>





      <div className="table-card">


        <h2>
          High Value Claims
        </h2>


        <table>

          <thead>

            <tr>

              <th>
                Claim ID
              </th>

              <th>
                Amount
              </th>

              <th>
                Status
              </th>

            </tr>

          </thead>


          <tbody>


          {
            data.high_value_claims.map(
              (claim)=> (

                <tr key={claim.claim_id}>

                  <td>
                    {claim.claim_id}
                  </td>

                  <td>
                    ₹{claim.amount.toLocaleString()}
                  </td>

                  <td>
                    <span className="status-badge">
                      {claim.status}
                    </span>
                  </td>

                </tr>

              )
            )
          }


          </tbody>


        </table>


      </div>


    </div>

  );

}


export default RiskAnalytics;


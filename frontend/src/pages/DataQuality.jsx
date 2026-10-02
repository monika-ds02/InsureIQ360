import { useEffect, useState } from "react";

function DataQuality() {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);


  async function fetchQuality() {

    try {

      const token = localStorage.getItem("token");


      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/data-quality/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );


      if (!response.ok) {
        throw new Error("Failed to load data quality");
      }


      const result = await response.json();

      setData(result);


    } catch (error) {

      console.error(
        "Data quality error:",
        error
      );

    } finally {

      setLoading(false);

    }

  }


  useEffect(() => {

    fetchQuality();

  }, []);



  if (loading) {

    return (
      <div>
        <h1>Data Quality</h1>
        <p>Loading...</p>
      </div>
    );

  }



  if (!data) {

    return (
      <div>
        <h1>Data Quality</h1>
        <p>Unable to load quality data</p>
      </div>
    );

  }



  return (

    <div>

      <div className="page-header">

        <div>

          <h1>
            Data Quality
          </h1>

          <p>
            Claims data validation and health monitoring
          </p>

        </div>


        <div className="live-indicator">
          🟢 Healthy
        </div>

      </div>



      <div className="cards">


        <div className="card">

          <h3>
            Data Quality Score
          </h3>

          <h2>
            {data.quality_score}%
          </h2>

        </div>



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
            Checks Passed
          </h3>

          <h2>
            {data.passed_checks}/{data.total_checks}
          </h2>

        </div>



        <div className="card">

          <h3>
            Failed Checks
          </h3>

          <h2>
            {data.failed_checks}
          </h2>

        </div>


      </div>



      <div className="table-card">

        <h2>
          Validation Results
        </h2>


        <table>

          <thead>

            <tr>
              <th>Check</th>
              <th>Status</th>
            </tr>

          </thead>


          <tbody>


            <tr>
              <td>Duplicate Claims</td>
              <td>✅ {data.duplicate_claims}</td>
            </tr>


            <tr>
              <td>Invalid Customers</td>
              <td>✅ {data.invalid_customers}</td>
            </tr>


            <tr>
              <td>Invalid Policies</td>
              <td>✅ {data.invalid_policies}</td>
            </tr>


            <tr>
              <td>Invalid Amounts</td>
              <td>✅ {data.invalid_amounts}</td>
            </tr>


          </tbody>


        </table>


      </div>



      <div className="table-card">

        <h2>
          Claim Status Values
        </h2>


        <ul>

          {data.statuses.map(
            (status) => (
              <li key={status}>
                {status}
              </li>
            )
          )}

        </ul>


      </div>


    </div>

  );

}


export default DataQuality;


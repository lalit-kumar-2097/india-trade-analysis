
// import React, { useState } from 'react';
// import ForecastControls from './ForecastControls';
// import ForecastTable from './ForecastTable';
// import ValidationMetrics from './ValidationMetrics';
// import ValidationTable from './ValidationTable';
// import ForecastChart from './ForecastChart';
// import ValidationChart from './ValidationChart';
// import LoadingSpinner from './LoadingSpinner';



// export default function ForecastDashboard() {
//   const [hsCode, setHsCode] = useState('');
//   const [model, setModel] = useState('prophet');
//   const [validation, setValidation] = useState(false);

//   const [forecastData, setForecastData] = useState([]);  // Start with empty array
//   const [metrics, setMetrics] = useState(null);

//   const [loading, setLoading] = useState(false);  // Optional: Add loading state if needed

//   const fetchForecast = async () => {
//     try {
//       setLoading(true);  // Set loading state if you want to show a spinner
//       setForecastData([]);   // Clear as array, not null
//       setMetrics(null);

//       const response = await fetch('http://192.168.0.103:8000/api/forecast/', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           hs_code: hsCode,
//           model: model,
//           validation: validation
//         }),
//       });

//       const data = await response.json();

//       if (validation && data.mae) {
//         setMetrics({ mae: data.mae, rmse: data.rmse });
//         setForecastData({
//           predictions: data.predictions,
//           actuals: data.actuals
//         });
//       } else {
//         setForecastData(data);
//       }
//     } catch (error) {
//       console.error('Error fetching forecast:', error);
//     } finally {
//       setLoading(false);  // Reset loading state
//     }
//   };

//   return (
    
//       <div className="p-4 max-w-5xl mx-auto">
//       <h1 className="text-2xl font-bold mb-4">Forecast Dashboard</h1>

//       <ForecastControls
//         hsCode={hsCode}
//         setHsCode={setHsCode}
//         model={model}
//         setModel={setModel}
//         validation={validation}
//         setValidation={setValidation}
//         onFetch={fetchForecast} />

//       <ValidationMetrics metrics={metrics} />

//       {loading ? (
//         <LoadingSpinner />
//       ) : (
//         <>
//           {validation && forecastData && forecastData.predictions ? (
//             <>
//               <ValidationChart
//                 actuals={forecastData.actuals}
//                 predictions={forecastData.predictions} />
//               <ValidationTable
//                 actuals={forecastData.actuals}
//                 predictions={forecastData.predictions} />
//             </>
//           ) : (
//             <>
//               <ForecastChart data={forecastData} />
//               <ForecastTable data={forecastData} />
//             </>
//           )}
//         </>
//       )}

//     </div>
//   );
// }


import React, { useState } from 'react';
import ForecastControls from './ForecastControls';
import ForecastTable from './ForecastTable';
import ValidationMetrics from './ValidationMetrics';
import ValidationTable from './ValidationTable';
import ForecastChart from './ForecastChart';
import ValidationChart from './ValidationChart';
import LoadingSpinner from './LoadingSpinner';
import CommodityDropdown from './CommodityDropdown';
import Navbar from './Navbar';



export default function ForecastDashboard() {
  const [hsCode, setHsCode] = useState('');
  const [model, setModel] = useState('prophet');
  const [validation, setValidation] = useState(false);

  const [forecastData, setForecastData] = useState([]);    // Always keep as array (for non-validation)
  const [metrics, setMetrics] = useState(null);
  const [commodityName, setCommodityName] = useState('');   // New: To store commodity name
  const [loading, setLoading] = useState(false);

  const fetchForecast = async () => {
    try {
      setLoading(true);
      setForecastData([]);
      setMetrics(null);
      setCommodityName('');

      const response = await fetch('http://192.168.0.103:8000/api/forecast/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          hs_code: hsCode,
          model: model,
          validation: validation
        }),
      });

      const data = await response.json();

      if (validation && data.mae) {
        // Validation mode
        setMetrics({ mae: data.mae, rmse: data.rmse });
        setForecastData({
          predictions: data.predictions,
          actuals: data.actuals
        });
        setCommodityName(data.commodity_name || '');
      } else {
        // Regular forecast mode
        setForecastData(data.forecast || []);    // << Key Change
        setCommodityName(data.commodity_name || '');
      }

    } catch (error) {
      console.error('Error fetching forecast:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <Navbar />

      <h1 className="text-2xl font-bold mb-4">Forecast Dashboard</h1>

      <ForecastControls
        hsCode={hsCode}
        setHsCode={setHsCode}
        model={model}
        setModel={setModel}
        validation={validation}
        setValidation={setValidation}
        onFetch={fetchForecast}
      />

      {commodityName && (
        <h2 className="text-xl font-semibold mb-2">
          Commodity: {commodityName}
        </h2>
      )}

      <ValidationMetrics metrics={metrics} />

      {loading ? (
        <LoadingSpinner />
      ) : (
        <>
          {validation && forecastData?.predictions ? (
            <>
              <ValidationChart
                actuals={forecastData.actuals}
                predictions={forecastData.predictions}
              />
              <ValidationTable
                actuals={forecastData.actuals}
                predictions={forecastData.predictions}
              />
            </>
          ) : (
            <>
              <ForecastChart data={forecastData} />
              <ForecastTable data={forecastData} />
            </>
          )}
        </>
      )}
    </div>
  );
}
// This component serves as the main dashboard for trade forecasting.
// It includes controls for selecting HS codes and models, displays validation metrics,   
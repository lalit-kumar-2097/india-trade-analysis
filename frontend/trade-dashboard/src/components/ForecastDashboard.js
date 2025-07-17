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

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export default function ForecastDashboard() {
  const [hsCode, setHsCode] = useState('');
  const [model, setModel] = useState('prophet');
  const [validation, setValidation] = useState(false);

  const [forecastData, setForecastData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [commodityName, setCommodityName] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchForecast = async () => {
    try {
      setLoading(true);
      setForecastData([]);
      setMetrics(null);
      setCommodityName('');

      const response = await fetch(`${API_BASE_URL}/forecast/`, {
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
        setMetrics({ mae: data.mae, rmse: data.rmse });
        setForecastData({
          predictions: data.predictions,
          actuals: data.actuals
        });
        setCommodityName(data.commodity_name || '');
      } else {
        setForecastData(data.forecast || []);    
        setCommodityName(data.commodity_name || '');
      }

    } catch (error) {
      console.error('Error fetching forecast:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-5xl mx-auto container">      

      <h1 className="text-2xl font-bold mb-4">Forecast Dashboard</h1>
          

      {/* Main Control Panel */}
      <ForecastControls
        hsCode={hsCode}
        setHsCode={setHsCode}
        model={model}
        setModel={setModel}
        validation={validation}
        setValidation={setValidation}
        onFetch={fetchForecast}
      />

      <ValidationMetrics metrics={metrics} />

      {/* Show selected commodity name */}
      {commodityName && (
        <h2 className="text-xl font-semibold mb-2 text-blue-600">
          Commodity: {commodityName}
        </h2>
      )}

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

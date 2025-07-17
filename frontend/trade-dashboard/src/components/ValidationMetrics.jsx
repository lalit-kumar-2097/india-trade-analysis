import React from 'react';

export default function ValidationMetrics({ metrics }) {
  if (!metrics) return null;

  return (
    <div className="mt-4 bg-yellow-100 p-4 rounded-lg">
      <h3 className="font-bold mb-2">Validation Metrics</h3>
      <p>MAE: {metrics.mae}</p>
      <p>RMSE: {metrics.rmse}</p>
    </div>
  );
}

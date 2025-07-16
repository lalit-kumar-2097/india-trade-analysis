// import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// export default function ValidationChart({ actuals, predictions }) {
//   if (!actuals || !predictions) return <p>No validation data available.</p>;

//   const chartData = actuals.map((actual, index) => ({
//     point: `Point ${index + 1}`,
//     actual: actual,
//     predicted: predictions[index]
//   }));

//   return (
//     <div className="my-6">
//       <h2 className="text-lg font-semibold mb-2">Validation Chart</h2>
//       <ResponsiveContainer width="100%" height={300}>
//         <LineChart data={chartData}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis dataKey="point" />
//           <YAxis />
//           <Tooltip />
//           <Legend />
//           <Line type="monotone" dataKey="actual" stroke="#ff7300" name="Actual" />
//           <Line type="monotone" dataKey="predicted" stroke="#8884d8" name="Predicted" />
//         </LineChart>
//       </ResponsiveContainer>
//     </div>
//   );
// }
// // This component visualizes the validation results by comparing actual and predicted values.
// // It uses Recharts to create a line chart that displays both actual and predicted values over time.
// // The chart helps in understanding the accuracy of the predictions made by the forecasting model.  



import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function ValidationChart({ actuals, predictions }) {
  const safeActuals = Array.isArray(actuals) ? actuals : [];
  const safePredictions = Array.isArray(predictions) ? predictions : [];

  if (safeActuals.length === 0 || safePredictions.length === 0) {
    return <p className="text-center text-gray-500">No validation data available.</p>;
  }

  const chartData = safeActuals.map((actual, index) => ({
    point: `Point ${index + 1}`,
    actual: actual,
    predicted: safePredictions[index]
  }));

  const formatInMillions = (value) => `${(value / 1_000_000).toFixed(2)}M`;

  return (
    <div className="my-6">
      <h2 className="text-lg font-semibold mb-2">Validation Chart</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="point" />
          <YAxis tickFormatter={formatInMillions} />
          <Tooltip formatter={(value) => formatInMillions(value)} />
          <Legend />
          <Line type="monotone" dataKey="actual" stroke="#ff7300" name="Actual" dot={false} />
          <Line type="monotone" dataKey="predicted" stroke="#8884d8" name="Predicted" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

// import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// export default function ForecastChart({ data }) {
//   if (!data || data.length === 0) return <p>No forecast data available.</p>;

//   return (
//     <div className="my-6">
//       <h2 className="text-lg font-semibold mb-2">Forecast Chart</h2>
//       <ResponsiveContainer width="100%" height={300}>
//         <LineChart data={data}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis dataKey="ds" />
//           <YAxis />
//           <Tooltip />
//           <Legend />
//           <Line type="monotone" dataKey="yhat" stroke="#8884d8" name="Prediction" />
//           <Line type="monotone" dataKey="yhat_lower" stroke="#82ca9d" name="Lower Bound" />
//           <Line type="monotone" dataKey="yhat_upper" stroke="#ff7300" name="Upper Bound" />
//         </LineChart>
//       </ResponsiveContainer>
//     </div>
//   );
// }



import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function ForecastChart({ data }) {
  const safeData = Array.isArray(data) ? data : [];

  if (safeData.length === 0) return <p className="text-center text-gray-500">No forecast data available.</p>;

  const formatInMillions = (value) => `${(value / 1_000_000).toFixed(2)}M`;

  return (
    <div className="my-6">
      <h2 className="text-lg font-semibold mb-2">Forecast Chart</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={safeData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ds" />
          <YAxis tickFormatter={formatInMillions} />
          <Tooltip formatter={(value) => formatInMillions(value)} />
          <Legend />
          <Line type="monotone" dataKey="yhat" stroke="#8884d8" name="Prediction" dot={false} />
          <Line type="monotone" dataKey="yhat_lower" stroke="#82ca9d" name="Lower Bound" dot={false} />
          <Line type="monotone" dataKey="yhat_upper" stroke="#ff7300" name="Upper Bound" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

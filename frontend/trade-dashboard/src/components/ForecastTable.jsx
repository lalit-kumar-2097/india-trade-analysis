// import React from 'react';

// export default function ForecastTable({ data }) {
//   if (!data || data.length === 0) return null;

//   return (
//     <table className="w-full mt-4 border" border="1" cellPadding="8">
//       <thead>
//         <tr>
//           <th>Date</th>
//           <th>Prediction (yhat)</th>
//           <th>Lower Bound</th>
//           <th>Upper Bound</th>
//         </tr>
//       </thead>
//       <tbody>
//         {data.map((item, idx) => (
//           <tr key={idx}>
//             <td>{item.ds}</td>
//             <td>{item.yhat}</td>
//             <td>{item.yhat_lower}</td>
//             <td>{item.yhat_upper}</td>
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// }



import React from 'react';

export default function ForecastTable({ data }) {
  const formatToMillions = (num) => {
    if (isNaN(num)) return '-';
    return (num / 1_000_000).toFixed(2) + ' M';
  };

  return (
    <div className="overflow-x-auto mt-6">
      <table className="min-w-full border border-gray-300 text-center" border="1" cellPadding="8">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">Date</th>
            <th className="border p-2">Prediction (yhat)</th>
            <th className="border p-2">Lower Bound</th>
            <th className="border p-2">Upper Bound</th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(data) && data.map((row, index) => (
            <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              <td className="border p-2">{row.ds}</td>
              <td className="border p-2">{formatToMillions(row.yhat)}</td>
              <td className="border p-2">{formatToMillions(row.yhat_lower)}</td>
              <td className="border p-2">{formatToMillions(row.yhat_upper)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

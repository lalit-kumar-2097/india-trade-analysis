// import React from 'react';

// const ValidationTable = ({ actuals, predictions }) => {
//   if (!actuals || !predictions || actuals.length !== predictions.length) {
//     return <p>No validation data available.</p>;
//   }

//   return (
//     <div>
//       <h3>Validation Results</h3>
//       <table border="1" cellPadding="8">
//         <thead>
//           <tr>
//             <th>Point</th>
//             <th>Predicted</th>
//             <th>Actual</th>
//             <th>Error</th>
//           </tr>
//         </thead>
//         <tbody>
//           {predictions.map((pred, idx) => (
//             <tr key={idx}>
//               <td>Point {idx + 1}</td>
//               <td>{pred.toFixed(2)}</td>
//               <td>{actuals[idx].toFixed(2)}</td>
//               <td>{(Math.abs(pred - actuals[idx])).toFixed(2)}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// };

// export default ValidationTable;


import React from 'react';

export default function ValidationTable({ actuals, predictions }) {
  const formatToMillions = (num) => {
    if (isNaN(num)) return '-';
    return (num / 1_000_000).toFixed(2) + ' M';
  };

  return (
    <div className="overflow-x-auto mt-6">
      <table className="min-w-full border border-gray-300 text-center" border="1" cellPadding="8">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">Point</th>
            <th className="border p-2">Predicted</th>
            <th className="border p-2">Actual</th>
            <th className="border p-2">Error</th>
          </tr>
        </thead>
        <tbody>
          {actuals.map((actual, index) => {
            const predicted = predictions[index];
            const error = Math.abs(predicted - actual);

            return (
              <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="border p-2">Point {index + 1}</td>
                <td className="border p-2">{formatToMillions(predicted)}</td>
                <td className="border p-2">{formatToMillions(actual)}</td>
                <td className="border p-2">{formatToMillions(error)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

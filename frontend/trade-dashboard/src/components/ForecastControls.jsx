// import React from 'react';

// export default function ForecastControls({ hsCode, setHsCode, model, setModel, validation, setValidation, onFetch }) {
//   return (
//     <div className="p-4 bg-gray-100 rounded-lg">
//       <input
//         type="text"
//         placeholder="HS Code"
//         value={hsCode}
//         onChange={(e) => setHsCode(e.target.value)}
//         className="p-2 border rounded mr-2"
//       />
//       <select value={model} onChange={(e) => setModel(e.target.value)} className="p-2 border rounded mr-2">
//         <option value="prophet">Prophet</option>
//         <option value="sarima">SARIMA</option>
//         <option value="xgboost">XGBoost</option>
//       </select>
//       <label className="mr-2">
//         <input type="checkbox" checked={validation} onChange={(e) => setValidation(e.target.checked)} /> Validation Mode
//       </label>
//       <button onClick={onFetch} className="bg-blue-500 text-white px-4 py-2 rounded">
//         Get Forecast
//       </button>
//     </div>
//   );
// }


import CommodityDropdown from './CommodityDropdown';

export default function ForecastControls({
  hsCode,
  setHsCode,
  model,
  setModel,
  validation,
  setValidation,
  onFetch
}) {
  return (
    <div className="mb-4">
      <label className="block mb-2 font-semibold">Commodity / HS Code:</label>

      <CommodityDropdown onSelect={option => setHsCode(option ? option.value : '')} />


      <select value={model} onChange={(e) => setModel(e.target.value)} className="p-2 border rounded mr-2">
         <option value="prophet">Prophet</option>
         <option value="sarima">SARIMA</option>
         <option value="xgboost">XGBoost</option>
       </select>
       <label className="mr-2">
         <input type="checkbox" checked={validation} onChange={(e) => setValidation(e.target.checked)} /> Validation Mode
      </label>
       <button onClick={onFetch} className="bg-blue-500 text-white px-4 py-2 rounded">
        Get Forecast
      </button>
    </div>
  );
}
// This component provides controls for the forecast dashboard.
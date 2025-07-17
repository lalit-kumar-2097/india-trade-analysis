// import AsyncSelect from 'react-select/async';

// const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// export default function CommodityDropdown({ onSelect }) {
//   const loadOptions = async (inputValue) => {
//     if (!inputValue) return [];

//     const response = await fetch(`${API_BASE_URL}/commodities/?search=${inputValue}`);
//     const data = await response.json();

//     return data.map(item => ({
//       label: `${item.commodity} (${item.hs_code})`,
//       value: item.hs_code
//     }));
//   };

//   return (
//     <div className="my-4">
//       <AsyncSelect
//         cacheOptions
//         loadOptions={loadOptions}
//         defaultOptions={false}
//         placeholder="Type to search commodity..."
//         onChange={onSelect}
//         isClearable={true}  // 🔑 Enables clearing and re-selection
//       />
//     </div>
//   );
// }


import AsyncSelect from 'react-select/async';
import { fetchCommodities } from '../services/api';

export default function CommodityDropdown({ onSelect }) {
  const loadOptions = async (inputValue) => {
    if (!inputValue) return [];
    const data = await fetchCommodities(inputValue);

    return data.map(item => ({
      label: `${item.commodity} (${item.hs_code})`,
      value: item.hs_code
    }));
  };

  return (
    <div className="my-4">
      <AsyncSelect
        cacheOptions
        loadOptions={loadOptions}
        defaultOptions={false}
        placeholder="Type to search commodity..."
        onChange={onSelect}
        isClearable={true}  // Enables clearing and re-selection
      />
    </div>
  );
}

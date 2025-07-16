// import React, { useState } from 'react';
// import AsyncSelect from 'react-select/async';

// export default function CommodityDropdown({ onSelect }) {
//   const [inputValue, setInputValue] = useState('');

//   // Load options as the user types
//   const loadOptions = async (inputValue, callback) => {
//     if (!inputValue) {
//       callback([]);
//       return;
//     }

//     try {
//       const response = await fetch(`http://192.168.0.103:8000/api/commodities/?search=${inputValue}`);
//       const data = await response.json();

//       const options = data.map(item => ({
//         label: `${item.commodity} (${item.hs_code})`,
//         value: item.hs_code
//       }));

//       callback(options);
//     } catch (error) {
//       console.error('Error fetching commodities:', error);
//       callback([]);
//     }
//   };

//   return (
//     <AsyncSelect
//       cacheOptions
//       loadOptions={loadOptions}
//       onInputChange={setInputValue}
//       placeholder="Search Commodity or HS Code..."
//       onChange={selected => onSelect(selected)}
//     />
//   );
// }


import AsyncSelect from 'react-select/async';

export default function CommodityDropdown({ onSelect }) {
  const loadOptions = async (inputValue) => {
    if (!inputValue) return [];

    const response = await fetch(`http://192.168.0.103:8000/api/commodities/?search=${inputValue}`);
    const data = await response.json();

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
        isClearable={true}  // 🔑 Enables clearing and re-selection
      />
    </div>
  );
}

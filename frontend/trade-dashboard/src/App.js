import React from 'react';
import ForecastDashboard from './components/ForecastDashboard';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className="App">
      <Navbar />
      <ForecastDashboard />
    </div>
  );
}

export default App;
// This is the main entry point of the React application.
// It imports the ForecastDashboard component and renders it within the App component.
// The App component serves as the root component of the application, which can be extended with more features and components in the future.
// The ForecastDashboard component is responsible for displaying the trade forecast functionality,
// allowing users to input HS codes and retrieve forecast data based on the selected model.
// This structure allows for easy expansion and modularization of the application as new features are added.
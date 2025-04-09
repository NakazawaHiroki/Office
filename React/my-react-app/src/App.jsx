import React from 'react';
import MapComponent from './MapComponent'; // ← MapComponentを読み込む
import Toolbar from './Toolbar';
import './App.css';

function App() {
  return (
    <div className="App">
      <MapComponent />
      <Toolbar />
    </div>
  );
}

export default App;

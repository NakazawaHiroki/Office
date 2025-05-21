import React from 'react';
import MapComponent from './MapComponent.tsx'; // ← MapComponentを読み込む
import Toolbar from './Toolbar.tsx';
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

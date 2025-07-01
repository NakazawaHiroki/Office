// src/Floating.tsx
import React from 'react';

type Props = {
  zoomEnabled: boolean;
  setZoomEnabled: React.Dispatch<React.SetStateAction<boolean>>;
};

const buttonStyle: React.CSSProperties = {
  position: 'absolute',
  top: '16px',
  right: '16px',
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  color: '#fff',
  border: 'none',
  padding: '8px 12px',
  borderRadius: '4px',
  fontSize: '14px',
  cursor: 'pointer',
  zIndex: 1000
};

const Floating: React.FC<Props> = ({ zoomEnabled, setZoomEnabled }) => {
  const handleToggle = () => setZoomEnabled(prev => !prev);
  return (
    <button onClick={handleToggle} style={buttonStyle}>
      {zoomEnabled ? 'ON' : 'OFF'}
    </button>
  );
};

export default Floating;

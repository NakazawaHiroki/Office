import React, { useState } from 'react';
import { GoogleMap, OverlayView, useLoadScript } from '@react-google-maps/api';
import './App.css';

import locationsData from './locations_horror.js';


// Googleマップのスタイル
const mapContainerStyle = {
  width: '100%',
  height: '100vh'
};

// 中心座標（東京駅）
const center = { lat: 36.645091, lng: 138.192772 };
// Googleマップのオプション（不要なUIを非表示）
const options = {
  disableDefaultUI: true,       // ← 全てのデフォルトUIを無効化（ズームボタン、ストリートビュー、人型アイコン等）
};

// Overlay（吹き出し）本体のスタイル
const bubbleStyle = {
  position: 'absolute',
  background: '#fff',
  border: '2px solid #333',
  borderRadius: '6px',
  padding: '0px 5px 0px 5px',
  fontSize: '14px',
  whiteSpace: 'nowrap'
};

const MapComponent = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: 'AIzaSyAg13B6aIPtpC9ZBeL9t6VA_72B4YpBjmE'
  });

  const [locations, ] = useState(locationsData);

  if (loadError) return <div>マップのロードエラーです。</div>;
  if (!isLoaded) return <div>マップを読み込み中...</div>;

  return (
    <GoogleMap mapContainerStyle={mapContainerStyle} zoom={15} center={center} options={options}>
      {locations.map(loc => (
        <OverlayView
          key={loc.id}
          position={loc.position}
          mapPaneName={OverlayView.OVERLAY_MOUSE_TARGET}
          >
          <div style={bubbleStyle}>
            {loc.message}
          </div>
        </OverlayView>
      ))}
    </GoogleMap>
  );
};

export default MapComponent;

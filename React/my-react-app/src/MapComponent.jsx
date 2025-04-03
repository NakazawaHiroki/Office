import React, { useState } from 'react';
import { GoogleMap, OverlayView, useLoadScript } from '@react-google-maps/api';
import locationsData from './locations';
import './App.css';

// Googleマップのスタイル
const mapContainerStyle = {
  width: '100%',
  height: '100vh'
};

// 中心座標（東京駅）
const center = { lat: 35.681236, lng: 139.767125 };

// Googleマップのオプション（不要なUIを非表示）
const options = {
  disableDefaultUI: true,       // ← 全てのデフォルトUIを無効化（ズームボタン、ストリートビュー、人型アイコン等）
};

// Overlay（吹き出し）本体のスタイル
const bubbleStyle = {
  position: 'absolute',
  background: '#fff',
  border: '1px solid #333',
  borderRadius: '6px',
  padding: '0px 2px 2px 0px',
  fontSize: '14px',
  whiteSpace: 'nowrap'
};

const MapComponent = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: '#################API　KEY####################'
  });

  const [locations, ] = useState(locationsData);

  if (loadError) return <div>マップのロードエラーです。</div>;
  if (!isLoaded) return <div>マップを読み込み中...</div>;

  return (
    <GoogleMap mapContainerStyle={mapContainerStyle} zoom={13} center={center} options={options}>
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

import React, { useState, useMemo } from 'react';
import { GoogleMap, OverlayView, useLoadScript } from '@react-google-maps/api';
import './App.css';
import Floating from './Floating'; // ← 追加：Floating ボタンを読み込む
import locationsData from './locations_horror.js';

// Googleマップのスタイル
const mapContainerStyle = {
  width: '100%',
  height: '100vh',
  position: 'relative', // Floatingボタンを重ねるために必要
};

// 中心座標（東京駅）
const center = { lat: 36.645091, lng: 138.192772 };

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
  // APIキー読み込み完了後に useLoadScript を実行
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: '_________KEY_________'  // 初期は空文字で防御
  });

  const [zoomEnabled, setZoomEnabled] = useState(true);
  const [locations, ] = useState(locationsData);

  const mapOptions = useMemo(() => ({
    disableDefaultUI: true,
    scrollwheel: zoomEnabled,
  }), [zoomEnabled]);

  if (loadError) return <div>マップのロードエラーです。</div>;
  if (!isLoaded) return <div>マップを読み込み中...</div>;

  return (
    <div style={mapContainerStyle}>
      <GoogleMap mapContainerStyle={mapContainerStyle} zoom={15} center={center} options={mapOptions}>
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
      <Floating zoomEnabled={zoomEnabled} setZoomEnabled={setZoomEnabled} />
    </div>
  );
};

export default MapComponent;

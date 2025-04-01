import React, { useState } from 'react';
import { GoogleMap, OverlayView, useLoadScript } from '@react-google-maps/api';
import locationsData from './locations';

// Googleマップのスタイル
const mapContainerStyle = {
  width: '100%',
  height: '100vh'
};

// 中心座標（東京駅）
const center = { lat: 35.681236, lng: 139.767125 };

// state管理の位置データ
// const initialLocations = [
//   { id: 1, position: { lat: 35.681236, lng: 139.767125 }, message: '東京駅' },
//   { id: 2, position: { lat: 35.6595, lng: 139.7005 }, message: '渋谷交差点' },
//   { id: 3, position: { lat: 35.6586, lng: 139.7454 }, message: '東京タワー' }
// ];

// Googleマップのオプション（不要なUIを非表示）
const options = {
  disableDefaultUI: true,       // ← 全てのデフォルトUIを無効化（ズームボタン、ストリートビュー、人型アイコン等）
};

// Overlay（吹き出し）本体のスタイル
const bubbleStyle = {
  position: 'absolute',
  transform: 'translate(-50%, -100%)', // 吹き出しが座標上部中央になるよう調整
  background: '#fff',
  border: '1px solid #333',
  borderRadius: '4px',
  padding: '6px 10px',
  fontSize: '14px',
  fontWeight: 'bold',
  whiteSpace: 'nowrap'
};

// 吹き出し先端（三角形）のスタイル
const triangleStyle = {
  position: 'absolute',
  left: '50%',
  bottom: '-15px', // 吹き出しの真下に配置
  transform: 'translateX(-50%)',
  width: '0',
  height: '0',
  borderLeft: '8px solid transparent',
  borderRight: '8px solid transparent',
  borderTop: '15px solid #333'
};

const MapComponent = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: '_____google_map__key___'
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
            <div style={triangleStyle} />
          </div>
        </OverlayView>
      ))}
    </GoogleMap>
  );
};

export default MapComponent;

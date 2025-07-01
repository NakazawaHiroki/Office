import React, { useMemo, useState } from 'react';
import {
  APIProvider,
  Map,
  AdvancedMarker,                     // ★ 新コンポーネント
} from '@vis.gl/react-google-maps';
import './App.css';
import Floating from './Floating.tsx';
import locationsData from './locations_horror.ts';

/* ---------- 定数 ---------- */
const CENTER = { lat: 36.645091, lng: 138.192772 };
const FONT_SIZE_MAP: Record<number, number> = { 1: 12, 2: 30 };
const DEFAULT_FONT_SIZE = 14;

/* ---------- 型 ---------- */
type MarkerItem = {
  id: string;
  position: google.maps.LatLngLiteral;
  message: string;
  fontSize: number;
};

/* ---------- メイン ---------- */
const MapComponent: React.FC = () => {
  const [zoomEnabled, setZoomEnabled] = useState(true);

  /* マーカー配列を構築（※SVG 生成は不要になったので削除） */
  const markers = useMemo<MarkerItem[]>(() =>
    locationsData.map((loc) => ({
      id: String(loc.id),
      position: loc.position,
      message: loc.message,
      fontSize: FONT_SIZE_MAP[loc.volume] ?? DEFAULT_FONT_SIZE,
    })),
  []);

  return (
    <APIProvider
      apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
      libraries={['marker']}                // ★ AdvancedMarker 用
    >
      <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
          <Map
            key={zoomEnabled ? 'zoom-on' : 'zoom-off'}
            mapId={import.meta.env.VITE_MAP_ID}
            defaultCenter={CENTER}
            defaultZoom={13}
            options={{
              disableDefaultUI: true,
              gestureHandling: zoomEnabled ? 'greedy' : 'none',
              scrollwheel: zoomEnabled,
            }}
          >
          {markers.map(({ id, position, message, fontSize }) => (
            <AdvancedMarker key={id} position={position}>
              {/* ▼ custom HTML（CSSは下記） */}
              <div className="marker-bubble" style={{ fontSize }}>
                {message}
              </div>
            </AdvancedMarker>
          ))}
        </Map>

        {/* 既存 UI（ズーム ON/OFF ボタンなど） */}
        <Floating
          zoomEnabled={zoomEnabled}
          setZoomEnabled={setZoomEnabled}
        />
      </div>
    </APIProvider>
  );
};

export default MapComponent;

import React, { useState, useMemo } from 'react';
import { GoogleMap, Marker, useLoadScript } from '@react-google-maps/api';
import './App.css';
import Floating from './Floating';
import locationsData from './locations_horror.js'; // volume対応版を想定

const mapContainerStyle = {
  width: '100%',
  height: '100vh',
  position: 'relative',
};

const center = { lat: 36.645091, lng: 138.192772 };

// volume に応じてフォントサイズを変える
const getFontSize = (volume) => {
  if (volume === 1) return 12;
  if (volume === 2) return 14;
  if (volume === 3) return 16;
  return 14;
};

// Canvas を使って文字列の描画幅を測定
const measureTextWidth = (text, fontSize = 14, fontFamily = 'Arial') => {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  ctx.font = `${fontSize}px ${fontFamily}`;
  return ctx.measureText(text).width;
};

// SVGマーカーを作成（長方形＋角丸）
const createSvgMarker = (text, fontSize = 14) => {
  const paddingH = 10; // 左右余白
  const paddingV = 4;  // 上下余白
  const measuredWidth = measureTextWidth(text, fontSize);
  const width = Math.ceil(measuredWidth + paddingH * 2);
  const height = fontSize + paddingV * 2;

  const escapedText = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">
      <rect x="0" y="0" width="${width}" height="${height}" rx="6" ry="6"
            fill="#ffffff" stroke="#333333" stroke-width="1.5"/>
      <text x="${width / 2}" y="${height / 2 + fontSize / 2 - 2}" text-anchor="middle"
            font-size="${fontSize}" font-family="Arial" fill="#000000">
        ${escapedText}
      </text>
    </svg>
  `;

  return {
    url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`,
    size: { width, height },
    anchor: { x: width / 2, y: height }
  };
};


const MapComponent = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: '___________KEY___________'
  });

  const [zoomEnabled, setZoomEnabled] = useState(true);
  const [locations] = useState(locationsData);

  const mapOptions = useMemo(() => ({
    disableDefaultUI: true,
    scrollwheel: zoomEnabled,
  }), [zoomEnabled]);

  if (loadError) return <div>マップのロードエラーです。</div>;
  if (!isLoaded) return <div>マップを読み込み中...</div>;

  return (
    <div style={mapContainerStyle}>
      <GoogleMap
        mapContainerStyle={{ width: '100%', height: '100%' }}
        zoom={13}
        center={center}
        options={mapOptions}
      >
      {locations.map(loc => {
        const fontSize = getFontSize(loc.volume);
        const { url, size, anchor } = createSvgMarker(loc.message, fontSize);

        return (
          <Marker
            key={loc.id}
            position={loc.position}
            icon={{
              url,
              scaledSize: new window.google.maps.Size(size.width, size.height),
              anchor: new window.google.maps.Point(anchor.x, anchor.y)
            }}
          />
        );
      })}
      </GoogleMap>

      <Floating zoomEnabled={zoomEnabled} setZoomEnabled={setZoomEnabled} />
    </div>
  );
};

export default MapComponent;

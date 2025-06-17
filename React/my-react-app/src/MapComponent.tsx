import React, { useMemo, useRef, useState } from 'react';
import {
  GoogleMap,
  Marker,
  useLoadScript,
  type MarkerProps,
} from '@react-google-maps/api';
import './App.css';
import Floating from './Floating.tsx';
import locationsData from './locations_horror.ts';

/* ---------- 定数 & 型 ---------- */

type LatLng = google.maps.LatLngLiteral;               // Google Maps が型を持っているので転用
type Location = typeof locationsData[number];          // data の型そのまま流用（id / position / message / volume）

const CENTER: LatLng = { lat: 36.645091, lng: 138.192772 };
const MAP_CONTAINER_STYLE: React.CSSProperties = { width: '100%', height: '100vh', position: 'relative' };

/* volume → font-size 変換は定数テーブルで十分 */
const FONT_SIZE_MAP: Record<number, number> = { 1: 12, 2: 30 };
const DEFAULT_FONT_SIZE = 14;

/* ---------- ユーティリティ ---------- */

/** 再利用する 2D Canvas。毎回生成しない */
const getMeasurementContext = (() => {
  let ctx: CanvasRenderingContext2D | null = null;
  return () => {
    if (ctx) return ctx;
    const canvas = document.createElement('canvas');
    ctx = canvas.getContext('2d');
    return ctx;
  };
})();

/** 文字列幅を測定（フォントと文字列でキャッシュ） */
const measureTextWidth = (() => {
  const cache = new Map<string, number>();
  return (text: string, fontSize = DEFAULT_FONT_SIZE, fontFamily = 'Arial'): number => {
    const key = `${fontSize}-${fontFamily}-${text}`;
    if (cache.has(key)) return cache.get(key)!;

    const ctx = getMeasurementContext();
    if (!ctx) return 0;

    ctx.font = `${fontSize}px ${fontFamily}`;
    const width = ctx.measureText(text).width;
    cache.set(key, width);
    return width;
  };
})();

/** マーカー SVG を生成（text+fontSize をキーにキャッシュ） */
const createSvgMarker = (() => {
  const cache = new Map<string, MarkerIcon>();
  return (text: string, fontSize: number = DEFAULT_FONT_SIZE): MarkerIcon => {
    const key = `${fontSize}-${text}`;
    if (cache.has(key)) return cache.get(key)!;

    const paddingH = 10;
    const paddingV = 4;
    const measuredWidth = measureTextWidth(text, fontSize);
    const width = Math.ceil(measuredWidth + paddingH * 2);
    const height = fontSize + paddingV * 2;

    /* HTML エスケープ */
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

    const icon: MarkerIcon = {
      url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`,
      size: { width, height },
      anchor: { x: width / 2, y: height },
    };
    cache.set(key, icon);
    return icon;
  };
})();

type MarkerIcon = {
  url: string;
  size: { width: number; height: number };
  anchor: { x: number; y: number };
};

/* ---------- メインコンポーネント ---------- */

const MapComponent: React.FC = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  });

  /** ズーム制御 */
  const [zoomEnabled, setZoomEnabled] = useState(true);

  /** マップ共通オプション（依存は zoomEnabled のみ） */
  const mapOptions = useMemo<google.maps.MapOptions>(
    () => ({ disableDefaultUI: true, scrollwheel: zoomEnabled }),
    [zoomEnabled]
  );

  /** Marker 描画オブジェクトを 1 回だけ構築 */
  const markers = useMemo<MarkerProps[]>(() => {
    if (!isLoaded) return [];               // ← ここがポイント
    return locationsData.map((loc) => {
      const fontSize = FONT_SIZE_MAP[loc.volume] ?? DEFAULT_FONT_SIZE;
      const { url, size, anchor } = createSvgMarker(loc.message, fontSize);

      return {
        key: String(loc.id),
        position: loc.position,
        icon: {
          url,
          scaledSize: new google.maps.Size(size.width, size.height),
          anchor: new google.maps.Point(anchor.x, anchor.y),
        },
      };
    });
  }, [isLoaded]);

  if (loadError) return <div>マップのロードエラーです。</div>;
  if (!isLoaded) return <div>マップを読み込み中...</div>;

  return (
    <div style={MAP_CONTAINER_STYLE}>
      <GoogleMap
        mapContainerStyle={{ width: '100%', height: '100%' }}
        zoom={13}
        center={CENTER}
        options={mapOptions}
      >
        {markers.map((props) => (
          <Marker {...props} />
        ))}
      </GoogleMap>

      <Floating zoomEnabled={zoomEnabled} setZoomEnabled={setZoomEnabled} />
    </div>
  );
};

export default MapComponent;

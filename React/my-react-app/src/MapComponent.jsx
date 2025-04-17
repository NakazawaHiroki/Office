import React, { useState, useMemo, useRef, useCallback } from 'react';
import { GoogleMap, OverlayView, useLoadScript } from '@react-google-maps/api';
import './App.css';
import Floating from './Floating';
import locationsData from './locations_horror.js';

const mapContainerStyle = {
  width: '100%',
  height: '100vh',
  position: 'relative',
};

const defaultCenter = { lat: 36.645091, lng: 138.192772 };

const bubbleStyle = {
  position: 'absolute',
  background: '#fff',
  border: '2px solid #333',
  borderRadius: '6px',
  padding: '0px 5px 0px 5px',
  fontSize: '14px',
  whiteSpace: 'nowrap',
  pointerEvents: 'none', // 吹き出しでクリック遮らないように
};

const MapComponent = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
  });

  const [zoomEnabled, setZoomEnabled] = useState(true);
  const [locations] = useState(locationsData);

  const mapRef = useRef();

  const onLoad = useCallback(map => {
    mapRef.current = map;

    // ビューポートに収める（locationsからbounds計算）
    const bounds = new window.google.maps.LatLngBounds();
    locations.forEach(loc => bounds.extend(loc.position));
    map.fitBounds(bounds);
  }, [locations]);

  const mapOptions = useMemo(() => ({
    disableDefaultUI: true,
    scrollwheel: zoomEnabled,
    gestureHandling: 'greedy',
  }), [zoomEnabled]);

  if (loadError) return <div>マップのロードエラーです。</div>;
  if (!isLoaded) return <div>マップを読み込み中...</div>;

  return (
    <div style={mapContainerStyle}>
      <Floating zoomEnabled={zoomEnabled} setZoomEnabled={setZoomEnabled} />
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={8}
        center={defaultCenter}
        options={mapOptions}
        onLoad={onLoad}
      >
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
    </div>
  );
};

export default MapComponent;

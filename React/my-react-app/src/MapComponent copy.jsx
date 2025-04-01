import React from 'react';
import { GoogleMap, InfoWindow, useLoadScript } from '@react-google-maps/api';
import InfoWindowMessage from './InfoWindowMessage';

// Googleマップの表示領域のスタイル（画面いっぱいに表示）
const mapContainerStyle = {
  width: '100%',
  height: '100vh'
};

// マップの初期表示位置（東京駅の座標）
const center = { lat: 35.681236, lng: 139.767125 };

// 各場所の座標と、表示する吹き出しのメッセージ
const locations = [
  { position: { lat: 35.681236, lng: 139.767125 }, message: '東京駅' },
  { position: { lat: 35.6595,  lng: 139.7005   }, message: '渋谷スクランブル交差点' },
  { position: { lat: 35.6586,  lng: 139.7454   }, message: '東京タワー' },
  { position: { lat: 35.7148,  lng: 139.7967   }, message: '浅草寺' },
  { position: { lat: 35.6764,  lng: 139.6993   }, message: '明治神宮' },
  { position: { lat: 35.6605,  lng: 139.7297   }, message: '六本木ヒルズ' },
  { position: { lat: 35.6300,  lng: 139.8800   }, message: 'お台場' },
  { position: { lat: 35.7156,  lng: 139.7730   }, message: '上野公園' },
  { position: { lat: 35.6852,  lng: 139.7528   }, message: '皇居' },
  { position: { lat: 35.6987,  lng: 139.7733   }, message: '秋葉原' }
];

// Googleマップのオプション（不要なUIを非表示）
const options = {
  disableDefaultUI: true,       // ← 全てのデフォルトUIを無効化（ズームボタン、ストリートビュー、人型アイコン等）
};

// MapComponentコンポーネント本体
const MapComponent = () => {

  // Googleマップのスクリプトを非同期ロード
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: 'AIzaSyBThVJZtvyxFt4NopZvau5yjyH7iplF1TA'
  });

  // InfoWindow（吹き出し）が表示されたタイミングで呼ばれる
  // 吹き出しのデザイン（余白や影など）を調整する処理
  const handleInfoWindowLoad = () => {
    // InfoWindowの要素を取得
    document.querySelectorAll('.gm-style-iw').forEach(iw => {
      // InfoWindowの余白を削除
      iw.style.padding = '0';
      iw.parentElement.style.top = '0px';  // ← 親要素も調整

      // 吹き出しの背景（枠、影）を取得
      const iwBackground = iw.previousElementSibling;

      if (iwBackground) {

        iwBackground.style.top = '0px';

        // 左右の余白を削除
        [0, 2].forEach(i => {
          if(iwBackground.children[i]) iwBackground.children[i].style.margin = '0';
        });

        // 上下の影を非表示にする
        [1, 3].forEach(i => {
          if(iwBackground.children[i]) iwBackground.children[i].style.display = 'none';
        });
      }
    });

    // 吹き出しの閉じるボタン（×）を非表示にする
    document.querySelectorAll('.gm-ui-hover-effect').forEach(btn => {
      btn.style.display = 'none';
    });
  };

  // マップがロード中にエラーが起きた場合の表示
  if (loadError) return <div>マップの読み込み中にエラーが発生しました。</div>;

  // マップのロードが完了するまでの表示
  if (!isLoaded) return <div>マップを読み込み中です...</div>;

  return (
    // GoogleMapコンポーネントで地図を表示
    <GoogleMap 
      mapContainerStyle={mapContainerStyle}  // 表示スタイル
      zoom={13}                              // 初期ズームレベル
      center={center}                        // 中心座標
      options={options}                      // UIオプション設定
    >
      {/* 各場所に吹き出し（InfoWindow）を表示 */}
      {locations.map((loc, idx) => (
        <InfoWindow
          key={idx}                          // Reactで各要素を識別するためのkey
          position={loc.position}            // 吹き出しの表示位置
          onDomReady={handleInfoWindowLoad}  // 表示後のスタイル調整処理を呼ぶ
        >
          {/* 吹き出し内にメッセージを表示する専用コンポーネントを使用 */}
          <InfoWindowMessage 
            message={loc.message}
            style={{
//              padding: '2px 6px',        // 吹き出し内余白を調整（少なめ）
              fontSize: '14px',          // フォントサイズ調整
              color: '#333',             // 文字色
              //fontWeight: 'bold'         // 太字に設定
              textAlign: 'center'         //位置
            }}
          />
        </InfoWindow>
      ))}
    </GoogleMap>
  );
};

export default MapComponent;

import React from 'react';

// 吹き出し内メッセージのデザインを担当するコンポーネント
const InfoWindowMessage = ({ message, style = {} }) => {
  const defaultStyle = {
    margin: 0,             // デフォルトの余白はなし
    padding: '4px 8px',    // デフォルトの内側余白
    fontSize: '16px',      // デフォルトのフォントサイズ
    lineHeight: '1',       // 行間を最小限に
    whiteSpace: 'nowrap',   // メッセージが改行されないようにする
  };

  return (
    <div style={{ ...defaultStyle, ...style }}>
      {message}
    </div>
  );
};

export default InfoWindowMessage;

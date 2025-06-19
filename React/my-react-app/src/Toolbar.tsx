import React, { useState, CSSProperties, ChangeEvent } from 'react';

/*--------------------------------------------------
  型定義
--------------------------------------------------*/
type ToolbarProps = {
  /** 送信ボタンを押したときに呼ばれるコールバック */
  onSend?: (message: string) => void;
};

/*--------------------------------------------------
  インラインスタイル（CSSProperties 型）
--------------------------------------------------*/
const toolbarStyle: CSSProperties = {
  position: 'fixed',
  bottom: 0,
  left: 0,
  right: 0,
  width: '100%',
  height: '60px',
  backgroundColor: '#eee',
  display: 'flex',
  alignItems: 'center',
  paddingLeft: '4px',
  paddingRight: '4px',
  boxShadow: '0 -2px 5px rgba(0,0,0,0.1)',
  zIndex: 1000,
  boxSizing: 'border-box',
};

const inputStyle: CSSProperties = {
  flexGrow: 1,
  height: '36px',
  fontSize: '16px',
  padding: '0 10px',
  marginRight: '8px',
  border: '1px solid #ccc',
  borderRadius: '4px',
};

const buttonStyle: CSSProperties = {
  height: '36px',
  padding: '0 16px',
  fontSize: '14px',
  marginRight: '2px',
  backgroundColor: '#4CAF50',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};

/*--------------------------------------------------
  コンポーネント
--------------------------------------------------*/
const Toolbar: React.FC<ToolbarProps> = ({ onSend }) => {
  const [input, setInput] = useState<string>('');

  /* 送信ハンドラ */
  const handleSend = () => {
    onSend?.(input);          // 親に渡したい場合
    console.log('送信:', input);
    setInput('');
  };

  /* 入力欄 onChange ハンドラ */
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  return (
    <div style={toolbarStyle}>
      <input
        type="text"
        value={input}
        onChange={handleChange}
        placeholder="メッセージを入力"
        style={inputStyle}
      />
      <button onClick={handleSend} style={buttonStyle}>
        送信
      </button>
    </div>
  );
};

export default Toolbar;

import React, { useState } from 'react';

    const toolbarStyle = {
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,                      // ← 追加：右端を明示的に制御
        width: '100%',
        height: '60px',
        backgroundColor: '#eee',
        display: 'flex',
        alignItems: 'center',
        paddingLeft: '16px',           // 左側余白
        paddingRight: '16px',          // 右側余白（明示）
        boxShadow: '0 -2px 5px rgba(0,0,0,0.1)',
        zIndex: 1000,
        boxSizing: 'border-box'        // ← paddingを含めて幅を計算（これが超重要）
    };

  const inputStyle = {
    flexGrow: 1,
    height: '36px',
    fontSize: '16px',
    padding: '0 10px',
    marginRight: '8px',
    border: '1px solid #ccc',
    borderRadius: '4px'
  };
  
  const buttonStyle = {
    height: '36px',
    padding: '0 16px',
    fontSize: '14px',
    marginRight: '8px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  };

const Toolbar = () => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    console.log('送信:', input);
    setInput('');
  };

  return (
    <div style={toolbarStyle}>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="メッセージを入力"
        style={inputStyle}
      />
      <button onClick={handleSend} style={buttonStyle}>送信</button>
    </div>
  );
};

export default Toolbar;

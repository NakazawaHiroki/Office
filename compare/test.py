import tkinter as tk

def create_canvas_app():
    # メインウィンドウを作成
    root = tk.Tk()
    root.title("Canvas Layout Example")
    
    # ウィンドウサイズを設定
    root.geometry("800x600")
    
    # ウィンドウのレイアウトを3列に設定
    root.columnconfigure(0, weight=0, minsize=100)  # 左のCanvas（横幅固定100ピクセル）
    root.columnconfigure(1, weight=1, minsize=100)  # 中央のCanvas（伸縮可）
    root.columnconfigure(2, weight=1, minsize=100)  # 右のCanvas（伸縮可）
    
    root.rowconfigure(0, weight=1)  # Canvas全体の高さを伸縮可能に設定
    
    # 左のCanvas
    left_canvas = tk.Canvas(root, bg="blue", width=100)
    left_canvas.grid(row=0, column=0, sticky="nsew")
    
    # 中央のCanvas
    center_canvas = tk.Canvas(root, bg="green", width=200)
    center_canvas.grid(row=0, column=1, sticky="nsew")
    
    # 右のCanvas
    right_canvas = tk.Canvas(root, bg="red", width=350)
    right_canvas.grid(row=0, column=2, sticky="nsew")
    
    # アプリケーションを開始
    root.mainloop()

if __name__ == "__main__":
    create_canvas_app()

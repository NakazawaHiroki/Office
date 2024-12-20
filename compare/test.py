import tkinter as tk
from tkinter import ttk

class ScrollableCanvasFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Canvasとスクロールバーを作成
        self.canvas = tk.Canvas(self, bg="white")
        self.h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # Canvasにスクロールバーを設定
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        # ウィジェットを配置
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        # グリッドの重みを設定
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _update_scroll_region(self, event):
        """Canvasのスクロール領域を更新"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# メインアプリケーション
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Resizable Canvas Frames with Entry and Button")
        self.geometry("800x600")

        # 上部にエントリーウィジェットとボタンを配置するフレーム
        self.top_frame = tk.Frame(self, bg="lightblue")
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # エントリーウィジェットを追加
        self.entry1 = tk.Entry(self.top_frame)
        self.entry2 = tk.Entry(self.top_frame)
        self.entry1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.entry2.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # ボタンを追加
        self.button = tk.Button(self.top_frame, text="Click Me")
        self.button.grid(row=0, column=2, padx=5, pady=5)

        # グリッドの重みを設定（レスポンシブ対応）
        self.top_frame.columnconfigure(0, weight=1)  # Entry1
        self.top_frame.columnconfigure(1, weight=1)  # Entry2
        self.top_frame.columnconfigure(2, weight=0)  # Buttonは固定サイズ

        # 左フレーム
        self.left_frame = ScrollableCanvasFrame(self, bg="blue")
        self.left_frame.grid(row=1, column=0, sticky="nsew")

        # 右フレーム
        self.right_frame = ScrollableCanvasFrame(self, bg="red")
        self.right_frame.grid(row=1, column=1, sticky="nsew")

        # ウィンドウ全体のグリッド設定
        self.rowconfigure(1, weight=1)  # 下部のフレーム
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

# アプリケーションを起動
if __name__ == "__main__":
    app = App()
    app.mainloop()

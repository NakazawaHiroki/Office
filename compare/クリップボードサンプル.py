import tkinter as tk
from PIL import Image, ImageTk, ImageGrab


class ClipboardImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("クリップボード画像表示（直接Canvasに描画）")

        # メインフレーム
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # キャンバス作成
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # スクロールバー作成
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # 初期設定
        self.images = []  # 表示される画像のリスト（ImageTkオブジェクトを保持）
        self.image_items = []  # Canvas内に配置された画像アイテムのリスト
        self.y_offset = 0  # 画像を積み重ねるためのY位置
        self.last_image_check = None

        # スクロール領域を更新
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # 右クリックイベントをバインド
        self.canvas.bind("<Button-3>", self.delete_image)

        # クリップボードの監視を開始
        self.check_clipboard()

    def on_canvas_configure(self, event):
        """キャンバスのスクロール領域を更新"""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def check_clipboard(self):
        """クリップボードをチェックし、新しい画像があれば追加する"""
        try:
            # 現在のクリップボードの内容を取得
            content = ImageGrab.grabclipboard()

            # 画像データの場合
            if isinstance(content, Image.Image):
                if content != self.last_image_check:
                    self.last_image_check = content
                    self.add_image_to_canvas(content)
            # PNGファイルパスの場合
            elif isinstance(content, list) and len(content) > 0:
                for file_path in content:
                    if file_path.lower().endswith(".png"):  # PNGファイルのみ処理
                        img = Image.open(file_path)
                        if self.last_image_check != img:
                            self.last_image_check = img
                            self.add_image_to_canvas(img)

        except Exception as e:
            print("エラー:", e)

        # 500msごとにクリップボードをチェック
        self.root.after(500, self.check_clipboard)

    def add_image_to_canvas(self, img):
        """Canvasに直接画像を追加表示（左寄せで実際のサイズ）"""
        # Tkinter用に変換
        tk_img = ImageTk.PhotoImage(img)
        self.images.append(tk_img)  # メモリ解放防止のため保持

        # Canvasに画像を描画
        image_item = self.canvas.create_image(0, self.y_offset, anchor="nw", image=tk_img)
        self.image_items.append(image_item)  # アイテムIDを保存

        # 次の画像のY位置を更新
        self.y_offset += img.height + 10

        # キャンバスの仮想サイズを拡張
        self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), self.y_offset))

    def delete_image(self, event):
        """右クリックされた画像を削除"""
        # クリック位置のキャンバスアイテムを取得
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        clicked_item = self.canvas.find_closest(x, y)[0]

        if clicked_item in self.image_items:
            # 削除対象のアイテムをリストから削除
            index = self.image_items.index(clicked_item)
            self.image_items.pop(index)
            self.images.pop(index)

            # キャンバスからアイテムを削除
            self.canvas.delete(clicked_item)

            # 削除後の画像を再配置
            self.relayout_images()

    def relayout_images(self):
        """画像を再配置"""
        self.y_offset = 0
        for item, img in zip(self.image_items, self.images):
            self.canvas.coords(item, 0, self.y_offset)
            self.y_offset += img.height() + 10

        # キャンバスの仮想サイズを再設定
        self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), self.y_offset))


if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardImageApp(root)
    root.mainloop()

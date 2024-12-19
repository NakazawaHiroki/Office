import tkinter as tk

class CustomFrame(tk.Frame):
    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # フレームのサイズを指定
        self.config(width=width, height=height)
        self.pack_propagate(False)  # サイズが自動的に調整されないようにする
        self.pack()  # フレームを親ウィジェットに配置

# テスト用のコード
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Custom Frame Example")

    # 横幅300、高さ200のフレームを作成
    custom_frame = CustomFrame(root, width=300, height=200, bg='lightblue')

    # その他のウィジェットをフレーム内に追加
    label = tk.Label(custom_frame, text="This is a custom frame")
    label.pack()

    root.mainloop()

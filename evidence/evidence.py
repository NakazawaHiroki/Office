import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar, Frame, Button, Canvas
from tkinter import messagebox
import win32clipboard
import io
import re

#############################################################
# 定数
#############################################################
WINDOW_WIDTH            = 600
WINDOW_HEIGHT           = 400
BUTTON_CAPTION_SIZE     = 9
BUTTON_CAPTION_FONT     = 'Arial'
LABEL_TEXT_SIZE         = 9
LABEL_TEXT_FONT         = 'Arial'

#############################################################
# Evidence
#############################################################
class Evidence(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("エビデンス収集")
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')  # ウィンドウの初期サイズを設定
        #ウィンドウのリサイズ設定
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        #ツールバーの作成
        toolFrame = tk.Frame(self)
        toolFrame.grid(row=0, column=0, sticky="we")
        self.createToolBar(toolFrame)
        #キャンバスフレームの作成
        canvasFrame = tk.Frame(self)
        canvasFrame.grid(row=1, column=0, sticky="nswe")
        self.createCanvasFrame(canvasFrame)


    #ツールバーの作成
    def createToolBar(self, toolFrame : Frame):
        # "ToClip" ボタン
        self.to_clip_button = tk.Button(toolFrame, text="ToClip", 
                                        command=self.on_to_clip, 
                                        font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        self.to_clip_button.grid(row=0, column=0, padx=3)

        # コンボボックス
        self.scale_combo = ttk.Combobox(toolFrame, 
                                        values=["0.4", "0.6", "0.8", "1.0"], 
                                        state="readonly", width=4)
        self.scale_combo.current(2)  # デフォルトで"1.0"を選択
        self.scale_combo.grid(row=0, column=1, padx=3)

        # トグルボタン: "右へ"
        self.right_button = tk.Button(toolFrame, text="右へ", 
                                      command=lambda: self.toggle_direction("right"),
                                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        self.right_button.grid(row=0, column=2, padx=3)

        # トグルボタン: "下へ"
        self.down_button = tk.Button(toolFrame, text="下へ", 
                                     command=lambda: self.toggle_direction("down"),
                                     font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        self.down_button.grid(row=0, column=3, padx=3)

        # "画像..." ボタン
        self.save_button = tk.Button(toolFrame, text="画像...", 
                                     command=self.on_save_destination,
                                     font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        self.save_button.grid(row=0, column=4, padx=3)

        # トグルボタンの状態を管理
        self.toggle_state = {"right": False, "down": False}


    #キャンバスフレームの作成
    def createCanvasFrame(self, canvasFrame : Frame):
        canvasFrame.rowconfigure(0, weight=1)
        canvasFrame.columnconfigure(0, weight=1)
        temp = Canvas(canvasFrame, bg="gray")
        temp.grid(row=0, column=0, sticky="nsew")
        # 垂直スクロールバーを作成
        VScroll = Scrollbar(canvasFrame, orient=tk.VERTICAL, command=temp.yview)
        VScroll.grid(row=0, column=1, sticky="ns")
        # 水平スクロールバーを作成
        HScroll = Scrollbar(canvasFrame, orient=tk.HORIZONTAL, command=temp.xview)
        HScroll.grid(row=1, column=0, sticky="ew")
        # キャンバスにスクロールバーを設定
        temp.configure(xscrollcommand=HScroll.set, yscrollcommand=VScroll.set)


    def toggle_direction(self, direction):
        """トグルボタンの動作を制御"""
        if direction == "right":
            self.toggle_state["right"] = True
            self.toggle_state["down"] = False
        elif direction == "down":
            self.toggle_state["right"] = False
            self.toggle_state["down"] = True

        # ボタンの外観を更新
        self.update_toggle_buttons()


    def update_toggle_buttons(self):
        """トグルボタンの見た目を更新"""
        if self.toggle_state["right"]:
            self.right_button.config(relief="sunken")
            self.down_button.config(relief="raised")
        else:
            self.right_button.config(relief="raised")
            self.down_button.config(relief="sunken")


    def on_to_clip(self):
        """"ToClip" ボタンの動作"""
        print("ToClipボタンが押されました")


    def on_save_destination(self):
        """"保存先" ボタンの動作"""
        print("保存先ボタンが押されました")


#メインループ
if __name__ == "__main__":
    #アプリを起動する
    app = Evidence()
    app.update_idletasks()
    app.mainloop()
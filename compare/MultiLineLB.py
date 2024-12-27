import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar

class MultiLineLB(tk.Frame):
    def __init__(self, parent, width, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bNeedScrl      = False
        self.items          = []
        self.selected_item  = None

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Canvas and Scrollbar initialization
        self.canvas = Canvas(self, bg="white", width=width)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        self.bind("<Configure>", self.on_frame_resize)

    #フレームサイズが変更された時に呼ばれる
    def on_frame_resize(self, event):
        self._check_need_scroll()
    
    #アイテムの個数
    def getItemCount(self):
        return len(self.items)

    def addItem(self, *texts):
        # Add a new label with the given texts to the inner frame, each text on a new line
        full_text = "\n".join(texts)
        label = tk.Label(self.inner_frame,
                        text=full_text,
                        anchor="w",
                        justify="left",
                        bg="white",
                        fg="black",
                        width=self.canvas.winfo_width())
        label.default_color = "white"
        label.pack(anchor="nw", pady=1, fill="x")

        # Add a line below each item
        line = tk.Frame(self.inner_frame, height=1, bg="black", width=self.canvas.winfo_width())
        line.pack(fill="x", pady=0)

        # Add the label and line to the list
        self.items.append((label, line))
        # Bind right-click event to the label for selection
        label.bind("<Button-1>", lambda e, lbl=label: self.selectItem(lbl))
        label.bind("<MouseWheel>", self._on_mouse_wheel)
        #一度表示して正確な高さを取得する
        self.update_idletasks()
        self._check_need_scroll()
        #スクロールが必要ならば追加したアイテムが表示されるように移動する
        if self.bNeedScrl:
            self.canvas.yview_moveto(1.0)
        return len(self.items) - 1
    
    #アイテムの更新
    def updateItem(self, index, *texts):
        if index < len(self.items):
            full_text = "\n".join(texts)
            label, line = self.items[index]
            label["text"] = full_text

    #アイテムのテキスト情報の取得
    def getItemText(self, index):
        result = []
        if index < len(self.items):
            label, line = self.items[index]
            result = label["text"].split('\n')
        return result

    #アイテムの削除
    def deleteItem(self, index):
        # Delete the label and line at the given index
        if 0 <= index < len(self.items):
            label, line = self.items.pop(index)
            label.unbind("<Button-1>")
            label.destroy()
            line.destroy()
        self._check_need_scroll()

    def selectItem(self, label):
        # Deselect the previously selected item
        if self.selected_item is not None:
            self.selected_item.configure(bg=self.selected_item.default_color if hasattr(self.selected_item, 'default_color') else 'white')
        # Select the new item
        label.configure(bg="lightblue")
        self.selected_item = label

    def getSelectIndex(self):
        # Get the index of the currently selected item
        if self.selected_item is not None:
            for index, (label, line) in enumerate(self.items):
                if label == self.selected_item:
                    return index
        return -1

    def removeAll(self):
        while self.items:
            label, line = self.items.pop()
            label.destroy()
            line.destroy()
        self.items = []
        self._check_need_scroll()

    def changeItemColor(self, index, color):
        # Change the background color of the item at the given index
        if 0 <= index < len(self.items):
            label, _ = self.items[index]
            label.configure(bg=color)
            label.default_color = color

    def _check_need_scroll(self):
        # Configure the scroll region based on the inner frame size
        reg = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=(reg[0], reg[1], reg[2], reg[3]))
        # Disable scrolling if the inner frame height is less than or equal to the canvas height
        if reg[3] <= self.canvas.winfo_height():
            self.bNeedScrl = False
        else:
            self.bNeedScrl = True
 
    def _on_mouse_wheel(self, event):
        if self.bNeedScrl:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

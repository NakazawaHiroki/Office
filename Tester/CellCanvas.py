from tkinter import Canvas
import tkinter as tk
import math
import CONST


###################################################################
#   ToolTip
###################################################################
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    # ツールチップを表示
    def show_tooltip(self, text, x, y):
        if self.tip_window:
            return
        # ツールチップのウィンドウを作成
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # ウィンドウ枠を消す
        tw.wm_geometry(f"+{x+10}+{y+10}")  # カーソルの少し横に表示
        
        label = tk.Label(tw, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=('Arial', 12))
        label.pack(ipadx=5, ipady=5)

    # ツールチップを隠す
    def hide_tooltip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

###################################################################
#   UpDownAllow 選択中の列で値が入力されているセルまでスキップする
###################################################################
#矩形の情報
RECT_LENGTH = 30

class UpDownAllow:
    def __init__(self, widget):
        self.parent: CellCanvas = widget
        self.upallowRect    = None
        self.downallowRect  = None
        self.upallowText    = None
        self.downallowText  = None

    def destroyAllow(self):
        if self.upallowRect is not None:
            self.parent.delete(self.upallowRect)
            self.upallowRect = None
        if self.upallowText is not None:
            self.parent.delete(self.upallowText)
            self.upallowText = None
        if self.downallowRect is not None:
            self.parent.delete(self.downallowRect)
            self.downallowRect = None
        if self.downallowText is not None:
            self.parent.delete(self.downallowText)
            self.downallowText = None

    def create_allow(self):
        self.destroyAllow()
        #上矢印
        self.upallowRect = self.parent.create_rectangle(0, 0, 1, 1, outline="blue", fill="", width=3)
        self.upallowText = self.parent.create_text(0, 0, text="⇧", font=("Arial", 20, "bold"))
        self.parent.tag_bind(self.upallowRect, "<ButtonPress-1>", self.on_uparrow_press)
        self.parent.tag_bind(self.upallowText, "<ButtonPress-1>", self.on_uparrow_press)
        self.parent.tag_bind(self.upallowRect, "<ButtonRelease-1>", self.on_uparrow_release)
        self.parent.tag_bind(self.upallowText, "<ButtonRelease-1>", self.on_uparrow_release)
        #下矢印
        self.downallowRect = self.parent.create_rectangle(0, 0, 1, 1, outline="blue", fill="", width=3)
        self.downallowText = self.parent.create_text(0, 0, text="⇩", font=("Arial", 20, "bold"))
        self.parent.tag_bind(self.downallowRect, "<ButtonPress-1>", self.on_downarrow_press)
        self.parent.tag_bind(self.downallowText, "<ButtonPress-1>", self.on_downarrow_press)
        self.parent.tag_bind(self.downallowRect, "<ButtonRelease-1>", self.on_downarrow_release)
        self.parent.tag_bind(self.downallowText, "<ButtonRelease-1>", self.on_downarrow_release)
        #表示位置を指定
        self.move_allow(0, 0, self.parent.winfo_width(), self.parent.winfo_height())

    def move_allow(self, x1, y1, x2, y2):
        origin_x = x2 - RECT_LENGTH - 5
        origin_y = (((y2 - y1) / 2) + y1) - RECT_LENGTH
        self.parent.coords(self.upallowRect, origin_x, origin_y, origin_x+RECT_LENGTH, origin_y+RECT_LENGTH)
        self.parent.coords(self.upallowText, origin_x + (RECT_LENGTH/2), origin_y + (RECT_LENGTH/2))
        self.parent.coords(self.downallowRect, origin_x, origin_y+RECT_LENGTH, origin_x+RECT_LENGTH, origin_y+(RECT_LENGTH*2))
        self.parent.coords(self.downallowText, origin_x + (RECT_LENGTH/2), origin_y + (RECT_LENGTH/2 + RECT_LENGTH))

    def on_uparrow_press(self, event):
        self.parent.itemconfig(self.upallowRect, fill="blue")
        self.parent.itemconfig(self.upallowText, fill="white")

    def on_uparrow_release(self, event):
        self.parent.itemconfig(self.upallowRect, fill="")
        self.parent.itemconfig(self.upallowText, fill="black")
        x1, y1, x2, y2 = self.parent.coords(self.upallowRect)
        mouse_x, mouse_y = self.calMousePosition(event)
        #マウスが矩形になければ実行しない
        if mouse_x < x1 or mouse_x > x2 or mouse_y < y1 or mouse_y > y2:
            return
        self.parent.listPageUp()

    def on_downarrow_press(self, event):
        self.parent.itemconfig(self.downallowRect, fill="blue")
        self.parent.itemconfig(self.downallowText, fill="white")

    def on_downarrow_release(self, event):
        self.parent.itemconfig(self.downallowRect, fill="")
        self.parent.itemconfig(self.downallowText, fill="black")
        x1, y1, x2, y2 = self.parent.coords(self.downallowRect)
        mouse_x, mouse_y = self.calMousePosition(event)
        #マウスが矩形になければ実行しない
        if mouse_x < x1 or mouse_x > x2 or mouse_y < y1 or mouse_y > y2:
            return
        self.parent.listPageDown()

    def IsAllowArea(self, event):
        if self.upallowRect is None or self.downallowRect is None:
            return False
        ux1, uy1, ux2, uy2 = self.parent.coords(self.upallowRect)
        dx1, dy1, dx2, dy2 = self.parent.coords(self.downallowRect)
        #マウスの全体領域での座標を計算する
        mouse_x, mouse_y = self.calMousePosition(event)
        #少し余裕を持たせてチェックする
        if mouse_x > (ux1-5) and mouse_x < (ux2+5) and mouse_y > (uy1-5) and mouse_y < (dy2+5):
            return True
        return False
    
    #イベントから親ウィンドウの実際のマウスの座標を計算
    def calMousePosition(self, event):
        x_start, y_start, x_end, y_end = self.parent.getVisiblePosition()
        mouse_x = x_start + event.x
        mouse_y = y_start + event.y
        return mouse_x, mouse_y
    
    #ウィジェットの表示非表示を切り替える
    def visible(self, visible):
        if visible:
            self.parent.itemconfig(self.upallowRect, state=tk.NORMAL)
            self.parent.itemconfig(self.downallowRect, state=tk.NORMAL)
            self.parent.itemconfig(self.upallowText, state=tk.NORMAL)
            self.parent.itemconfig(self.downallowText, state=tk.NORMAL)
        else:
            self.parent.itemconfig(self.upallowRect, state=tk.HIDDEN)
            self.parent.itemconfig(self.downallowRect, state=tk.HIDDEN)
            self.parent.itemconfig(self.upallowText, state=tk.HIDDEN)
            self.parent.itemconfig(self.downallowText, state=tk.HIDDEN)


###################################################################
#   CellCanvas
###################################################################
class CellCanvas(Canvas):
    def __init__(self, master, selectpermission, dispallow, rows, columns, cell_widths, cell_height, **kwargs):
        super().__init__(master, **kwargs, bg='white')
        self.rows                       = rows
        self.columns                    = columns
        self.cell_widths                = cell_widths
        self.cell_height                = cell_height
        self.cells                      = {}
        self.selected_col               = None  # 選択された列を追跡
        self.ListData                   = []
        self.errorCells                 = []
        self.last_mouse_position        = (0, 0)
        self.after_id                   = None
        self.tooltip                    = ToolTip(self)
        self.enableSelect               = True
        self.notifyClick: CellCanvas    = None
        self.notifyVScroll: CellCanvas  = None
        self.updownAllow                = None
        self.popup_menu                 = None
        self.editbox                    = None
        self.editCellPoint              = []

        #イベントをバインド
        if selectpermission:
            self.bind("<Button-1>", self.on_click)
            self.bind("<Motion>", self.on_mouse_move)
            self.bind("<Leave>", self.on_out_canvas)
            #右クリックメニューを作成
            self.popup_menu = tk.Menu(self, tearoff=0)
            self.popup_menu.add_command(label="セル編集", command=self.edit_cell)
            self.bind("<Button-3>", self.on_right_click)
            self.editbox = tk.Entry(self, width=25, font=('Arial', 12), bd=3, relief=tk.SUNKEN)
            self.editbox.place_forget()
            #Enterキー入力をバインド
            self.editbox.bind("<Return>", self.on_enter_key)
        #矢印ボタンを作成する
        if dispallow:
            self.updownAllow = UpDownAllow(self)
            self.bind("<Configure>", self.adjust_allow)


    #クリックイベントがあったことを知らせたいときに指定する
    def setNotifyClick(self, notify):
        self.notifyClick = notify

    def setNotifyVScroll(self, notify):
        self.notifyVScroll = notify

    #クリックイベントが通知された
    def fireClickEvent(self, col):
        self.select_col(col)

    def load_data(self, data):
        self.selected_col = None
        self.errorCells = []    #エラーの選択状態もクリアする
        gridOriginY = 0
        for row, row_data in enumerate(data):
            gridOriginX = 0
            for col, value in enumerate(row_data):
                #列ごとの幅を取得
                cell_width = self.cell_widths[col]
                gridOriginY = row * self.cell_height
                rect_id = self.create_rectangle(gridOriginX, 
                                                gridOriginY,  
                                                gridOriginX+cell_width, 
                                                gridOriginY+self.cell_height, 
                                                outline="lightgray",
                                                fill="")
                self.updateCellText(str(value), row, col)
                gridOriginX = gridOriginX + cell_width
                self.cells[(row, col)] = rect_id
        self.ListData = data
        # ウィジェットが描画された後にサイズを取得するためにafterを使用
        if self.updownAllow is not None:
            self.after(100, self.create_allow)

    #矢印ボタンの作成
    def create_allow(self):
        if self.updownAllow is not None:
            self.updownAllow.create_allow()

    #矢印ボタンをちょうどいい場所に表示しなおす
    def adjust_allow(self, event=None):
        if self.updownAllow is None:
            return
        x_start, y_start, x_end, y_end = self.getVisiblePosition()
        #表示位置を指定
        self.updownAllow.move_allow(x_start, y_start, x_end, y_end)

    #実行の開始と終了を通知する
    def enterProcess(self, proc):
        if self.updownAllow is not None:
            if proc:
                self.updownAllow.visible(False)
                self.enableSelect = False
            else:
                self.updownAllow.visible(True)
                self.enableSelect = True

    #1列全体の色を変更する
    def change_column_color(self, col, color):
        # 列全体の背景色を変更
        for row in range(self.rows):
            cell_id = self.cells.get((row, col))
            if cell_id and cell_id not in self.errorCells:
                self.itemconfig(cell_id, fill=color)


    #現在選択中の列番号を取得する
    def get_select_col(self):
        return self.selected_col


    #指定された列を全選択する
    def select_col(self, col, dispscroll=False):
        if self.selected_col is not None:
            # 前の選択された列の色をリセット
            self.change_column_color(self.selected_col, "white")
        
        # 新しい選択を記録して列全体の色を変更
        if col >= 0:
            self.selected_col = col
            self.change_column_color(col, "lightblue")
            if dispscroll:
                # 選択された列のフレーム上の位置を計算
                selectColPoint = sum(self.cell_widths[:col])  # 指定列の左端のX座標を計算

                # xviewでスクロール割合を取得
                x_start, x_end = self.xview()
                scrollregion = self.bbox("all")
                
                if scrollregion:
                    x1, y1, x2, y2 = scrollregion
                    # 水平スクロール位置をX座標に変換
                    x_scroll_start = x1 + (x2 - x1) * x_start
                    x_scroll_end = x1 + (x2 - x1) * x_end
                    
                    # 選択した列が表示されていない場合にスクロールする
                    if selectColPoint < x_scroll_start or selectColPoint > x_scroll_end:
                        # スクロール位置を調整して、選択した列が中央にくるように設定
                        new_x_view = selectColPoint / (x2 - x1)
                        self.xview_moveto(new_x_view)


    def display_row(self, rowNum):
        # 行数が範囲外の場合は何もしない
        if rowNum < 0 or rowNum >= self.rows:
            return
        # 指定された行のY座標を計算（セルの高さを使って）
        row_y = rowNum * self.cell_height
        # キャンバスの表示領域の高さを取得
        canvas_height = self.winfo_height()
        # 指定された行が画面中央に表示されるようにするためのスクロール位置を計算
        scroll_y = row_y - (canvas_height / 2) + (self.cell_height / 2)
        # スクロール領域の範囲を取得
        scrollregion = self.bbox("all")
        if scrollregion:
            x1, y1, x2, y2 = scrollregion
            total_height = y2 - y1  # 全体の高さ

            # スクロール位置を割合に変換してyview_movetoで設定
            if total_height > 0:
                scroll_position = scroll_y / total_height
                self.yview_moveto(scroll_position)
                self.adjust_allow()


    def get_selected_column_values(self):
        # 選択された列の値をすべて取得
        if self.selected_col is None or self.ListData is None:
            return []
        return [self.ListData[row][self.selected_col] for row in range(self.rows)]


    #マウスカーソルの位置の行と列を取得する
    def get_rowcol_OnCursor(self):
        resultRow = -1
        resultCol = -1
        x, y = self.last_mouse_position

        # xviewで水平スクロール割合を取得
        x_start, x_end = self.xview()
        # yviewで垂直スクロール割合を取得
        y_start, y_end = self.yview()
        
        # キャンバスのscrollregion（全体の領域）
        scrollregion = self.bbox("all")
        if scrollregion:
            # scrollregionは(x1, y1, x2, y2)の形式で返される
            x1, y1, x2, y2 = scrollregion
            
            # 水平スクロール位置をX座標に変換
            x_scroll_start = x1 + (x2 - x1) * x_start
            # 垂直スクロール位置をY座標に変換
            y_scroll_start = y1 + (y2 - y1) * y_start

            # 水平スクロール量を加味した列の計算
            col = math.floor(((x + x_scroll_start) / sum(self.cell_widths)) * len(self.cell_widths))
            # 垂直スクロール量を加味した行の計算
            row = math.floor((y + y_scroll_start) // self.cell_height)
            
            if (row, col) in self.cells:
                resultRow = row
                resultCol = col

        return resultRow, resultCol


    def on_click(self, event):
        #矢印ボタンの上は中止する
        if self.updownAllow is not None and self.updownAllow.IsAllowArea(event):
            return
        
        if self.editbox is not None and self.editbox.winfo_viewable():
            #セル編集をキャンセル扱いにする
            self.editbox.place_forget()
        
        if self.enableSelect:
            row, col = self.get_rowcol_OnCursor()
            if row >= 0 and col >= 0:
                self.select_col(col)
                if self.notifyClick is not None:
                    self.notifyClick(col)

    #ポップアップメニューを表示する
    def on_right_click(self, event):
        if self.editbox is not None and self.editbox.winfo_viewable():
            #セル編集をキャンセル扱いにする
            self.editbox.place_forget()
        if self.popup_menu is not None:
            self.editCellPoint = self.get_rowcol_OnCursor()
            self.popup_menu.post(event.x_root, event.y_root)

    #セルを編集する
    def edit_cell(self):
        if self.popup_menu is not None:
            row = self.ListData[self.editCellPoint[0]]
            celltext = row[self.editCellPoint[1]]
            self.editbox.delete(0, tk.END)
            self.editbox.insert(0, celltext)
            #表示位置を計算
            cellX = sum(self.cell_widths[:self.editCellPoint[1]])
            cellY = self.cell_height * self.editCellPoint[0]
            x1, y1, x2, y2 = self.getVisiblePosition()
            pointX = math.ceil(cellX - x1)
            pointY = math.ceil(cellY - y1)
            if self.editbox.winfo_width() < self.winfo_width() - pointX:
                #エディットボックスを右方向に表示
                self.editbox.place(x=pointX, y=pointY)
            else:
                self.editbox.place(x=(pointX - self.editbox.winfo_width()), y=pointY)
            self.editbox.focus()

    def on_enter_key(self, event):
        if self.editbox is not None and self.editbox.winfo_viewable():
            self.editbox.place_forget()
            #セル編集エディットボックスが出ていてエンターキーが押された
            text = self.editbox.get()
            row = self.ListData[self.editCellPoint[0]]
            row[self.editCellPoint[1]] = text
            self.updateCellText(text, self.editCellPoint[0], self.editCellPoint[1], True)


    def on_mousewheel(self, event):
        # 垂直スクロール
        self.yview_scroll(int(-1*(event.delta/40)), "units")
        self.adjust_allow()

    def on_shift_mousewheel(self, event):
        # Shiftキーを押しながらのホイール操作で水平スクロール
        self.xview_scroll(int(-1*(event.delta/40)), "units")
        self.adjust_allow()


    # カーソルが一定時間同じ場所にとどまった時の処理
    def on_still(self):
        #カーソル上のセル情報を取得する
        row, col = self.get_rowcol_OnCursor()
        if row >= 0 and col >= 0:
            cell = self.find_withtag(f"text_{row}_{col}")
            if cell:
                text = self.itemcget(cell[0], 'text')
                if text == '':
                    return
                # キャンバス上のマウス座標
                x_canvas, y_canvas = self.last_mouse_position
                
                # キャンバス上の座標をウィンドウ（スクリーン）座標に変換
                x_root = self.winfo_rootx() + x_canvas
                y_root = self.winfo_rooty() + y_canvas            
                self.tooltip.show_tooltip(text, x_root, y_root)


    # マウスが動いた時の処理
    def on_mouse_move(self, event):
        current_position = (event.x, event.y)
        self.tooltip.hide_tooltip()
        
        # 前回のマウス座標と違うなら
        if current_position != self.last_mouse_position:
            # マウスの新しい位置を更新
            self.last_mouse_position = current_position

            # すでにタイマーが設定されている場合はキャンセル
            if self.after_id is not None:
                self.after_cancel(self.after_id)

            # 2秒後にon_still関数を呼び出すタイマーを設定
            self.after_id = self.after(1000, self.on_still)

    #キャンバスからマウスカーソルが外れた時
    def on_out_canvas(self, event):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.tooltip.hide_tooltip()


    #テストの結果によってセルの色を変更する
    def reflectionCell(self, resultcode, row, col):
        color = None
        
        if resultcode == CONST.RES_MISMATCH:
            color = 'red'
        elif resultcode == CONST.RES_TAGTYPE_ERROR:
            color = 'yellow'
        elif resultcode == CONST.RES_TAGID_NONE:
            color = 'orange'
        elif resultcode == CONST.RES_NO_SUCH_SELECT:
            color = 'yellow'

        cell_id = self.cells.get((row, col))
        if cell_id and color is not None:
            self.itemconfig(cell_id, fill=color)
            self.errorCells.append(cell_id)


    #エラーセルをリセットして選択状態もクリアする
    def clearCellStatus(self):
        self.selected_col = None
        self.errorCells = []    #エラーの選択状態もクリアする
        for i in range(self.columns):
            self.change_column_color(i, "white")


    def updateCellText(self, text, row, col, update = False):
        textOriginX = sum(self.cell_widths[:col])
        textOriginY = row * self.cell_height
        fontsize = 9
        xPadding = (self.cell_widths[col] / 2)
        align = 'center'

        #文字数が多いときはフォントサイズを調整する
        if len(text) > 7:
            fontsize = 6
            xPadding = 3
            align = 'w'

        tag = f"text_{row}_{col}"
        if update:
            self.itemconfig(tag, text=text, font=('Arial', fontsize))
        else:
            self.create_text(textOriginX + xPadding, textOriginY + (self.cell_height / 2)
                                , text=text, tags=tag, font=('Arial', fontsize), anchor=align)
            

    #現在リスト上のどの部分を表示しているか返却
    def getVisiblePosition(self):
        # キャンバス全体のスクロール領域（scrollregion）
        x1, y1, x2, y2 = self.bbox("all")  # 現在のスクロール領域（全体の領域）
        canvas_width = x2 - x1
        canvas_height = y2 - y1
        # 現在表示されている領域の割合
        xview_start, xview_end = self.xview()
        yview_start, yview_end = self.yview()
        # 表示されているX座標範囲を計算
        visible_x_start = xview_start * canvas_width
        visible_x_end = xview_end * canvas_width
        # 表示されているY座標範囲を計算
        visible_y_start = yview_start * canvas_height
        visible_y_end = yview_end * canvas_height
        return visible_x_start, visible_y_start, visible_x_end, visible_y_end

    def listPageUp(self):
        col = self.get_select_col()
        if col is None:
            return
        x_start, y_start, x_end, y_end = self.getVisiblePosition()
        #現在リスト上段に表示されている行を計算する
        rownum = math.ceil(y_start / self.cell_height)
        index = -1
        if rownum > 0:
            for i, row in enumerate(reversed(self.ListData[:rownum])):
                if row[col] != "":
                    index = len(self.ListData[:rownum]) - 1 - i
                    break
            if index >= 0:
                self.display_row(index)
                self.notifyVScroll.display_row(index)

    def listPageDown(self):
        col = self.get_select_col()
        if col is None:
            return
        x_start, y_start, x_end, y_end = self.getVisiblePosition()
        #現在リスト上段に表示されている行を計算する
        rownum = math.ceil(y_end / self.cell_height)
        index = -1
        if rownum > 0:
            for i, row in enumerate(self.ListData[rownum:], start = rownum):
                if row[col] != "":
                    index = i
                    break
            if index >= 0:
                self.display_row(index)
                self.notifyVScroll.display_row(index)

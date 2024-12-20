import fitz  # PyMuPDF
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import CONST

###################################################################
# 定数
###################################################################
TEXT_PADDING_X      = 4                 #矩形で囲った時のPDFへの座標の縮小分横方向(PDFの座標は少し小さめで検出する)
TEXT_PADDING_Y      = 4                 #矩形で囲った時のPDFへの座標の縮小分縦方向(PDFの座標は少し小さめで検出する)
RECT_LINE           = 3                 #矩形の線の太さ
WID_NUM             = 20                #番号の矩形の幅
HEI_NUM             = 13                #番号の矩形の高さ
WID_BTN             = 10                #閉じるマークの幅
HEI_BTN             = 13                #閉じるマークの高さ

def pdf_to_bmp(pdf_path, page_number):
    # PDFを読み込み、指定ページを画像として抽出
    pdf_document = fitz.open(pdf_path)
    if page_number >= pdf_document.page_count:
        return None
    page = pdf_document.load_page(page_number)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    print(f"Resolution: {pix.width}x{pix.height} pixels")  # 解像度を表示
    return img, pdf_document, page, pix.width, pix.height, pdf_document.page_count

###################################################################
# PDFCanvas
###################################################################
class PDFCanvas(tk.Canvas):
    def __init__(self, parent, callback1, callback2, callback3, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callPointRec       = callback1
        self.callPointCancel    = callback2
        self.callSpecRectinfo       = callback3
        self.pdfPath                = ''
        self.document               = None
        self.page                   = None
        self.pageNum                = 0
        self.rect_id                = None
        self.dctRectID              = {}
        self.bYScrl                 = True
        self.bXScrl                 = True
        self.bEnable                = True
        self.loadpdf                = False
        self.nextIdx                = 0         #矩形のインデックスの次の番号
        self.popup_menu             = None
        self.selectRect : fitz.Rect = None      #現在選択中の矩形の座標

        #イベントのバインド
        self.bind("<ButtonPress-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_move)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.bind("<MouseWheel>", self.on_mousewheel)
        self.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)
        #クリックメニューを作成
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="削除", command=self.on_delete_rect)
        self.popup_menu.add_command(label="一致にする", command=self.on_force_match)
        self.popup_menu.add_command(label="番号を上に付ける", command=self.on_move_number)
        self.bind("<Button-3>", self.on_right_click)




    #インデックスの番号を設定する
    def updaterectIndex(self, idx):
        self.nextIdx = idx

    #矩形情報のクリア
    def removeRect(self, nPage, rect, all=False):
        if rect in self.dctRectID:
            if all:
                #後でリストは空にするので、型は残して内容だけ削除する
                idx, color, rectId, numId, btnID, numTextID, btnTextID = self.dctRectID[rect]
            else:
                idx, color, rectId, numId, btnID, numTextID, btnTextID = self.dctRectID.pop(rect)
            self.delete(rectId)
            self.delete(numId)
            self.delete(btnID)
            self.delete(numTextID)
            self.delete(btnTextID)
    
    #矩形情報の全て削除
    def removeAllRect(self):
        for rect in self.dctRectID.keys():
            self.removeRect(self.page, rect, True)
        self.dctRectID.clear()

    #pdfのロード、bOpenは初めてPDFファイルを開いた
    def load_pdf(self, pdf_path, document = None, nPage = 1):
        # PDFを読み込み、指定ページを画像として抽出
        if pdf_path is not None:
            self.page = None
            self.document = None
            doc = fitz.open(pdf_path)
            if doc:
                self.document = doc
                self.pdfPath = pdf_path
            else:
                return False
        if nPage > self.document.page_count:
            return False
        self.page = self.document.load_page(nPage-1)
        pix = self.page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if img is None:
            return False
        
        #矩形を全て削除する
        self.removeAllRect()

        self.pageNum = nPage
        self.img_tk = ImageTk.PhotoImage(img)
        self.create_image(0, 0, anchor="nw", image=self.img_tk)
        self.config(scrollregion=(0, 0, pix.width, pix.height))

        #親ウィジェットのサイズとスクロール領域サイズを比較する
        parent_width = self.master.winfo_width()
        if parent_width < pix.width:
            self.bXScrl = True
        else:
            self.bXScrl = False
        parent_height = self.master.winfo_height()
        if parent_height < pix.height:
            self.bYScrl = True
        else:
            self.bYScrl = False
        self.loadpdf = True
        self.dctRectID.clear()
        print(f"Resolution: {pix.width}x{pix.height} pixels")  # 解像度を表示
        return True

    #PDFファイルをロードしているかのフラグ
    def isLoadPDF(self):
        return self.page is not None
    
    #指定された領域のテキスト情報を取得する
    def getRectText(self, page, x1, y1, x2, y2):
        result = ""
        rect = fitz.Rect(x1+TEXT_PADDING_X, y1+TEXT_PADDING_Y, x2-TEXT_PADDING_X, y2-TEXT_PADDING_Y)
        result = page.get_text("text", clip=rect)
        return result

    #矩形を追加する
    def addRectangle(self, nPage, x1, y1, x2, y2, rectID=None):
        stResult = ''
        #指定ページが表示ページなら矩形を表示する
        if nPage == self.pageNum:
            #矩形を作成
            if rectID is None:
                rectID = self.create_rectangle(x1, y1, x2, y2, outline=CONST.COLOR_SEL, width=RECT_LINE)
            #番号タグを作成する
            numID, btnID, numTextID, btnTextID = self.createNumberTag(CONST.NUM_TAG_RIGHT, x1, y1, x2, y2)
            #配列へ追加する
            self.dctRectID[fitz.Rect(x1, y1, x2, y2)] = (self.nextIdx, CONST.COLOR_SEL, rectID, numID, btnID, numTextID, btnTextID)
            #矩形内の文字列を抽出
            stResult = self.getRectText(self.page, x1, y1, x2, y2)
        elif nPage <= self.document.page_count:
            #表示ページでないならページをロードしてテキストを抽出
            tempPage = self.document.load_page(nPage - 1)
            stResult = self.getRectText(tempPage, x1, y1, x2, y2)
            tempPage = None
        return stResult
    
    #番号のタグを作成する
    def createNumberTag(self, origin, x1, y1, x2, y2, number = -1):
        if origin == CONST.NUM_TAG_TOP:   #上に番号タグをつける
            numX1 = x2 - (WID_NUM+WID_BTN)
            numY1 = y1 - HEI_NUM
        elif origin == CONST.NUM_TAG_RIGHT:   #右に番号タグをつける
            numX1 = x2
            numY1 = y1
        elif origin == CONST.NUM_TAG_BOTTOM:   #下に番号タグをつける
            numX1 = x2 - (WID_NUM+WID_BTN)
            numY1 = y2
        elif origin == CONST.NUM_TAG_LEFT:   #左に番号タグをつける
            numX1 = x1 - (WID_NUM+WID_BTN)
            numY1 = y1
        numX2 = numX1 + WID_NUM
        numY2 = numY1 + HEI_NUM
        #numberが-1の時は新規作成なので現在のインデックスをセット
        if number == -1:
            number = self.nextIdx
        #数字の矩形
        numID = self.create_rectangle(numX1, numY1, numX2, numY2, outline=CONST.COLOR_SEL, width=1, fill='white')
        numTextID = self.create_text(numX1+2, numY1 + (HEI_NUM/2), text=str(number), font=('Arial', 8), anchor='w')
        #ボタンの矩形
        btnID = self.create_rectangle(numX1 + WID_NUM, 
                                        numY1, 
                                        numX1+(WID_NUM+WID_BTN), 
                                        numY1+HEI_BTN, outline=CONST.COLOR_SEL, width=1, fill='lightgray')
        btnTextID = self.create_text(numX1 + WID_NUM + (WID_BTN/2), numY1 + (HEI_BTN/2), text="▼", font=('Arial', 8), anchor='center')
        return numID, btnID, numTextID, btnTextID

    #矩形の色を変更する
    def changeRectColor(self, nPage, rect, stColor):
        if rect in self.dctRectID:
            idx, color, rectId, numId, btnID, numTextID, btnTextID = self.dctRectID[rect]
            self.itemconfig(rectId, outline=stColor)
            self.itemconfig(numId, outline=stColor)
            self.itemconfig(btnID, outline=stColor)
            self.dctRectID[rect] = (idx, stColor, rectId, numId, btnID, numTextID, btnTextID)
    

    #キャンバス表示状態をイメージとして出力
    def getCanvasImage(self):
        if self.page is None:
            return None
        pix = self.page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if img is None:
            return None
        draw = ImageDraw.Draw(img)
        for idx, rectColor, rectID, numID, btnID, numTextID, btnTextID in self.dctRectID.values():
            coords = self.coords(rectID)
            numCoords = self.coords(numID)
            if coords and numCoords:
                x1, y1, x2, y2 = coords
                draw.rectangle([x1, y1, x2, y2], outline=rectColor, width=RECT_LINE)
                x1, y1, x2, y2 = numCoords
                draw.rectangle([x1, y1, x2, y2], outline=rectColor, width=1, fill='white')
                draw.text((x1 + 2, y1), text=str(idx), fill='black', font=ImageFont.load_default())
        return img

    def on_mouse_down(self, event):
        if self.bEnable and self.page is not None:
            # 矩形の開始点を記録
            self.start_x = self.canvasx(event.x)
            self.start_y = self.canvasy(event.y)
            # 矩形描画のためのオブジェクトを初期化
            self.rect_id = self.create_rectangle(self.start_x, self.start_y, self.start_x, 
                                                self.start_y, outline=CONST.COLOR_SEL, width=RECT_LINE)

    #マウスカーソルが動いてる途中
    def on_mouse_move(self, event):
        if self.bEnable and self.page is not None:
            # マウス移動中に矩形を更新
            if self.rect_id:
                self.coords(self.rect_id, self.start_x, self.start_y, self.canvasx(event.x), self.canvasy(event.y))

    #マウスのボタンが離れた
    def on_mouse_up(self, event):
        if self.bEnable and self.page is not None:
            # 矩形の終了点を記録
            end_x = self.canvasx(event.x)
            end_y = self.canvasy(event.y)
            if self.page and end_x-self.start_x > 5 and end_y-self.start_y > 5:
                #矩形を追加
                text = self.addRectangle(self.pageNum, self.start_x, self.start_y, end_x, end_y, self.rect_id)
                self.callPointRec(self, self.pageNum, fitz.Rect(self.start_x, self.start_y, end_x, end_y), text)
            else:
                self.delete(self.rect_id)

    def on_mousewheel(self, event):
        # 垂直スクロール
        if self.bYScrl:
            self.yview_scroll(int(-1*(event.delta/40)), "units")

    def on_shift_mousewheel(self, event):
        # Shiftキーを押しながらのホイール操作で水平スクロール
        if self.bXScrl:
            self.xview_scroll(int(-1*(event.delta/40)), "units")

    #キャンバス上でのクリックイベント
    def on_right_click(self, event):
        #クリック座標から押されたボタンを検出する
        px = self.canvasx(event.x)
        py = self.canvasy(event.y)
        for key, (idx, color, rectId, numId, btnID, numTextID, btnTextID) in self.dctRectID.items():
            coords1 = self.coords(numId)
            nx1, ny1, nx2, ny2 = coords1
            coords2 = self.coords(btnID)
            bx1, by1, bx2, by2 = coords2
            if px >= nx1 and px <= bx2 and py >= by1 and py <= by2:
                self.popup_menu.post(event.x_root, event.y_root)
                self.selectRect = key
                break

    #ポップアップメニューの削除を選択
    def on_delete_rect(self):
        if self.selectRect is not None:
            #メインへ通知
            idx, temp1, temp2, temp3, temp4, temp5, temp6 = self.dctRectID[self.selectRect]
            if self.callPointCancel(self, idx):
                #削除が成功なら削除する
                self.removeRect(self.page, self.selectRect)
    #ポップアップメニューの強制的に一致にするを選択
    def on_force_match(self):
        if self.selectRect is not None:
            self.callSpecRectinfo(self, self.pageNum, self.selectRect, CONST.SR_COLOR, CONST.COLOR_MATCH)

    #ポップアップメニュー番号ラベルを下に付ける
    def on_move_number(self):
        if self.selectRect is not None:
            self.moveNumberTag(self.pageNum, self.selectRect, CONST.NUM_TAG_TOP, True)
    
    #番号タグを移動する
    def moveNumberTag(self, nPage, rect : fitz.Rect, origin, bCall = False):
        if nPage == self.pageNum and rect in self.dctRectID:
            idx, color, rectId, numId, btnID, numTextID, btnTextID = self.dctRectID[rect]
            #一度タグを削除して新たに付ける
            self.delete(numId)
            self.delete(btnID)
            self.delete(numTextID)
            self.delete(btnTextID)
            numId, btnID, numTextID, btnTextID = self.createNumberTag(CONST.NUM_TAG_TOP, rect.x0, rect.y0, rect.x1, rect.y1, idx)
            self.itemconfig(numId, outline=color)
            self.itemconfig(btnID, outline=color)
            self.dctRectID[rect] = (idx, color, rectId, numId, btnID, numTextID, btnTextID)
            if bCall:
                self.callSpecRectinfo(self, nPage, rect, CONST.SR_TAGORI, CONST.NUM_TAG_TOP)

    #現在のPDFでページを移動する
    def movePage(self, nPage):
        self.load_pdf(None, self.document, nPage)
    #現在のPDFのページ数を返却する
    def getPageCount(self):
        if self.document is not None:
            return self.document.page_count
        else:
            return 0
    #現在のページ番号を返却する
    def getPageNum(self):
        return self.pageNum
    
    def disable(self):
        self.bEnable = False
    def enable(self):
        self.bEnable = True

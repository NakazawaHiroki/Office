import tkinter as tk
from tkinter import filedialog, Scrollbar, Frame, Button
import fitz  # PyMuPDF
from tkinter import messagebox
from PIL import Image
import win32clipboard
import io
import re

from PDFCanvas import PDFCanvas
from MatList import MatList
from MultiLineLB import MultiLineLB
import CONST

###################################################################
#   アプリケーション定数
###################################################################
WINDOW_WIDTH            = 1600
WINDOW_HEIGHT           = 900
BUTTON_CAPTION_SIZE     = 9
BUTTON_CAPTION_FONT     = 'Arial'
LABEL_TEXT_SIZE         = 9
LABEL_TEXT_FONT         = 'Arial'
ORGNX_LIST              = 0     #リスト情報の左座標
ORGNX_LEFTPDF           = 200   #左PDFの左端座標
ORGNX_RIGHTPDF          = 900   #右PDFの左端座標
ORGNX_TOOL              = 680   #ツールボタンの左端座標
ORGNX_RIGHTWIDGET       = ORGNX_RIGHTPDF + 210  #右PDFのファイル開く関係左端座標
CANV_WIDTH              = 700   #キャンバスの横幅
CANV_HEIGHT             = 865   #キャンバスの縦幅
CANV_ORGY               = 25    #キャンバスのY開始位置

###################################################################

# 入力が数字かどうかをチェック
def only_numbers_input(char):
    return char.isdigit()

##################################################################
#    CompareLedger
###################################################################
class CompareLedger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.leftFrame: Frame               = None
        self.rightFrame: Frame              = None
        self.leftVScroll: Scrollbar         = None
        self.leftHScroll: Scrollbar         = None
        self.rightVScroll: Scrollbar        = None
        self.rightHScroll: Scrollbar        = None
        self.leftCanvas: PDFCanvas          = None
        self.rightCanvas: PDFCanvas         = None
        self.first                          = None  #最初に矩形を定義した側の情報(キャンバス,ページ番号,矩形座標,テキスト)
        self.nextIdx                        = 0
        self.specRect                       = {}    #ユーザーの指示で矩形の設定を変更したリスト

        self.title("PDF比較ツール")
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')  # ウィンドウの初期サイズを設定

        #記録リストの作成
        self.matlist = MatList()
        # メインフレームを作成
        main_frame = Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        #ボタン等の作成
        self.createComponent(main_frame)
        #サブフレームとスクロールバーの作成
        self.createFrame(main_frame)
        self.leftCanvas.enable()
        self.rightCanvas.enable()

    #ウィンドウ内のコンポネントを作成する
    def createComponent(self, main_frame):
        # バリデーション関数を登録
        vcmd = (self.register(only_numbers_input), '%S')

        #クリップボードへコピーボタンを作成
        btn  = Button(main_frame,  text="To Clip", 
                      command=lambda: self.copyClipbord(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_TOOL, y=0)
        #matファイルパス表示
        self.mat_entry = tk.Entry(main_frame, width=26, font=('Arial', 10))
        self.mat_entry.place(x=ORGNX_LIST, y=3)
        #matファイルを開くボタン
        btn  = Button(main_frame,  text=" ... ", 
                      command=lambda: self.selectmatfile(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LIST+160, y=25)
        #リストを全て削除するボタン
        btn  = Button(main_frame,  text="リセット", 
                      command=lambda: self.clearmat(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LIST+0, y=25)

        #マッチ情報リスト
        self.matLB = MultiLineLB(main_frame, width=200, height=780)
        self.matLB.place(x=ORGNX_LIST, y=55)
        #matファイルを上書き保存ボタンを作成
        btn  = Button(main_frame,  text="保  存", 
                      command=lambda: self.savematfile(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LIST+15, y=843)
        #matファイルを名前つけて保存ボタンを作成
        btn  = Button(main_frame,  text="別名で保存", 
                      command=lambda: self.renamesavematfile(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LIST+80, y=843)

        #左PDFファイル表示
        self.leftpdf_entry = tk.Entry(main_frame, width=50, font=('Arial', 10))
        self.leftpdf_entry.place(x=ORGNX_LEFTPDF, y=3)
        #左pdfファイルを開くボタン
        btn  = Button(main_frame,  text=" ... ", 
                      command=lambda: self.selectleftpdf(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LEFTPDF+356, y=0)
        #改ページ上下ボタン
        btn  = Button(main_frame,  text="▲", 
                      command=lambda: self.pageupleftpdf(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LEFTPDF+390, y=0)
        #左PDFページ表示
        self.leftpdf_page_entry = tk.Entry(main_frame, width=4, font=('Arial', 10), justify="center", 
                                           validate='key', validatecommand=vcmd)
        self.leftpdf_page_entry.place(x=ORGNX_LEFTPDF+416, y=3)
        self.leftpdf_page_entry.bind('<Return>', self.on_left_changepage)
        #改ページ下ボタン
        btn  = Button(main_frame,  text="▼", 
                      command=lambda: self.pagedownleftpdf(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_LEFTPDF+450, y=0)

        #右PDFファイル表示
        self.rightpdf_entry = tk.Entry(main_frame, width=50, font=('Arial', 10))
        self.rightpdf_entry.place(x=ORGNX_RIGHTWIDGET, y=3)
        #右pdfファイルを開くボタン
        btn  = Button(main_frame,  text=" ... ", 
                      command=lambda: self.selectrightpdf(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_RIGHTWIDGET+356, y=0)
        #改ページ上下ボタン
        btn  = Button(main_frame,  text="▲", 
                      command=lambda: self.pageuprightpdf(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_RIGHTWIDGET+390, y=0)
        #右PDFページ表示
        self.rightpdf_page_entry = tk.Entry(main_frame, width=4, font=('Arial', 10), justify="center", 
                                            validate='key', validatecommand=vcmd)
        self.rightpdf_page_entry.bind('<Return>', self.on_right_changepage)
        self.rightpdf_page_entry.place(x=ORGNX_RIGHTWIDGET+416, y=3)
        #改ページ下ボタン
        btn  = Button(main_frame,  text="▼", 
                      command=lambda: self.pagedownrightpdf(), 
                      font=(BUTTON_CAPTION_FONT, BUTTON_CAPTION_SIZE))
        btn.place(x=ORGNX_RIGHTWIDGET+450, y=0)

    #サブフレームとスクロールバーの作成
    def createFrame(self, main_frame):
        #左側PDF表示領域の作成
        self.leftFrame = Frame(main_frame)
        self.leftFrame.place(x=ORGNX_LEFTPDF, y=CANV_ORGY, width=CANV_WIDTH, height=CANV_HEIGHT)
        #左PDF表示キャンバスを作成
        self.leftCanvas = PDFCanvas(self.leftFrame, self.PointRec, self.PointCancel, self.specifyRectInfo, bg="gray")
        self.leftCanvas.grid(row=0, column=0, sticky="nsew")
        # 垂直スクロールバーを作成
        self.leftVScroll = Scrollbar(self.leftFrame, orient=tk.VERTICAL, command=self.leftCanvas.yview)
        self.leftVScroll.grid(row=0, column=1, sticky="ns")
        # 水平スクロールバーを作成
        self.leftHScroll = Scrollbar(self.leftFrame, orient=tk.HORIZONTAL, command=self.leftCanvas.xview)
        self.leftHScroll.grid(row=1, column=0, sticky="ew")
        # キャンバスにスクロールバーを設定
        self.leftFrame.grid_rowconfigure(0, weight=1)
        self.leftFrame.grid_columnconfigure(0, weight=1)
        self.leftCanvas.configure(xscrollcommand=self.leftHScroll.set, yscrollcommand=self.leftVScroll.set)

        #右側PDF表示領域の作成
        self.rightFrame = Frame(main_frame)
        self.rightFrame.place(x=ORGNX_RIGHTPDF, y=CANV_ORGY, width=CANV_WIDTH, height=CANV_HEIGHT)
        #右PDFキャンバスを作成
        self.rightCanvas = PDFCanvas(self.rightFrame, self.PointRec, self.PointCancel, self.specifyRectInfo, bg="gray")
        self.rightCanvas.grid(row=0, column=0, sticky="nsew")
        # 垂直スクロールバーを作成
        self.rightVScroll = Scrollbar(self.rightFrame, orient=tk.VERTICAL, command=self.rightCanvas.yview)
        self.rightVScroll.grid(row=0, column=1, sticky="ns")
        # 水平スクロールバーを作成
        self.rightHScroll = Scrollbar(self.rightFrame, orient=tk.HORIZONTAL, command=self.rightCanvas.xview)
        self.rightHScroll.grid(row=1, column=0, sticky="ew")
        # キャンバスにスクロールバーを設定
        self.rightFrame.grid_rowconfigure(0, weight=1)
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightCanvas.config(xscrollcommand=self.rightHScroll.set, yscrollcommand=self.rightVScroll.set)

    #矩形の位置が決定したときに呼び出される関数
    def PointRec(self, canvas : PDFCanvas, nPage, recPoints : fitz.Rect, text):
        if self.first is None:
            #最初なので情報を保持する
            self.first = (canvas, nPage, recPoints, text)
            canvas.disable()
            if canvas == self.leftCanvas:
                self.rightCanvas.enable()
            else:
                self.leftCanvas.enable()
        else:
            if self.nextIdx < self.matLB.getItemCount():
                #対象のインデックスがアイテム数より小さい場合は変更の時
                #後から登録された情報だけ更新すればいい
                texts = self.matLB.getItemText(self.nextIdx)
                if canvas == self.leftCanvas:
                    self.matLB.updateItem(self.nextIdx,
                                          self.pointText(nPage, recPoints),
                                          self.transText(-1, text),
                                          texts[2], texts[3])
                    self.matlist.updateData(self.nextIdx, 0, nPage, recPoints)
                    self.compareText(text, nPage, recPoints, self.first[3], self.first[1], self.first[2])
                else:
                    self.matLB.updateItem(self.nextIdx,
                                          texts[0], texts[1],
                                          self.pointText(nPage, recPoints),
                                          self.transText(-1, text))
                    self.matlist.updateData(self.nextIdx, 1, nPage, recPoints)
                    self.compareText(self.first[3], self.first[1], self.first[2], text, nPage, recPoints)
            else:
                #対象のインデックスがアイテム数と同じは新規追加
                if self.first[0] == self.leftCanvas:
                    #左側が先に来ていた
                    self.matlist.addData(self.first[1], self.first[2], nPage, recPoints)
                    self.addListBox(self.first[1], self.first[2], nPage, recPoints, self.first[3], text)
                else:
                    #右側が先に来ていた
                    self.matlist.addData(nPage, recPoints, self.first[1], self.first[2])
                    self.addListBox(nPage, recPoints, self.first[1], self.first[2], text, self.first[3])
            #登録・更新が終わったので初期状態にする
            self.first = None
            self.leftCanvas.enable()
            self.rightCanvas.enable()
            #次のインデックス番号をキャンバスへセットする
            self.nextIdx = self.matLB.getItemCount()
            self.leftCanvas.updaterectIndex(self.nextIdx)
            self.rightCanvas.updaterectIndex(self.nextIdx)
    
    #矩形が削除された
    def PointCancel(self, canvas : PDFCanvas, nIndex):
        bResult = True
        if self.nextIdx == nIndex:
            #現在登録中の矩形がキャンセルになった
            texts = self.matLB.getItemText(nIndex)
            for text in texts:
                if text == "":
                    #リストボックスのアイテムに空欄があるということは、先ほど片割れが削除されたことになるので、
                    #リストアイテムを削除する
                    self.matLB.deleteItem(nIndex)
                    self.matlist.deleteData(nIndex)
                    self.update()
                    break
            self.first = None
            canvas.enable()
            #次のインデックス番号をキャンバスへセットする
            self.nextIdx = self.matLB.getItemCount()
            self.leftCanvas.updaterectIndex(self.nextIdx)
            self.rightCanvas.updaterectIndex(self.nextIdx)
        elif self.first == None:
            #登録済みの矩形がキャンセルになった
            texts = self.matLB.getItemText(nIndex)
            if len(texts) == 4:
                rectinfo = ""
                text = ""
                firstCanvas = None
                if canvas == self.leftCanvas:
                    #左がキャンセルになった
                    self.matLB.updateItem(nIndex, "", "", texts[2], texts[3])
                    rectinfo = texts[2]
                    text = texts[3]
                    firstCanvas = self.rightCanvas
                else:
                    #右がキャンセルになった
                    self.matLB.updateItem(nIndex, texts[0], texts[1], "", "")
                    rectinfo = texts[0]
                    text = texts[1]
                    firstCanvas = self.leftCanvas
                #現在の仕掛中の矩形情報を更新する
                parts = rectinfo.split(":")
                nPage = int(parts[0].strip())
                # 残りの部分をカンマで分割して、それぞれを浮動小数点数に変換
                rect = [float(num.strip()) for num in parts[1].split(",")]
                self.first = (firstCanvas, nPage, fitz.Rect(rect[0], rect[1], rect[2], rect[3]), text)
                firstCanvas.changeRectColor(nPage, fitz.Rect(rect[0], rect[1], rect[2], rect[3]), CONST.COLOR_SEL)
                #編集対象のインデックスを更新する削除した側のキャンバスを有効にして、反対を無効にする
                self.nextIdx = nIndex
                canvas.updaterectIndex(self.nextIdx)
                canvas.enable()
                firstCanvas.disable()
        else:
            bResult = False
            #矩形の登録中に他の矩形を削除できない
            messagebox.showwarning('矩形の削除', '登録中は他の矩形を削除できません')
        return bResult

    #矩形の特殊指定
    def specifyRectInfo(self, canv : PDFCanvas, nPage, rect : fitz.Rect, spec, val):
        self.specRect[(canv, nPage, rect, spec)] = val
        if spec == CONST.SR_COLOR:
            canv.changeRectColor(nPage, rect, val)
            if self.leftCanvas == canv:
                nVersPage, rVersRect = self.matlist.getVersusData(0, nPage, rect)
                if nVersPage is not None:
                    self.rightCanvas.changeRectColor(nVersPage, rVersRect, val)
            else:
                nVersPage, rVersRect = self.matlist.getVersusData(1, nPage, rect)
                if nVersPage is not None:
                    self.leftCanvas.changeRectColor(nVersPage, rVersRect, val)
        elif spec == CONST.SR_TAGORI:
            pass #既に変更されているのですることは無し

    #リストに表示するページ番号と座標情報の文字列を出力する
    def pointText(self, nPage, rect : fitz.Rect):
        return f'{nPage}:{rect.x0}, {rect.y0}, {rect.x1}, {rect.y1}'

    #リストへ要素を追加する
    def addListBox(self, nleftPNum, leftRect : fitz.Rect, nrightPNum, rightRect : fitz.Rect, stLeft='', stRight=''):
        stleftpt = self.pointText(nleftPNum, leftRect)
        strightpt = self.pointText(nrightPNum,rightRect)
        self.matLB.addItem(stleftpt, self.transText(-1, stLeft), strightpt, self.transText(-1, stRight))
        self.compareText(stLeft, nleftPNum, leftRect, stRight, nrightPNum, rightRect)

    #矩形で囲われた文字列を比較して一致なら矩形の線の色を変更する
    def compareText(self, text1, page1, rect1, text2, page2, rect2):
        bResult = True
        setColor = CONST.COLOR_MATCH
        #全て数字の場合は先頭の0について削除した文字列に変換する
        textA = self.remove_leading_zeros(self.transText(-1, text1))
        textB = self.remove_leading_zeros(self.transText(-1, text2))
        #桁区切りのカンマを削除する
        textA = self.remove_digit_commas(textA)
        textB = self.remove_digit_commas(textB)
        if textA != textB:
            setColor = CONST.COLOR_MIS    #テキストが不一致なので不一致の枠線にする
            bResult = False
        self.leftCanvas.changeRectColor(page1, rect1, setColor)
        self.rightCanvas.changeRectColor(page2, rect2, setColor)
        return bResult

    #クリップボードへコピー
    def copyClipbord(self):
        #イメージを取得する
        image1 : Image = None
        image2 : Image = None
        image1 = self.leftCanvas.getCanvasImage()
        image2 = self.rightCanvas.getCanvasImage()
        if image1 is None or image2 is None:
            messagebox.showwarning('クリップボード', 'コピーできませんでした')
            return
        height = max(image1.height, image2.height)
        image1 = image1.resize((int(image1.width * (height / image1.height)), height), Image.Resampling.LANCZOS)
        image2 = image2.resize((int(image2.width * (height / image2.height)), height), Image.Resampling.LANCZOS)

        # 画像を左右に結合
        total_width = image1.width + image2.width
        new_image = Image.new("RGB", (total_width, height))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1.width, 0))

        output = io.BytesIO()
        new_image.save(output, format="BMP")  # BMP形式に変換
        data = output.getvalue()[14:]  # BMPヘッダーの先頭14バイトを除去
        output.close()

        # クリップボードを操作
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        messagebox.showinfo('クリップボード', 'コピーしました')

    #マッチ情報をクリアする
    def clearmat(self, MatClear = True):
        self.mat_entry.delete(0, tk.END)
        self.matLB.removeAll()
        if MatClear:
            self.matlist.clearData()
        self.specRect.clear()
        #キャンバスの矩形も削除する
        self.leftCanvas.removeAllRect()
        self.rightCanvas.removeAllRect()
        self.nextIdx = 0
        self.leftCanvas.updaterectIndex(self.nextIdx)
        self.rightCanvas.updaterectIndex(self.nextIdx)

    #matファイルの選択
    def selectmatfile(self):
        #ファイル選択ダイアログを開いてmatファイルを選択
        file_path = filedialog.askopenfilename(filetypes=[("mat files", "*.mat")])
        if file_path:
            if self.matlist.loafMatFile(file_path):
                self.clearmat(False)
                self.matLB.removeAll()
                self.mat_entry.delete(0, tk.END)
                self.mat_entry.insert(0, file_path)
                for i in range(self.matlist.getDataCount()):
                    lp, lpoint, rp, rpoint = self.matlist.getData(i)
                    self.addListBox(lp, lpoint, rp, rpoint, '', '')
                self.update()
            else:
                messagebox.showerror("ファイルエラー", '指定されたファイルが開けません')

    #matファイルの上書き保存
    def savematfile(self):
        if self.mat_entry.get() == '':
            self.renamesavematfile()
        else:
            self.matlist.saveMatFile(self.mat_entry.get())

    #matファイルの名前つけて保存
    def renamesavematfile(self):
        # ファイル保存ダイアログを開く
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mat",  # デフォルトの拡張子
            filetypes=[("mat files", "*.mat")],  # ファイルの種類
            title="名前を付けて保存")
        if file_path:
            if self.matlist.saveMatFile(file_path):
                self.mat_entry.delete(0, tk.END)
                self.mat_entry.insert(0, file_path)
            else:
                messagebox.showerror("ファイルエラー", '指定されたファイルに保存できません')

    #左PDFファイルの表示関連
    def selectleftpdf(self):
        #ファイル選択ダイアログを開いてmatファイルを選択
        file_path = filedialog.askopenfilename(filetypes=[("pdf files", "*.pdf")])
        if file_path:
            self.leftpdf_entry.delete(0, tk.END) 
            self.leftpdf_page_entry.delete(0, tk.END)
            self.leftCanvas.removeAllRect()
            self.specRect.clear()
            if self.leftCanvas.load_pdf(file_path):
                self.leftpdf_entry.insert(0, file_path)
                self.leftpdf_page_entry.insert(0, '1')
                self.update()
    #左PDFのページアップ
    def pageupleftpdf(self):
        if self.leftpdf_page_entry.get() != '':
            result = self.movePage(self.leftCanvas, self.leftpdf_page_entry.get(), -1)
            if result != self.leftpdf_page_entry.get():
                self.updateCanvas(self.leftCanvas)
                self.leftpdf_page_entry.delete(0, tk.END)
                self.leftpdf_page_entry.insert(0, result)
    #左PDFのページダウン
    def pagedownleftpdf(self):
        if self.leftpdf_page_entry.get() != '':
            result = self.movePage(self.leftCanvas, self.leftpdf_page_entry.get(), 1)
            if result != self.leftpdf_page_entry.get():
                self.updateCanvas(self.leftCanvas)
                self.leftpdf_page_entry.delete(0, tk.END)
                self.leftpdf_page_entry.insert(0, result)
    #左ページ表示のエンターキー
    def on_left_changepage(self, event):
        if self.leftpdf_page_entry.get() != '':
            result = self.movePage(self.leftCanvas, self.leftpdf_page_entry.get(), 0)
            #エンターキーの場合はresultと同じ数字ならページ移動成功ということで更新する
            if result == self.leftpdf_page_entry.get(): 
                self.updateCanvas(self.leftCanvas)
            self.leftpdf_page_entry.delete(0, tk.END)
            self.leftpdf_page_entry.insert(0, result)

    #右PDFファイルの表示関連
    def selectrightpdf(self):
        #ファイル選択ダイアログを開いてmatファイルを選択
        file_path = filedialog.askopenfilename(filetypes=[("pdf files", "*.pdf")])
        if file_path:
            self.rightpdf_entry.delete(0, tk.END) 
            self.rightpdf_page_entry.delete(0, tk.END)
            self.rightCanvas.removeAllRect()
            self.specRect.clear()
            if self.rightCanvas.load_pdf(file_path):
                self.rightpdf_entry.insert(0, file_path)
                self.rightpdf_page_entry.insert(0, '1')
                self.update()
    #右PDFのページアップ
    def pageuprightpdf(self):
        if self.rightpdf_page_entry.get() != '':
            result = self.movePage(self.rightCanvas, self.rightpdf_page_entry.get(), -1)
            if result != self.rightpdf_page_entry.get():
                self.updateCanvas(self.rightCanvas)
                self.rightpdf_page_entry.delete(0, tk.END)
                self.rightpdf_page_entry.insert(0, result)
    #右PDFのページダウン
    def pagedownrightpdf(self):
        if self.rightpdf_page_entry.get() != '':
            result = self.movePage(self.rightCanvas, self.rightpdf_page_entry.get(), 1)
            if result != self.rightpdf_page_entry.get():
                self.updateCanvas(self.rightCanvas)
                self.rightpdf_page_entry.delete(0, tk.END)
                self.rightpdf_page_entry.insert(0, result)
    #右ページ表示のエンターキー
    def on_right_changepage(self, event):
        if self.rightpdf_page_entry.get() != '':
            result = self.movePage(self.rightCanvas, self.rightpdf_page_entry.get(), 0)
            if result == self.rightpdf_page_entry.get():
                self.updateCanvas(self.rightCanvas)
            self.rightpdf_page_entry.delete(0, tk.END)
            self.rightpdf_page_entry.insert(0, result)

    #指定されたキャンバスとページ数でページ移動するページ移動が成功したらそのページ番号を返却する
    def movePage(self, pcanv : PDFCanvas, stPage, nInc):
        #指定ページを文字列にする
        nPage = int(stPage)
        if nPage + nInc == 0 or nPage + nInc > pcanv.getPageCount():
            #現在のページ番号を取得する
            nNowPage = pcanv.getPageNum()
            return str(nNowPage)
        pcanv.movePage(nPage + nInc)
        return str(nPage + nInc)
    
    #キャンバスへ矩形情報を登録する
    def update(self):
        if self.matlist.getDataCount() > 0 and self.leftCanvas.isLoadPDF() and self.rightCanvas.isLoadPDF():
            self.leftCanvas.removeAllRect()
            self.rightCanvas.removeAllRect()
            for i in range(self.matlist.getDataCount()):
                lp, lpoint, rp, rpoint = self.matlist.getData(i)
                self.leftCanvas.updaterectIndex(i)
                self.rightCanvas.updaterectIndex(i)
                textL = self.leftCanvas.addRectangle(lp, lpoint[0], lpoint[1], lpoint[2], lpoint[3])
                textR = self.rightCanvas.addRectangle(rp, rpoint[0], rpoint[1], rpoint[2], rpoint[3])
                self.matLB.updateItem(i, self.pointText(lp, lpoint), self.transText(i, textL), self.pointText(rp, rpoint), self.transText(i, textR))
                self.compareText(textL, lp, lpoint, textR, rp, rpoint)

            self.nextIdx = self.matlist.getDataCount() #反映が終わったら次のインデックスを更新する
            self.leftCanvas.updaterectIndex(self.nextIdx)
            self.rightCanvas.updaterectIndex(self.nextIdx)
            self.updateSpecRect()
    
    #現在のページへ矩形情報をセットする
    def updateCanvas(self, canv : PDFCanvas):
        for i in range(self.matlist.getDataCount()):
            lp, lpoint, rp, rpoint = self.matlist.getData(i)
            if canv == self.leftCanvas:
                if lp == self.leftCanvas.getPageNum():
                    self.leftCanvas.updaterectIndex(i)
                    self.leftCanvas.addRectangle(lp, lpoint[0], lpoint[1], lpoint[2], lpoint[3])
                    texts = self.matLB.getItemText(i)
                    self.compareText(texts[1], lp, lpoint, texts[3], rp, rpoint)
            else:
                if rp == self.rightCanvas.getPageNum():
                    self.rightCanvas.updaterectIndex(i)
                    self.rightCanvas.addRectangle(rp, rpoint[0], rpoint[1], rpoint[2], rpoint[3])
                    texts = self.matLB.getItemText(i)
                    self.compareText(texts[1], lp, lpoint, texts[3], rp, rpoint)
        self.updateSpecRect()
        #現在選択中のインデックスに直す
        canv.updaterectIndex(self.nextIdx)

    #特殊指定の矩形について反映する
    def updateSpecRect(self):
        for (canv, nPage, rect, spec), val in self.specRect.items():
            if spec == CONST.SR_COLOR:
                canv.changeRectColor(nPage, rect, val)
                if self.leftCanvas == canv:
                    nVers = self.matlist.getVersusData(0, nPage, rect)
                    if nVers is not None:
                        self.rightCanvas.changeRectColor(nVers[0], nVers[1], val)
                else:
                    nVers = self.matlist.getVersusData(1, nPage, rect)
                    if nVers is not None:
                        self.leftCanvas.changeRectColor(nVers[0], nVers[1], val)
            elif spec == CONST.SR_TAGORI:
                canv.moveNumberTag(nPage, rect, val)

    #抽出した文字列の変換
    def transText(self, matIndex, text : str):
        result = ''
        result = text.replace('\n', '').replace(' ', '').replace('　', '')
        return result

    def remove_leading_zeros(self, input_string):
        # 文字列が数字で構成されているかチェック
        if input_string.isdigit():
            return str(int(input_string))  # 数値に変換して戻すことで先頭の0を削除
        return input_string  # 数字でない場合はそのまま返す        

    def remove_digit_commas(self, input_string):
        pattern = r'^[0-9,]*$'  # 数字とカンマのみ許可
        if bool(re.match(pattern, input_string)):
            return input_string.replace(',', '')
        return input_string


#メインループ
if __name__ == "__main__":
    #アプリを起動する
    app = CompareLedger()
    app.update_idletasks()
    app.mainloop()

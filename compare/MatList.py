import fitz  # PyMuPDF
import json

###################################################################
#   JSON型のキー名
###################################################################
LKEY = 'left'
RKEY = 'right'
PKEY = 'page'
XORI = 'x1'
YORI = 'y1'
XEND = 'x2'
YEND = 'y2'

###################################################################
#   MatListクラス
###################################################################
class MatList:
    #初期化
    def __init__(self):
        self.mats = []      #左右のページ番号と座標を持つリスト

    #ファイルの保存
    def saveMatFile(self, stFilePath):
        try:
            with open(stFilePath, 'w') as json_file:
                json.dump(self.mats, json_file, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save JSON: {e}")
            return False

    #ファイルのロード
    def loafMatFile(self, stFilePath):
        try:
            with open(stFilePath, 'r') as json_file:
                self.mats = json.load(json_file)
                if isinstance(self.mats, list):
                    return True
                else:
                    print("The JSON data is not a list.")
                    return False
        except Exception as e:
            print(f"Failed to load JSON: {e}")
            return False

    #リストの個数を返却する
    def getDataCount(self):
        return len(self.mats)

    #要素の追加 追加が成功したらインデックスを返却する
    def addData(self, nleftPage, leftRect : fitz.Rect, nrightPage, rightRect : fitz.Rect):
        mat = {}
        mat[LKEY] = {PKEY:nleftPage, XORI:leftRect.x0, YORI:leftRect.y0, XEND:leftRect.x1, YEND:leftRect.y1}
        mat[RKEY] = {PKEY:nrightPage, XORI:rightRect.x0, YORI:rightRect.y0, XEND:rightRect.x1, YEND:rightRect.y1}
        self.mats.append(mat)
        return len(self.mats) - 1
    
    #要素の全削除
    def clearData(self):
        self.mats = []
        
    #要素の削除
    def deleteData(self, nIndex):
        if nIndex < len(self.mats):
            self.mats.pop(nIndex)

    #要素の更新 nSideは左側が0　右側が1を指定する
    def updateData(self, nIndex, nSide, nPage, newRect : fitz.Rect):
        if nIndex < len(self.mats):
            mat = self.mats[nIndex]
            info = {}
            if nSide == 0:
                info = mat[LKEY]
            else:
                info = mat[RKEY]
            info[PKEY] = nPage
            info[XORI] = newRect.x0
            info[YORI] = newRect.y0
            info[XEND] = newRect.x1
            info[YEND] = newRect.y1

    #要素の取得 左右のページ番号と座標を返却する
    def getData(self, nIndex):
        if nIndex < len(self.mats):
            mat = self.mats[nIndex]
            lrect = fitz.Rect(mat[LKEY][XORI], mat[LKEY][YORI], mat[LKEY][XEND], mat[LKEY][YEND])
            rrect = fitz.Rect(mat[RKEY][XORI], mat[RKEY][YORI], mat[RKEY][XEND], mat[RKEY][YEND])
            return mat[LKEY][PKEY], lrect, mat[RKEY][PKEY], rrect
        return None

    #ページと矩形と側で対となる情報を返却する
    #nPage=1, rect=fitz.Rect, side=left ならば右のページと矩形座標を返却する
    def getVersusData(self, nSide, nPage, rect : fitz.Rect):
        searchinfo = {}
        result = {}
        for index, mat in enumerate(self.mats, start=0):
            if nSide == 0:
                searchinfo = mat[LKEY]
                result = mat[RKEY]
            else:
                searchinfo = mat[RKEY]
                result = mat[LKEY]
            if searchinfo[PKEY] == nPage and \
                searchinfo[XORI] == rect.x0 and searchinfo[YORI] == rect.y0 and \
                searchinfo[XEND] == rect.x1 and searchinfo[YEND] == rect.y1:
                return index, result[PKEY], fitz.Rect(result[XORI],result[YORI],result[XEND],result[YEND])
        return None

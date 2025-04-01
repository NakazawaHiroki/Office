Attribute VB_Name = "Utility"
'===============================================================================
' VBAの汎用的な関数
'===============================================================================

'===============================================================================
' 指定したセルの文字列がファイルパスとして適切かチェックして文字列を返却します
' target: セルの座標　※必ず一つのセルを指定してください
' msg:エラーメッセージの前半部分　この文字列の後に「の指定がありません」がつきます
' return:セルの文字列が返却される、ファイルが無いときは空文字列""が返却されます
'===============================================================================
Function GetFilePath_util(target As Range, msg As String) As String
    Dim path As String
    Dim fso As Object
    path = target.value
    If path = "" Then
        MsgBox msg & "の指定がありません"
        GetFilePath_util = ""
        Exit Function
    End If
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' 指定されたパスのファイルが存在するかを確認
    If Not fso.FileExists(path) Then
        MsgBox msg & "のファイルがありません"
        GetFilePath_util = ""
        Exit Function
    End If
    
    ' FileSystemObjectのクリーンアップ
    Set fso = Nothing
    GetFilePath_util = path
End Function

'===============================================================================
' エクセルファイルを選択するファイルダイアログを表示します
' targetRange: 選択されたファイルを入力するセルの座標　※必ず一つのセル
' dialogTitle: ダイアログに表示するタイトル
'===============================================================================
Function SelectXLSXFile_util(targetRange As Range, dialogTitle As String)
    Dim fd As FileDialog
    Dim selectedFilePath As String
    
    ' ファイルダイアログの初期化
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    
    ' ダイアログの設定
    With fd
        .title = dialogTitle
        .Filters.Clear
        .Filters.Add "エクセルファイル", "*.xlsx"
        .AllowMultiSelect = False
        
        ' ダイアログを表示し、選択されたファイルを取得
        If .Show = -1 Then  ' ユーザーがファイルを選択した場合
            selectedFilePath = .SelectedItems(1)
            ' 選択されたファイルパスを指定されたセルに表示
            targetRange.value = selectedFilePath
        End If
    End With
    
    ' オブジェクトのクリーンアップ
    Set fd = Nothing
End Function

'===============================================================================
' CSVファイルを選択するファイルダイアログを表示します
' targetRange: 選択されたファイルを入力するセルの座標　※必ず一つのセル
' dialogTitle: ダイアログに表示するタイトル
' onlyCSV: True=CSVファイルのフィルターを付ける、False=全てのファイルだけ
'===============================================================================
Function SelectCSVFile_util(targetRange As Range, dialogTitle As String, onlyCSV As Boolean)
    Dim fd As FileDialog
    Dim selectedFilePath As String
    
    ' ファイルダイアログの初期化
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    
    ' ダイアログの設定
    With fd
        .title = dialogTitle
        .Filters.Clear
        If onlyCSV Then
            .Filters.Add "CSVファイル", "*.csv"
        End If
        .Filters.Add "すべてのファイル", "*.*"
        .AllowMultiSelect = False
        
        ' ダイアログを表示し、選択されたファイルを取得
        If .Show = -1 Then  ' ユーザーがファイルを選択した場合
            selectedFilePath = .SelectedItems(1)
            ' 選択されたファイルパスを指定されたセルに表示
            targetRange.value = selectedFilePath
        End If
    End With
    
    ' オブジェクトのクリーンアップ
    Set fd = Nothing
End Function


'===============================================================================
' フォルダ選択ダイアログを表示します
' dialogTitle: ダイアログのタイトル
' Return: 選択されたフォルダのパス　キャンセルの場合は空文字列""を返却します
'===============================================================================
Function SelectFolder_util(dialogTitle As String) As String
    Dim folderDialog As FileDialog
    Dim selectedFolderPath As String
    
    ' フォルダ選択ダイアログを作成
    Set folderDialog = Application.FileDialog(msoFileDialogFolderPicker)
    
    ' ダイアログの設定
    With folderDialog
        .title = dialogTitle       ' ダイアログのタイトルを設定
        .AllowMultiSelect = False   ' フォルダの複数選択を無効にする
        
        ' ダイアログを表示し、フォルダが選択された場合はパスを取得
        If .Show = -1 Then
            selectedFolderPath = .SelectedItems(1)
        Else
            selectedFolderPath = "" ' フォルダが選択されなかった場合は空の文字列
        End If
    End With
    
    ' 戻り値を設定
    SelectFolder_util = selectedFolderPath
    
    ' オブジェクトのクリーンアップ
    Set folderDialog = Nothing
End Function


'===============================================================================
'複数ファイルを選択できるダイアログを表示する
' targetRange: 選択したファイルを表示するセルの範囲
' addCSVFilter: CSVファイルのフィルタを付けるかの指定
' title: ダイアログタイトル
'===============================================================================
Function SelectMultipleFiles_util(targetRange As Range, Optional addCSVFilter As Boolean = False, Optional title As String = "ファイルを選択してください")
    Dim fd As FileDialog
    Dim selectedFilePath As String
    Dim i As Integer

    ' ファイルダイアログの初期化
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    
    ' ダイアログの設定
    With fd
        .title = title
        .AllowMultiSelect = True       ' 複数ファイルの選択を許可
        .Filters.Clear                 ' 既存のフィルターをクリア
        If addCSVFilter Then
            .Filters.Add "CSVファイル", "*.csv"
        End If
        .Filters.Add "すべてのファイル", "*.*"
        ' ダイアログを表示し、選択されたファイルを取得
        If .Show = -1 Then
            ' 選択されたファイルパスを指定したセル範囲に表示
            If targetRange.count < .SelectedItems.count Then
                MsgBox "選択したセルよりもファイル数が多いです " & targetRange.address
                Set fd = Nothing
                Exit Function
            End If
            targetRange.ClearContents  ' 範囲をクリア
            For i = 1 To .SelectedItems.count
                targetRange.Cells(i, 1).value = .SelectedItems(i)
            Next i
        End If
    End With
    ' オブジェクトのクリーンアップ
    Set fd = Nothing
End Function


'===============================================================================
' CSVファイルを読み込んでString配列を格納したCollectionオブジェクトを返却します
' filePath: ＣＳＶファイルのパス
' Return: Collectionオブジェクト ファイルが無い、読めない時はNothingを返却します
'===============================================================================
Function LoadCSV_util(filePath As String) As Collection
    Dim csvFile As Object
    Dim line As String
    Dim lineArray As Variant
    Dim rowCollection As Collection
    Dim fso As Object
    
    ' Collectionオブジェクトの初期化
    Set rowCollection = New Collection
    
    ' ファイルシステムオブジェクトの作成
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' ファイルが存在するか確認
    If Not fso.FileExists(filePath) Then
        MsgBox "指定されたファイルが見つかりません: " & filePath, vbExclamation
        Set LoadCSV_util = Nothing
        Exit Function
    End If
    
    ' ファイルを開く
    Set csvFile = fso.OpenTextFile(filePath, 1)
    
    ' 各行を読み込み、配列に変換してCollectionに追加
    csvFile.ReadLine    '1行目はヘッダーとしてスキップする
    Do Until csvFile.AtEndOfStream
        line = csvFile.ReadLine
        ' カンマ区切りで文字列を配列に変換
        lineArray = SplitCSV_util(line)
        ' Collectionに配列を追加
        rowCollection.Add lineArray
    Loop
    
    ' ファイルを閉じる
    csvFile.Close
    
    ' Collectionを返す
    Set LoadCSV_util = rowCollection
End Function

'===============================================================================
' シートから指定されたふたつの列をキーと値としてDictionary型で返却する
' sheetName: 読込先のシート名
' startRow: 読み込みを開始する行番号
' keyColumn: キーとなるセルの列番号
' valueColumn: 値となるセルの列番号
' Return: Dictionary型で返却する、シートが無いときはNotihngを返却する
'===============================================================================
Function GetDictiFromSheet_util(sheetName As String, startRow As Long, keyColumn As Long, valueColumn As Long) As Object
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim dataArr As Variant
    Dim rowDict As Object
    Dim i As Long
    Dim key As Variant
    Dim value As Variant
    
    ' ---- 初期化 ----
    Set rowDict = CreateObject("Scripting.Dictionary")
    
    ' ---- シートの存在確認 ----
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(sheetName)
    On Error GoTo 0
    If ws Is Nothing Then
        Set GetDictiFromSheet_util = Nothing ' シートが見つからない場合はNothingを返す
        Exit Function
    End If
    
    ' ---- 最終行を取得 ----
    lastRow = ws.Cells(ws.Rows.count, keyColumn).End(xlUp).row
    If lastRow < startRow Then
        Set GetDictionaryFromSheet = rowDict ' データが存在しない場合は空のDictionaryを返す
        Exit Function
    End If
    
    ' ---- データ範囲を配列に読み込む ----
    dataArr = ws.Range(ws.Cells(startRow, keyColumn), ws.Cells(lastRow, valueColumn)).value
    
    ' ---- Dictionaryにデータを格納 ----
    For i = 1 To UBound(dataArr, 1)
        key = dataArr(i, 1) ' 配列内でのキーの列
        value = dataArr(i, 2) ' 配列内での値の列
        
        ' キーが重複していないか確認
        If Not rowDict.Exists(key) Then
            rowDict.Add CStr(key), value
        Else
            ' キーの重複がある場合、必要に応じて処理を変更可能
            ' 現在は無視して次に進む
        End If
    Next i
    
    ' ---- 結果を返す ----
    Set GetDictiFromSheet_util = rowDict
End Function


'===============================================================================
' ダブルコーテーションを含むCSV文字列をString配列に変換する
' inputText: カンマ区切りの文字列　ダブルコーテーションも含む
' Return: AA,"BB",CC,"D,D",EE => AA | BB | CC | D,D | EE  という配列で返却
'===============================================================================
Function SplitCSV_util(inputText As String) As Variant
    Dim elements As Collection
    Set elements = New Collection
    
    Dim i As Integer
    Dim currentElement As String
    Dim inQuotes As Boolean
    
    currentElement = ""
    inQuotes = False
    
    For i = 1 To Len(inputText)
        Dim currentChar As String
        currentChar = Mid(inputText, i, 1)
        
        Select Case currentChar
            Case """"
                ' ダブルクォーテーションをトグル
                inQuotes = Not inQuotes
            Case ","
                If inQuotes Then
                    ' ダブルクォーテーション内のカンマは要素として扱う
                    currentElement = currentElement & currentChar
                Else
                    ' ダブルクォーテーション外のカンマは要素の区切りとして扱う
                    elements.Add currentElement
                    currentElement = ""
                End If
            Case Else
                ' 通常の文字を追加
                currentElement = currentElement & currentChar
        End Select
    Next i
    
    ' 最後の要素を追加
    elements.Add currentElement
    
    ' Collectionを配列に変換して返却
    Dim result() As String
    ReDim result(1 To elements.count)
    For i = 1 To elements.count
        result(i) = elements(i)
    Next i

    SplitCSV_util = result
End Function


'===============================================================================
' 指定したエクセルファイルをCollectionオブジェクトとして返却する
' filePath: 読み込むエクセルファイル
' sheetIndex: 読み込むシートのインデックス
' Return: 読み込んだコレクションオブジェクト、読み込めなければNothingを返却する
'===============================================================================
Function LoadExcel_util(filePath As String, sheetIndex As Integer) As Collection
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim rowCollection As Collection
    Dim rowArray As Variant
    Dim lastRow As Long, lastCol As Long
    Dim i As Long, j As Long
    
    ' Collectionオブジェクトを初期化
    Set rowCollection = New Collection
    
    ' ファイルの存在確認
    If Dir(filePath) = "" Then
        MsgBox "指定されたファイルが見つかりません: " & filePath, vbExclamation
        Set LoadExcel_util = Nothing
        Exit Function
    End If
    
    ' ファイルを開く
    Application.ScreenUpdating = False
    Set wb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' シートの存在確認
    If sheetIndex < 1 Or sheetIndex > wb.Sheets.count Then
        MsgBox "指定されたシートインデックスが無効です: " & sheetIndex, vbExclamation
        wb.Close False
        Set LoadExcel_util = Nothing
        Exit Function
    End If
    
    ' 指定されたシートを取得
    Set ws = wb.Sheets(sheetIndex)
    
    ' データ範囲の最終行と最終列を取得
    lastRow = ws.Cells(ws.Rows.count, 1).End(xlUp).row
    lastCol = ws.Cells(1, ws.Columns.count).End(xlToLeft).Column
    
    ' 各行をString配列としてCollectionに追加
    For i = 1 To lastRow
        ReDim rowArray(1 To lastCol)
        
        For j = 1 To lastCol
            rowArray(j) = CStr(ws.Cells(i, j).value) ' 各セルの値を文字列として取得
        Next j
        
        rowCollection.Add rowArray
    Next i
    
    ' ファイルを閉じて結果を返す
    wb.Close False
    Application.ScreenUpdating = True
    Set LoadExcel_util = rowCollection
End Function


'===============================================================================
' 日付らしい文字列を西暦に変換する
' dateString: 変換する文字列 例: "令和XX年XX月XX日", "RXX.XX.XX", "XXXX年XX月XX日"
' Return: yyyy/mm/ddの形式にして返却する 変換できなければ空文字列""を返却する
'===============================================================================
Function ConvertDate_util(dateString As String) As String
    Dim result As Date
    Dim temp As String
    
    On Error Resume Next
        result = CDate(dateString)
    On Error GoTo 0
    
    If result = 0 Then
        'R6.10.10などの形式があるかもしれないので、変換して再試行
        temp = Replace(dateString, ".", "/")
        On Error Resume Next
            result = CDate(temp)
        On Error GoTo 0
    End If
    
    If result = 0 Then
        ConvertDate_util = ""
    Else
        ConvertDate_util = Format(result, "yyyy/mm/dd")
    End If
End Function


'===============================================================================
' 文字列の配列をチェックして空だったらエラーメッセージを表示する
' subject: チェックする文字列の配列
' msg: エラーメッセージに表示する先頭の文字列　例："XXXXXXXを入力してください"
' Return: True=何も入っていないエラーメッセージが表示された False=配列に何かの文字列がある
'===============================================================================
Function IsEmptyArray_util(subject As Variant, msg As String) As Boolean
    If IsNull(subject) Then
        MsgBox msg & " を入力してください"
        IsEmptyArray_util = True
        Exit Function
    End If
    If IsArray(subject) Then
        ' 配列の要素数を確認
        If (UBound(subject) - LBound(subject) + 1) = 0 Then
            MsgBox msg & " を入力してください"
            IsEmptyArray_util = True
            Exit Function
        End If
    Else
        MsgBox msg & " を入力してください"
        IsEmptyArray_util = True
        Exit Function
    End If
    
    For i = LBound(subject) To UBound(subject)
        If subject(i) <> "" Then
            IsEmptyArray_util = False
            Exit Function
        End If
    Next i
    IsEmptyArray_util = True
    MsgBox msg & " を入力してください"
End Function


'===============================================================================
' 指定した範囲のセルから値を取得して配列にして返却する
' rng: 配列にしたいセルの範囲
' includeBlanks: 空白のセルも配列に含めるかのチェック True=含める　False=含めない
' Return: 文字配列を返却、値が全くない時はNullを返却する
'===============================================================================
Function GetValuesAsArray_util(rng As Range, includeBlanks As Boolean) As Variant
    Dim cell As Range
    Dim result As Collection
    Set result = New Collection
    
    ' セルの値をコレクションに追加
    For Each cell In rng
        If includeBlanks Or cell.value <> "" Then
            result.Add CStr(cell.value)
        End If
    Next cell
    ' 値がない場合はNullを返す
    If result.count = 0 Then
        GetValuesAsArray_util = Null
    Else
        ' コレクションを配列に変換して返す
        Dim arr() As String
        ReDim arr(0 To result.count - 1)
        
        Dim i As Integer
        For i = 1 To result.count
            arr(i - 1) = result(i)
        Next i
        GetValuesAsArray_util = arr
    End If
End Function


'===============================================================================
' 指定したフォルダとサブフォルダからファイルを検索してファイル名か絶対パスの配列を返却する
' folderPath:検索先のフォルダパス
' fileExtension: 検索する拡張子　例："csv", "txt"
' returnFullPath: 絶対パスを返却するかのフラグ　True:絶対パス　False:ファイル名だけ
' Return: Collectionを返却する
'===============================================================================
Function SearchFiles_util(folderPath As String, fileExtension As String, returnFullPath As Boolean) As Collection
    Dim fso As Object
    Dim folder As Object
    Dim subFolder As Object
    Dim file As Object
    Dim result As New Collection

    ' FileSystemObjectを作成
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' フォルダの存在確認
    If Not fso.FolderExists(folderPath) Then
        MsgBox "指定されたフォルダが見つかりません: " & folderPath, vbExclamation
        Set SearchFiles_util = Nothing
        Exit Function
    End If
    
    ' フォルダオブジェクトを取得
    Set folder = fso.GetFolder(folderPath)
    
    ' 指定フォルダ内のファイルを検索
    For Each file In folder.Files
        If LCase(fso.GetExtensionName(file)) = LCase(fileExtension) Then
            If returnFullPath Then
                result.Add file.path   ' 絶対パスを追加
            Else
                result.Add file.Name   ' ファイル名のみを追加
            End If
        End If
    Next file
    
    ' サブフォルダ内のファイルを再帰的に検索
    Dim temp As String
    For Each subFolder In folder.Subfolders
        Dim subResult As Collection
        Set subResult = SearchFiles_util(subFolder.path, fileExtension, returnFullPath)
        If Not subResult Is Nothing Then
            Dim item As Variant
            For Each item In subResult
                result.Add item
            Next item
        End If
    Next subFolder

    ' 結果を返す
    Set SearchFiles_util = result
End Function

'===============================================================================
' 文字列を指定のバイト数で切り詰めて返却する
' inputStr:カットする文字列
' byteLength: 切り詰めるバイト数
' Return: 文字列を返却　指定バイト数の文字が全角の1バイト目の時はその前の文字までを返却する
'===============================================================================
Function CutString_util(inputStr As String, byteLength As Long) As String
    Dim i As Long
    Dim currentByteLength As Long
    Dim cutPosition As Long
    Dim charByte As Long
    
    currentByteLength = 0
    cutPosition = 0
    
    For i = 1 To Len(inputStr)
        charByte = LenB(StrConv(Mid(inputStr, i, 1), vbFromUnicode))
        
        If currentByteLength + charByte > byteLength Then
            Exit For
        End If
        
        currentByteLength = currentByteLength + charByte
        cutPosition = i
    Next i
    
    CutString_util = Left(inputStr, cutPosition)
End Function

'===============================================================================
' シートのデータクリアする
' sheet: クリアするシート
' startRow: クリアする開始行
'===============================================================================
Sub ClearSheet_Util(sheet As Worksheet, startRow As Long)
    Dim lastRow As Long

    ' 最終行を取得
    lastRow = sheet.Cells(sheet.Rows.count, 1).End(xlUp).row

    ' 指定した行以降をクリア
    If startRow <= lastRow Then
        sheet.Rows(startRow & ":" & lastRow).ClearContents
    End If
End Sub

'===============================================================================
' 住所を都道府県町名、番地、方書に分解する
' strAddress: 分解する住所
' toZenkaku: True=全角に変換して出力　False=半角で出力
' return: 配列で返却する　都道府県町名,番地,方書
'===============================================================================
Function SplitAddress_util(strAddress As String, toZenkaku As Boolean) As Variant
    Dim townName As String
    Dim houseNumber As String
    Dim additionalInfo As String
    Dim match As Object
    Dim strCovert As String

    ' 正規表現オブジェクトを作成
    Dim regex As Object
    Set regex = CreateObject("VBScript.RegExp")

    ' 正規表現パターン（町名と番地の明確な分割）
    regex.pattern = "(.+[市区町村]*)\s*([0-9一-龠]+丁目[0-9一-龠-]*)\s*(.*)"
    If InStr(strAddress, "丁目") = 0 Then
        regex.pattern = "(.+[市区町村].*?[町村])\s*([0-9一-龠-]+)\s*(.*)"
    End If
    
    
    regex.Global = False
    regex.IgnoreCase = True

    strCovert = ConvertNumberWidth(strAddress, True)

    ' 正規表現で住所を分割
    If regex.test(strCovert) Then
        Set match = regex.Execute(strCovert)(0)

        ' グループ1: 町名
        townName = ConvertNumberWidth(Trim(match.SubMatches(0)), False)

        ' グループ2: 番地
        houseNumber = ConvertNumberWidth(Trim(match.SubMatches(1)), False)

        ' グループ3: 方書
        additionalInfo = ConvertNumberWidth(Trim(match.SubMatches(2)), False)
    Else
        townName = strAddress
        houseNumber = ""
        additionalInfo = ""
    End If

    ' 結果を表示
    If toZenkaku Then
        SplitAddress_util = Array(ConvertNumberWidth(townName, False), ConvertNumberWidth(houseNumber, False), ConvertNumberWidth(additionalInfo, False))
    Else
        SplitAddress_util = Array(townName, houseNumber, additionalInfo)
    End If
End Function

Function ConvertNumberWidth(inputStr As String, toHalfWidth As Boolean) As String
    Dim i As Long
    Dim c As String
    Dim result As String
    Dim fullWidthNumbers As Variant
    Dim halfWidthNumbers As Variant
    Dim j As Long
    Dim found As Boolean

    ' 全角・半角数字の配列を定義
    fullWidthNumbers = Array("０", "１", "２", "３", "４", "５", "６", "７", "８", "９", "－", "ー", "―", "‐")
    halfWidthNumbers = Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "-", "-", "-")
    
    result = ""

    ' 文字列を1文字ずつ処理
    For i = 1 To Len(inputStr)
        c = Mid(inputStr, i, 1)
        found = False
        
        If toHalfWidth Then
            ' 全角から半角へ変換
            For j = LBound(fullWidthNumbers) To UBound(fullWidthNumbers)
                If c = fullWidthNumbers(j) Then
                    c = halfWidthNumbers(j)
                    found = True
                    Exit For
                End If
            Next j
        Else
            ' 半角から全角へ変換
            For j = LBound(halfWidthNumbers) To UBound(halfWidthNumbers)
                If c = halfWidthNumbers(j) Then
                    c = fullWidthNumbers(j)
                    found = True
                    Exit For
                End If
            Next j
        End If

        ' 数字以外の文字はそのまま
        result = result & c
    Next i

    ConvertNumberWidth = result
End Function



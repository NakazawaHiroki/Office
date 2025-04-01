Attribute VB_Name = "Utility"
'===============================================================================
' VBA�̔ėp�I�Ȋ֐�
'===============================================================================

'===============================================================================
' �w�肵���Z���̕����񂪃t�@�C���p�X�Ƃ��ēK�؂��`�F�b�N���ĕ������ԋp���܂�
' target: �Z���̍��W�@���K����̃Z�����w�肵�Ă�������
' msg:�G���[���b�Z�[�W�̑O�������@���̕�����̌�Ɂu�̎w�肪����܂���v�����܂�
' return:�Z���̕����񂪕ԋp�����A�t�@�C���������Ƃ��͋󕶎���""���ԋp����܂�
'===============================================================================
Function GetFilePath_util(target As Range, msg As String) As String
    Dim path As String
    Dim fso As Object
    path = target.value
    If path = "" Then
        MsgBox msg & "�̎w�肪����܂���"
        GetFilePath_util = ""
        Exit Function
    End If
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' �w�肳�ꂽ�p�X�̃t�@�C�������݂��邩���m�F
    If Not fso.FileExists(path) Then
        MsgBox msg & "�̃t�@�C��������܂���"
        GetFilePath_util = ""
        Exit Function
    End If
    
    ' FileSystemObject�̃N���[���A�b�v
    Set fso = Nothing
    GetFilePath_util = path
End Function

'===============================================================================
' �G�N�Z���t�@�C����I������t�@�C���_�C�A���O��\�����܂�
' targetRange: �I�����ꂽ�t�@�C������͂���Z���̍��W�@���K����̃Z��
' dialogTitle: �_�C�A���O�ɕ\������^�C�g��
'===============================================================================
Function SelectXLSXFile_util(targetRange As Range, dialogTitle As String)
    Dim fd As FileDialog
    Dim selectedFilePath As String
    
    ' �t�@�C���_�C�A���O�̏�����
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    
    ' �_�C�A���O�̐ݒ�
    With fd
        .title = dialogTitle
        .Filters.Clear
        .Filters.Add "�G�N�Z���t�@�C��", "*.xlsx"
        .AllowMultiSelect = False
        
        ' �_�C�A���O��\�����A�I�����ꂽ�t�@�C�����擾
        If .Show = -1 Then  ' ���[�U�[���t�@�C����I�������ꍇ
            selectedFilePath = .SelectedItems(1)
            ' �I�����ꂽ�t�@�C���p�X���w�肳�ꂽ�Z���ɕ\��
            targetRange.value = selectedFilePath
        End If
    End With
    
    ' �I�u�W�F�N�g�̃N���[���A�b�v
    Set fd = Nothing
End Function

'===============================================================================
' CSV�t�@�C����I������t�@�C���_�C�A���O��\�����܂�
' targetRange: �I�����ꂽ�t�@�C������͂���Z���̍��W�@���K����̃Z��
' dialogTitle: �_�C�A���O�ɕ\������^�C�g��
' onlyCSV: True=CSV�t�@�C���̃t�B���^�[��t����AFalse=�S�Ẵt�@�C������
'===============================================================================
Function SelectCSVFile_util(targetRange As Range, dialogTitle As String, onlyCSV As Boolean)
    Dim fd As FileDialog
    Dim selectedFilePath As String
    
    ' �t�@�C���_�C�A���O�̏�����
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    
    ' �_�C�A���O�̐ݒ�
    With fd
        .title = dialogTitle
        .Filters.Clear
        If onlyCSV Then
            .Filters.Add "CSV�t�@�C��", "*.csv"
        End If
        .Filters.Add "���ׂẴt�@�C��", "*.*"
        .AllowMultiSelect = False
        
        ' �_�C�A���O��\�����A�I�����ꂽ�t�@�C�����擾
        If .Show = -1 Then  ' ���[�U�[���t�@�C����I�������ꍇ
            selectedFilePath = .SelectedItems(1)
            ' �I�����ꂽ�t�@�C���p�X���w�肳�ꂽ�Z���ɕ\��
            targetRange.value = selectedFilePath
        End If
    End With
    
    ' �I�u�W�F�N�g�̃N���[���A�b�v
    Set fd = Nothing
End Function


'===============================================================================
' �t�H���_�I���_�C�A���O��\�����܂�
' dialogTitle: �_�C�A���O�̃^�C�g��
' Return: �I�����ꂽ�t�H���_�̃p�X�@�L�����Z���̏ꍇ�͋󕶎���""��ԋp���܂�
'===============================================================================
Function SelectFolder_util(dialogTitle As String) As String
    Dim folderDialog As FileDialog
    Dim selectedFolderPath As String
    
    ' �t�H���_�I���_�C�A���O���쐬
    Set folderDialog = Application.FileDialog(msoFileDialogFolderPicker)
    
    ' �_�C�A���O�̐ݒ�
    With folderDialog
        .title = dialogTitle       ' �_�C�A���O�̃^�C�g����ݒ�
        .AllowMultiSelect = False   ' �t�H���_�̕����I���𖳌��ɂ���
        
        ' �_�C�A���O��\�����A�t�H���_���I�����ꂽ�ꍇ�̓p�X���擾
        If .Show = -1 Then
            selectedFolderPath = .SelectedItems(1)
        Else
            selectedFolderPath = "" ' �t�H���_���I������Ȃ������ꍇ�͋�̕�����
        End If
    End With
    
    ' �߂�l��ݒ�
    SelectFolder_util = selectedFolderPath
    
    ' �I�u�W�F�N�g�̃N���[���A�b�v
    Set folderDialog = Nothing
End Function


'===============================================================================
'�����t�@�C����I���ł���_�C�A���O��\������
' targetRange: �I�������t�@�C����\������Z���͈̔�
' addCSVFilter: CSV�t�@�C���̃t�B���^��t���邩�̎w��
' title: �_�C�A���O�^�C�g��
'===============================================================================
Function SelectMultipleFiles_util(targetRange As Range, Optional addCSVFilter As Boolean = False, Optional title As String = "�t�@�C����I�����Ă�������")
    Dim fd As FileDialog
    Dim selectedFilePath As String
    Dim i As Integer

    ' �t�@�C���_�C�A���O�̏�����
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    
    ' �_�C�A���O�̐ݒ�
    With fd
        .title = title
        .AllowMultiSelect = True       ' �����t�@�C���̑I��������
        .Filters.Clear                 ' �����̃t�B���^�[���N���A
        If addCSVFilter Then
            .Filters.Add "CSV�t�@�C��", "*.csv"
        End If
        .Filters.Add "���ׂẴt�@�C��", "*.*"
        ' �_�C�A���O��\�����A�I�����ꂽ�t�@�C�����擾
        If .Show = -1 Then
            ' �I�����ꂽ�t�@�C���p�X���w�肵���Z���͈͂ɕ\��
            If targetRange.count < .SelectedItems.count Then
                MsgBox "�I�������Z�������t�@�C�����������ł� " & targetRange.address
                Set fd = Nothing
                Exit Function
            End If
            targetRange.ClearContents  ' �͈͂��N���A
            For i = 1 To .SelectedItems.count
                targetRange.Cells(i, 1).value = .SelectedItems(i)
            Next i
        End If
    End With
    ' �I�u�W�F�N�g�̃N���[���A�b�v
    Set fd = Nothing
End Function


'===============================================================================
' CSV�t�@�C����ǂݍ����String�z����i�[����Collection�I�u�W�F�N�g��ԋp���܂�
' filePath: �b�r�u�t�@�C���̃p�X
' Return: Collection�I�u�W�F�N�g �t�@�C���������A�ǂ߂Ȃ�����Nothing��ԋp���܂�
'===============================================================================
Function LoadCSV_util(filePath As String) As Collection
    Dim csvFile As Object
    Dim line As String
    Dim lineArray As Variant
    Dim rowCollection As Collection
    Dim fso As Object
    
    ' Collection�I�u�W�F�N�g�̏�����
    Set rowCollection = New Collection
    
    ' �t�@�C���V�X�e���I�u�W�F�N�g�̍쐬
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' �t�@�C�������݂��邩�m�F
    If Not fso.FileExists(filePath) Then
        MsgBox "�w�肳�ꂽ�t�@�C����������܂���: " & filePath, vbExclamation
        Set LoadCSV_util = Nothing
        Exit Function
    End If
    
    ' �t�@�C�����J��
    Set csvFile = fso.OpenTextFile(filePath, 1)
    
    ' �e�s��ǂݍ��݁A�z��ɕϊ�����Collection�ɒǉ�
    csvFile.ReadLine    '1�s�ڂ̓w�b�_�[�Ƃ��ăX�L�b�v����
    Do Until csvFile.AtEndOfStream
        line = csvFile.ReadLine
        ' �J���}��؂�ŕ������z��ɕϊ�
        lineArray = SplitCSV_util(line)
        ' Collection�ɔz���ǉ�
        rowCollection.Add lineArray
    Loop
    
    ' �t�@�C�������
    csvFile.Close
    
    ' Collection��Ԃ�
    Set LoadCSV_util = rowCollection
End Function

'===============================================================================
' �V�[�g����w�肳�ꂽ�ӂ��̗���L�[�ƒl�Ƃ���Dictionary�^�ŕԋp����
' sheetName: �Ǎ���̃V�[�g��
' startRow: �ǂݍ��݂��J�n����s�ԍ�
' keyColumn: �L�[�ƂȂ�Z���̗�ԍ�
' valueColumn: �l�ƂȂ�Z���̗�ԍ�
' Return: Dictionary�^�ŕԋp����A�V�[�g�������Ƃ���Notihng��ԋp����
'===============================================================================
Function GetDictiFromSheet_util(sheetName As String, startRow As Long, keyColumn As Long, valueColumn As Long) As Object
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim dataArr As Variant
    Dim rowDict As Object
    Dim i As Long
    Dim key As Variant
    Dim value As Variant
    
    ' ---- ������ ----
    Set rowDict = CreateObject("Scripting.Dictionary")
    
    ' ---- �V�[�g�̑��݊m�F ----
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(sheetName)
    On Error GoTo 0
    If ws Is Nothing Then
        Set GetDictiFromSheet_util = Nothing ' �V�[�g��������Ȃ��ꍇ��Nothing��Ԃ�
        Exit Function
    End If
    
    ' ---- �ŏI�s���擾 ----
    lastRow = ws.Cells(ws.Rows.count, keyColumn).End(xlUp).row
    If lastRow < startRow Then
        Set GetDictionaryFromSheet = rowDict ' �f�[�^�����݂��Ȃ��ꍇ�͋��Dictionary��Ԃ�
        Exit Function
    End If
    
    ' ---- �f�[�^�͈͂�z��ɓǂݍ��� ----
    dataArr = ws.Range(ws.Cells(startRow, keyColumn), ws.Cells(lastRow, valueColumn)).value
    
    ' ---- Dictionary�Ƀf�[�^���i�[ ----
    For i = 1 To UBound(dataArr, 1)
        key = dataArr(i, 1) ' �z����ł̃L�[�̗�
        value = dataArr(i, 2) ' �z����ł̒l�̗�
        
        ' �L�[���d�����Ă��Ȃ����m�F
        If Not rowDict.Exists(key) Then
            rowDict.Add CStr(key), value
        Else
            ' �L�[�̏d��������ꍇ�A�K�v�ɉ����ď�����ύX�\
            ' ���݂͖������Ď��ɐi��
        End If
    Next i
    
    ' ---- ���ʂ�Ԃ� ----
    Set GetDictiFromSheet_util = rowDict
End Function


'===============================================================================
' �_�u���R�[�e�[�V�������܂�CSV�������String�z��ɕϊ�����
' inputText: �J���}��؂�̕�����@�_�u���R�[�e�[�V�������܂�
' Return: AA,"BB",CC,"D,D",EE => AA | BB | CC | D,D | EE  �Ƃ����z��ŕԋp
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
                ' �_�u���N�H�[�e�[�V�������g�O��
                inQuotes = Not inQuotes
            Case ","
                If inQuotes Then
                    ' �_�u���N�H�[�e�[�V�������̃J���}�͗v�f�Ƃ��Ĉ���
                    currentElement = currentElement & currentChar
                Else
                    ' �_�u���N�H�[�e�[�V�����O�̃J���}�͗v�f�̋�؂�Ƃ��Ĉ���
                    elements.Add currentElement
                    currentElement = ""
                End If
            Case Else
                ' �ʏ�̕�����ǉ�
                currentElement = currentElement & currentChar
        End Select
    Next i
    
    ' �Ō�̗v�f��ǉ�
    elements.Add currentElement
    
    ' Collection��z��ɕϊ����ĕԋp
    Dim result() As String
    ReDim result(1 To elements.count)
    For i = 1 To elements.count
        result(i) = elements(i)
    Next i

    SplitCSV_util = result
End Function


'===============================================================================
' �w�肵���G�N�Z���t�@�C����Collection�I�u�W�F�N�g�Ƃ��ĕԋp����
' filePath: �ǂݍ��ރG�N�Z���t�@�C��
' sheetIndex: �ǂݍ��ރV�[�g�̃C���f�b�N�X
' Return: �ǂݍ��񂾃R���N�V�����I�u�W�F�N�g�A�ǂݍ��߂Ȃ����Nothing��ԋp����
'===============================================================================
Function LoadExcel_util(filePath As String, sheetIndex As Integer) As Collection
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim rowCollection As Collection
    Dim rowArray As Variant
    Dim lastRow As Long, lastCol As Long
    Dim i As Long, j As Long
    
    ' Collection�I�u�W�F�N�g��������
    Set rowCollection = New Collection
    
    ' �t�@�C���̑��݊m�F
    If Dir(filePath) = "" Then
        MsgBox "�w�肳�ꂽ�t�@�C����������܂���: " & filePath, vbExclamation
        Set LoadExcel_util = Nothing
        Exit Function
    End If
    
    ' �t�@�C�����J��
    Application.ScreenUpdating = False
    Set wb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' �V�[�g�̑��݊m�F
    If sheetIndex < 1 Or sheetIndex > wb.Sheets.count Then
        MsgBox "�w�肳�ꂽ�V�[�g�C���f�b�N�X�������ł�: " & sheetIndex, vbExclamation
        wb.Close False
        Set LoadExcel_util = Nothing
        Exit Function
    End If
    
    ' �w�肳�ꂽ�V�[�g���擾
    Set ws = wb.Sheets(sheetIndex)
    
    ' �f�[�^�͈͂̍ŏI�s�ƍŏI����擾
    lastRow = ws.Cells(ws.Rows.count, 1).End(xlUp).row
    lastCol = ws.Cells(1, ws.Columns.count).End(xlToLeft).Column
    
    ' �e�s��String�z��Ƃ���Collection�ɒǉ�
    For i = 1 To lastRow
        ReDim rowArray(1 To lastCol)
        
        For j = 1 To lastCol
            rowArray(j) = CStr(ws.Cells(i, j).value) ' �e�Z���̒l�𕶎���Ƃ��Ď擾
        Next j
        
        rowCollection.Add rowArray
    Next i
    
    ' �t�@�C������Č��ʂ�Ԃ�
    wb.Close False
    Application.ScreenUpdating = True
    Set LoadExcel_util = rowCollection
End Function


'===============================================================================
' ���t�炵��������𐼗�ɕϊ�����
' dateString: �ϊ����镶���� ��: "�ߘaXX�NXX��XX��", "RXX.XX.XX", "XXXX�NXX��XX��"
' Return: yyyy/mm/dd�̌`���ɂ��ĕԋp���� �ϊ��ł��Ȃ���΋󕶎���""��ԋp����
'===============================================================================
Function ConvertDate_util(dateString As String) As String
    Dim result As Date
    Dim temp As String
    
    On Error Resume Next
        result = CDate(dateString)
    On Error GoTo 0
    
    If result = 0 Then
        'R6.10.10�Ȃǂ̌`�������邩������Ȃ��̂ŁA�ϊ����čĎ��s
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
' ������̔z����`�F�b�N���ċ󂾂�����G���[���b�Z�[�W��\������
' subject: �`�F�b�N���镶����̔z��
' msg: �G���[���b�Z�[�W�ɕ\������擪�̕�����@��F"XXXXXXX����͂��Ă�������"
' Return: True=���������Ă��Ȃ��G���[���b�Z�[�W���\�����ꂽ False=�z��ɉ����̕����񂪂���
'===============================================================================
Function IsEmptyArray_util(subject As Variant, msg As String) As Boolean
    If IsNull(subject) Then
        MsgBox msg & " ����͂��Ă�������"
        IsEmptyArray_util = True
        Exit Function
    End If
    If IsArray(subject) Then
        ' �z��̗v�f�����m�F
        If (UBound(subject) - LBound(subject) + 1) = 0 Then
            MsgBox msg & " ����͂��Ă�������"
            IsEmptyArray_util = True
            Exit Function
        End If
    Else
        MsgBox msg & " ����͂��Ă�������"
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
    MsgBox msg & " ����͂��Ă�������"
End Function


'===============================================================================
' �w�肵���͈͂̃Z������l���擾���Ĕz��ɂ��ĕԋp����
' rng: �z��ɂ������Z���͈̔�
' includeBlanks: �󔒂̃Z�����z��Ɋ܂߂邩�̃`�F�b�N True=�܂߂�@False=�܂߂Ȃ�
' Return: �����z���ԋp�A�l���S���Ȃ�����Null��ԋp����
'===============================================================================
Function GetValuesAsArray_util(rng As Range, includeBlanks As Boolean) As Variant
    Dim cell As Range
    Dim result As Collection
    Set result = New Collection
    
    ' �Z���̒l���R���N�V�����ɒǉ�
    For Each cell In rng
        If includeBlanks Or cell.value <> "" Then
            result.Add CStr(cell.value)
        End If
    Next cell
    ' �l���Ȃ��ꍇ��Null��Ԃ�
    If result.count = 0 Then
        GetValuesAsArray_util = Null
    Else
        ' �R���N�V������z��ɕϊ����ĕԂ�
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
' �w�肵���t�H���_�ƃT�u�t�H���_����t�@�C�����������ăt�@�C��������΃p�X�̔z���ԋp����
' folderPath:������̃t�H���_�p�X
' fileExtension: ��������g���q�@��F"csv", "txt"
' returnFullPath: ��΃p�X��ԋp���邩�̃t���O�@True:��΃p�X�@False:�t�@�C��������
' Return: Collection��ԋp����
'===============================================================================
Function SearchFiles_util(folderPath As String, fileExtension As String, returnFullPath As Boolean) As Collection
    Dim fso As Object
    Dim folder As Object
    Dim subFolder As Object
    Dim file As Object
    Dim result As New Collection

    ' FileSystemObject���쐬
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' �t�H���_�̑��݊m�F
    If Not fso.FolderExists(folderPath) Then
        MsgBox "�w�肳�ꂽ�t�H���_��������܂���: " & folderPath, vbExclamation
        Set SearchFiles_util = Nothing
        Exit Function
    End If
    
    ' �t�H���_�I�u�W�F�N�g���擾
    Set folder = fso.GetFolder(folderPath)
    
    ' �w��t�H���_���̃t�@�C��������
    For Each file In folder.Files
        If LCase(fso.GetExtensionName(file)) = LCase(fileExtension) Then
            If returnFullPath Then
                result.Add file.path   ' ��΃p�X��ǉ�
            Else
                result.Add file.Name   ' �t�@�C�����݂̂�ǉ�
            End If
        End If
    Next file
    
    ' �T�u�t�H���_���̃t�@�C�����ċA�I�Ɍ���
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

    ' ���ʂ�Ԃ�
    Set SearchFiles_util = result
End Function

'===============================================================================
' ��������w��̃o�C�g���Ő؂�l�߂ĕԋp����
' inputStr:�J�b�g���镶����
' byteLength: �؂�l�߂�o�C�g��
' Return: �������ԋp�@�w��o�C�g���̕������S�p��1�o�C�g�ڂ̎��͂��̑O�̕����܂ł�ԋp����
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
' �V�[�g�̃f�[�^�N���A����
' sheet: �N���A����V�[�g
' startRow: �N���A����J�n�s
'===============================================================================
Sub ClearSheet_Util(sheet As Worksheet, startRow As Long)
    Dim lastRow As Long

    ' �ŏI�s���擾
    lastRow = sheet.Cells(sheet.Rows.count, 1).End(xlUp).row

    ' �w�肵���s�ȍ~���N���A
    If startRow <= lastRow Then
        sheet.Rows(startRow & ":" & lastRow).ClearContents
    End If
End Sub

'===============================================================================
' �Z����s���{�������A�Ԓn�A�����ɕ�������
' strAddress: ��������Z��
' toZenkaku: True=�S�p�ɕϊ����ďo�́@False=���p�ŏo��
' return: �z��ŕԋp����@�s���{������,�Ԓn,����
'===============================================================================
Function SplitAddress_util(strAddress As String, toZenkaku As Boolean) As Variant
    Dim townName As String
    Dim houseNumber As String
    Dim additionalInfo As String
    Dim match As Object
    Dim strCovert As String

    ' ���K�\���I�u�W�F�N�g���쐬
    Dim regex As Object
    Set regex = CreateObject("VBScript.RegExp")

    ' ���K�\���p�^�[���i�����ƔԒn�̖��m�ȕ����j
    regex.pattern = "(.+[�s�撬��]*)\s*([0-9��-�]+����[0-9��-�-]*)\s*(.*)"
    If InStr(strAddress, "����") = 0 Then
        regex.pattern = "(.+[�s�撬��].*?[����])\s*([0-9��-�-]+)\s*(.*)"
    End If
    
    
    regex.Global = False
    regex.IgnoreCase = True

    strCovert = ConvertNumberWidth(strAddress, True)

    ' ���K�\���ŏZ���𕪊�
    If regex.test(strCovert) Then
        Set match = regex.Execute(strCovert)(0)

        ' �O���[�v1: ����
        townName = ConvertNumberWidth(Trim(match.SubMatches(0)), False)

        ' �O���[�v2: �Ԓn
        houseNumber = ConvertNumberWidth(Trim(match.SubMatches(1)), False)

        ' �O���[�v3: ����
        additionalInfo = ConvertNumberWidth(Trim(match.SubMatches(2)), False)
    Else
        townName = strAddress
        houseNumber = ""
        additionalInfo = ""
    End If

    ' ���ʂ�\��
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

    ' �S�p�E���p�����̔z����`
    fullWidthNumbers = Array("�O", "�P", "�Q", "�R", "�S", "�T", "�U", "�V", "�W", "�X", "�|", "�[", "�\", "�]")
    halfWidthNumbers = Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "-", "-", "-")
    
    result = ""

    ' �������1����������
    For i = 1 To Len(inputStr)
        c = Mid(inputStr, i, 1)
        found = False
        
        If toHalfWidth Then
            ' �S�p���甼�p�֕ϊ�
            For j = LBound(fullWidthNumbers) To UBound(fullWidthNumbers)
                If c = fullWidthNumbers(j) Then
                    c = halfWidthNumbers(j)
                    found = True
                    Exit For
                End If
            Next j
        Else
            ' ���p����S�p�֕ϊ�
            For j = LBound(halfWidthNumbers) To UBound(halfWidthNumbers)
                If c = halfWidthNumbers(j) Then
                    c = fullWidthNumbers(j)
                    found = True
                    Exit For
                End If
            Next j
        End If

        ' �����ȊO�̕����͂��̂܂�
        result = result & c
    Next i

    ConvertNumberWidth = result
End Function



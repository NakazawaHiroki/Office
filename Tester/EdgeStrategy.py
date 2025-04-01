from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from bs4 import BeautifulSoup
import os

import CONST
from Junk import *

#文字列から指定した文字を先頭から探して削除する s="000001234" char_to_remove="0" return "1234"
def remove_leading_chars(s: str, char_to_remove: str) -> str:
    i = 0
    while i < len(s) and s[i] == char_to_remove:
        i += 1
    return s[i:]


###################################################################
#   EdgeStrategy
###################################################################
class EdgeStrategy:
    def __init__(self):
        self.openURL = ''
        self.loginID = ''
        self.loginPass = ''
        self.openLedgerID = ''
        self.EdgeD = None

    #Edgeドライバーのパスを取得する
    def getWebDriverPath(self):
        driverpath = getConfVal('EdgeDriverPath')
        if driverpath == '' or driverpath == '.':
            #実行環境パスを取得する
            driverpath = os.path.join(os.getcwd(), "msedgedriver.exe")
        return driverpath

    #Webドライバーの初期化
    def initDriver(self):
        #サービスを取得する
        path = self.getWebDriverPath()
        #ファイルがあるかチェックする
        if not os.path.isfile(path):
            return CONST.RES_WEBDRV_NONE
        try:
            webdriver_service = Service(path)
        except Exception as e:
            print('ドライバーのロードに失敗した')
            print(f'例外が発生 {e}')
            return CONST.RES_WEBDRV_LOADERROR
        
        # WebDriverのインスタンスを作成
        try:
            opt = webdriver.EdgeOptions()
            opt.use_chromium = True
            opt.add_argument('--disable-extensions')  # 拡張機能を無効化
            opt.add_argument('--no-sandbox')  # サンドボックスを無効化
            opt.add_argument('--log-level=3')  # ログレベルをほとんど出さないようにする
            self.EdgeD = webdriver.Edge(service=webdriver_service, options=opt)
        except Exception as e:
            print('Edgeドライバーの作成に失敗した')
            print(f'例外が発生 {e}')
            return CONST.RES_WEBDRV_INCOMPATIBLE
        return CONST.RES_SUCCESS


    #指定されたURLのページを開く
    def accessURL(self, URL):
        try:
            # 指定されたURLを開く
            self.EdgeD.get(URL)
            self.EdgeD.set_page_load_timeout(60)
            self.openURL = URL
            return CONST.RES_SUCCESS
        except Exception as e:
            self.openURL = ''
            print(f'例外が発生 {e}')
            return CONST.RES_WRONG_URL

    def login(self, ID, Pass):
        try:
            if self.openURL == '':
                return CONST.RES_NO_OPENURL
            
            # id=loginIDのinputタグを取得して「densan」と入力
            login_id_field = self.EdgeD.find_element("id", "loginID")
            login_id_field.clear()  # 既存のテキストをクリア
            login_id_field.send_keys(ID)

            # id=passwordのinputタグを取得して「densan」と入力
            password_field = self.EdgeD.find_element("id", "password")
            password_field.clear()  # 既存のテキストをクリア
            password_field.send_keys(Pass)

            # id=button1のinputタグ（type=submit）を取得してクリック
            submitbuttonID = "button1"
            submit_button = WebDriverWait(self.EdgeD, 20).until(EC.element_to_be_clickable((By.ID, submitbuttonID)))
            self.EdgeD.execute_script("arguments[0].click();", submit_button)
            self.loginID = ID
            self.loginPass = Pass
            return CONST.RES_SUCCESS
        except Exception as e:
            self.loginID = ''
            self.loginPass = ''
            print(f'例外が発生 {e}')
            return CONST.RES_LOGIN_FAILURE

    #新規帳票を選択する
    def openNewLedger(self, ledgerID):
        try:
            #waitオブジェクトを作成してボタンでクリック可能まで待機する
            buttonWait = WebDriverWait(self.EdgeD, 10)

            # 新規を選択する
            menu_itemID = "menu3"
            menu_item = self.getElement(menu_itemID)
            buttonWait.until(EC.element_to_be_clickable((By.ID, menu_itemID)))
            menu_item.click()

            #リストの全てを選択する
            formListID = "formList"
            tempelem = self.getElement(formListID)
            select_element = Select(tempelem)
            select_element.select_by_value("all")

            #IDは先頭の0を削って指定する
            tempelem = self.getElement(remove_leading_chars(ledgerID, "0"))

            if tempelem is None:
                return CONST.RES_NO_LEDGER
            
            # 親の<tr>要素（行）を取得する
            row = tempelem.find_element(By.XPATH, "./ancestor::tr")
            # 行全体をクリックする
            self.EdgeD.execute_script("arguments[0].scrollIntoView(true);", row)
            self.EdgeD.execute_script("arguments[0].click();", row)

            #選択ボタンを取得する
            selectBtnID = "btn"
            tempelem = self.getElement(selectBtnID)
            buttonWait.until(EC.element_to_be_clickable((By.ID, selectBtnID)))
            self.EdgeD.execute_script("arguments[0].click();", tempelem)

            #帳票を開けるまで待機
            self.EdgeD.set_page_load_timeout(120)

            self.openLedgerID = ledgerID
        except Exception as e:
            self.openLedgerID = ''
            print(f'例外が発生 {e}')

    #未処理帳票を開く
    def openUnProcessLedger(self, ledgerID):
        result = CONST.RES_SUCCESS
        try:
            #waitオブジェクトを作成してボタンでクリック可能まで待機する
            buttonWait = WebDriverWait(self.EdgeD, 10)

            # 未処理帳票を選択する
            menu_itemID = "menu1"
            menu_item = self.getElement(menu_itemID)
            buttonWait.until(EC.element_to_be_clickable((By.ID, menu_itemID)))
            menu_item.click()

            #IDは先頭の0を削って指定する
            if ledgerID != 'top':
                tempelem = self.getElement(remove_leading_chars(ledgerID, "0"))
                if tempelem is None:
                    return CONST.RES_NO_LEDGER
                # 親の<tr>要素（行）を取得する
                row = tempelem.find_element(By.XPATH, "./ancestor::tr")
                self.EdgeD.execute_script("arguments[0].scrollIntoView(true);", row)
                self.EdgeD.execute_script("arguments[0].click();", row)
            else:
                row = WebDriverWait(self.EdgeD, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="list"]/tbody/tr[1]')))
                # 行全体をクリックする
                row.click()

            #選択ボタンを取得する
            selectBtnID = "btnSelectReports"
            tempelem = self.getElement(selectBtnID)
            buttonWait.until(EC.element_to_be_clickable((By.ID, selectBtnID)))
            self.EdgeD.execute_script("arguments[0].click();", tempelem)

            #帳票を開けるまで待機
            self.EdgeD.set_page_load_timeout(120)

            self.openLedgerID = ledgerID
        except Exception as e:
            self.openLedgerID = ''
            print(f'例外が発生 {e}')
            result = CONST.RES_NO_LEDGER

        return result


    #ブラウザの終了処理
    def terminateBrowser(self):
        self.openURL = ''
        self.loginID = ''
        self.loginPass = ''
        self.openLedgerID = ''
        if self.EdgeD is not None:
            #os.kill(self.EdgeD.service.process.pid, signal.SIGTERM)
            self.EdgeD.quit()
        self.EdgeD = None


    #指定のIDタグが表示されるまで待って要素を取得する
    def getElement(self, elementID):
        element = None
        try:
            wait = WebDriverWait(self.EdgeD, 5)  # 最大5秒待機
            wait.until(EC.presence_of_element_located((By.ID, elementID)))
            element = self.EdgeD.find_element(By.ID, elementID)
        except TimeoutException:
            return None
        return element

    def setValue(self, tagType, tagID, value):
        element = self.getElement(tagID)
        if element is None:
            return CONST.RES_TAGID_NONE
        
        actualType = element.get_attribute('type')
        if element.get_attribute('readonly'):
            actualType = 'readonly'
        elif actualType is None or actualType == '':
            actualType = element.tag_name

        #タイプの指定が違っていたら警告する
        if actualType.find(tagType) < 0:
            return CONST.RES_TAGTYPE_ERROR

        if element is not None and value != '':
            if tagType == "text":
                element.clear()  # 既存のテキストをクリア（必要に応じて）
                if value != 'clear':
                    element.send_keys(value)
            elif tagType == "select":
                try:
                    select = Select(element)
                    if value == 'clear':
                        value = ''
                    select.select_by_visible_text(value)
                except NoSuchElementException:
                    return CONST.RES_NO_SUCH_SELECT
            elif tagType == "checkbox":
                try:
                    element = WebDriverWait(self.EdgeD, 10).until(EC.element_to_be_clickable((By.ID, tagID)))
                except TimeoutException:
                    return CONST.RES_TAGTYPE_ERROR
                # 要素が画面に表示されるようにスクロール
                self.EdgeD.execute_script("arguments[0].scrollIntoView(true);", element)                    
                element.click()
            elif tagType == "button":
                try:
                    element = WebDriverWait(self.EdgeD, 10).until(EC.element_to_be_clickable((By.ID, tagID)))
                except TimeoutException:
                    return CONST.RES_TAGTYPE_ERROR
                # onclick属性を取得
                onclick_attr = element.get_attribute("onclick")
                if onclick_attr:
                    # onclick属性がある場合、そのJavaScriptコードを実行
                    self.EdgeD.execute_script(onclick_attr)
                else:
                    # 要素が画面に表示されるようにスクロール
                    self.EdgeD.execute_script("arguments[0].scrollIntoView(true);", element)                    
                    element.click()
                # ページ読み込みのタイムアウトを設定
                self.EdgeD.set_page_load_timeout(10)

        return CONST.RES_SUCCESS
    

    def compareValue(self, tagID, value):
        element = self.getElement(tagID)
        if element is None:
            return CONST.RES_TAGID_NONE

        #タイプの指定が違っていたら警告する
        actualType = element.get_attribute('type')
        if actualType.find("text") < 0:
            return CONST.RES_TAGTYPE_ERROR
        
        #valueが空白ならばチェックしないで成功
        if value == '':
            return CONST.RES_SUCCESS
        
        input_value = element.get_attribute("value")

        if input_value != '' and value == 'clear':
            return CONST.RES_MISMATCH
        elif input_value != value:
            return CONST.RES_MISMATCH

        return CONST.RES_SUCCESS
    

    #入力チェックボタンを押す
    def fireInputCheck(self):
        self.EdgeD.execute_script("inputCheck();")
        self.EdgeD.set_page_load_timeout(30)
        #<td class="err">が無くて例外が発生すれば成功とする
        try:
            element = self.EdgeD.find_element(By.XPATH, '//td[@class="err"]')
        except:
            return CONST.RES_SUCCESS
        return CONST.RES_ERROR

    #戻るボタンを押す
    def fireGoBack(self):
        try:
            element = self.EdgeD.find_element(By.XPATH, '//a[@onClick="goBack()"]')
        except:
            return CONST.RES_BUTTON_NONE
        self.EdgeD.execute_script("goBack();")
        self.EdgeD.set_page_load_timeout(30)

    #起票ボタンを押す
    def fireStartReport(self):
        try:
            element = self.EdgeD.find_element(By.XPATH, '//a[@onClick="startReportHandler()"]')
        except:
            return CONST.RES_BUTTON_NONE
        self.EdgeD.execute_script("startReportHandler();")
        ok_button = self.getElement('message_button_ok')
        ok_button.click()
        self.EdgeD.set_page_load_timeout(30)
    

    #承認ボタンを押す
    def fireAcceptReport(self):
        try:
            element = WebDriverWait(self.EdgeD, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@onClick="acceptReportHandler()"]')))            
        except Exception as e:
            print(f'例外発生 {e}')
            return CONST.RES_BUTTON_NONE
        self.EdgeD.execute_script("acceptReportHandler();")
        ok_button = self.getElement('message_button_ok')
        ok_button.click()
        self.EdgeD.set_page_load_timeout(30)
        #<td class="err">が無くて例外が発生レば成功とする
        try:
            element = self.EdgeD.find_element(By.XPATH, '//td[@class="err"]')
        except:
            return CONST.RES_SUCCESS
        return CONST.RES_ERROR

    #エラー情報を取得する
    def getErrorInfo(self):
        errorMessage = ''
        errorCode = ''
        try:
            elementCode = self.EdgeD.find_element(By.XPATH, '//span[@class="err"]')
            elementMes = self.EdgeD.find_element(By.XPATH, '//div[@class="err"]')
            errorCode = elementCode.text
            errorMessage = elementMes.text
        except:
            pass
        return errorCode, errorMessage

    #inputタグの指定したタイプを列挙する
    def enumInputTag(self, type):
        return self.EdgeD.find_elements(By.XPATH, f'//input[@type=\'{type}\']')

    #<textarea>タグを列挙する
    def enumTextAreaTag(self):
        return self.EdgeD.find_elements(By.TAG_NAME, "textarea")

    #<select>タグを列挙する
    def enumSelectTag(self):
        return self.EdgeD.find_elements(By.TAG_NAME, "select")
    
    #全てのタグを列挙する
    def enumTag(self):
        # WebDriverWait(self.EdgeD, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        html = self.EdgeD.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_tags = soup.find_all()
        return all_tags

    #ブラウザ情報の取得
    def getOpenURL(self):
        return self.openURL
    def getLogiID(self):
        return self.loginID
    def getLoginPass(self):
        return self.loginPass
    def getOpenLedger(self):
        return self.openLedgerID
    def IsBrowserOpen(self):
        if self.EdgeD is not None:
            if self.EdgeD.session_id is not None:
                try:
                    if len(self.EdgeD.window_handles) > 0:
                        return True
                except WebDriverException:
                    return False
        return False
    def getBrowserVer(self):
        result = get_edge_version()
        if result is None:
            result = ''
        return result
    def getDriverVer(self):
        result = ''
        path = self.getWebDriverPath()
        result = get_webdriver_version(path)
        if result is None:
            result = ''
        return result

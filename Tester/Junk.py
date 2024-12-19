import os
import subprocess

################################################################
# config.infから情報を取得する
################################################################
def getConfVal(getKey):
    result = ''
    file_path = os.path.join(os.getcwd(), "config.inf")
    try:
        with open(file_path, 'r') as config_file:
            for line in config_file:
                key, value = line.strip().split('=')
                if key == getKey:
                    result = value
                    break
    except FileNotFoundError:
        result = ''
    return result

################################################################
# レジストリからEdgeブラウザのバージョンを取得する
################################################################
def get_edge_version():
    try:
        # WindowsのレジストリからEdgeバージョンを取得するコマンドを実行
        result = subprocess.run(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Edge\\BLBeacon', '/v', 'version'],
            capture_output=True, text=True, check=True
        )
        # 結果からバージョン情報を抽出
        for line in result.stdout.splitlines():
            if 'version' in line:
                version = line.split()[-1]
                return version
    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")
        return None

################################################################
# WebDriverからバージョンを取得する
################################################################
def get_webdriver_version(driver_path):
    try:
        # WebDriverのバージョンを取得するためにsubprocessを使ってコマンド実行
        result = subprocess.run([driver_path, '--version'], capture_output=True, text=True)
        # 結果の出力からバージョン情報を抽出
        version_info = result.stdout.strip()
        version_info = get_string_between(version_info, 'WebDriver ', ' (')
        return version_info
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

################################################################
# 文字列から開始と終了の文字列に挟まれた文字を返却する
################################################################
def get_string_between(text, start_str, end_str):
    start_index = text.find(start_str)
    end_index = text.find(end_str, start_index + len(start_str))

    if start_index != -1 and end_index != -1:
        # 開始文字と終了文字の間の文字列を取得
        return text[start_index + len(start_str):end_index].strip()
    else:
        return ""
    
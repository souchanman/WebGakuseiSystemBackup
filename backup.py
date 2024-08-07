from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Chromeのオプションを設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモードで実行する場合
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriverのパスを設定
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# ログインページのURL
login_url = "https://risyu.saitama-u.ac.jp/portal/Login.aspx"
try:
    # ログインページにアクセス
    driver.get(login_url)

    # ログインフォームの要素を検索
    username_input = driver.find_element(By.ID, "txtID")
    password_input = driver.find_element(By.ID, "txtPassWord")
    login_button = driver.find_element(By.ID, "ctl17_btnLogin")

    # ユーザーIDとパスワードを入力
    username_input.send_keys("aa")
    password_input.send_keys("bb")

    # ログインボタンをクリック
    login_button.click()

    # ページが読み込まれるのを待つ
    driver.implicitly_wait(10)


except Exception as e:
            print(f"ログインにてエラーが発生しました: {e}")
            driver.quit()
            print("end")
            exit()
        
try:
        # ログイン後のページを取得し、新着メッセージボタンをクリック
    message_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_phContents_ucNewMessage_a"))
    )
    message_button.click()

except Exception as e:
            print(f"メッセージ画面への遷移にてエラーが発生しました: {e}")
            driver.quit()
            print("end")
            exit()


# メールリンクのXPathリストを作成
mail_xpaths = [
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[2]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[3]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[4]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[5]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[6]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[7]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[8]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[9]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[10]/td[5]/div/div[2]/a",
    "/html/body/form/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/contenttemplate/font/div/table/tbody/tr[11]/td[5]/div/div[2]/a"
]

page_number = 1  # 現在のページ番号
mail_counter = 1  # メールのカウント

while True:
    # 各メールリンクをクリックし、内容を取得して保存
    for mail_xpath in mail_xpaths:
        try:
            # 各メールリンクをクリック
            mail_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, mail_xpath))
            )
            mail_link.click()

            # メール詳細ページの内容を取得
            mail_content_html = driver.page_source

            # BeautifulSoupを使ってHTMLからテキストを抽出
            soup = BeautifulSoup(mail_content_html, 'html.parser')

            # 特定の要素を抽出
            content_element = soup.find('table', {'id': 'ctl00_phContents_ctlMesReceive_ctlMesReceiveDetail_fvDetail_tblMes'})
            if content_element:
                content_text = content_element.get_text(separator="\n").strip()

                # 内容をHTMLファイルに保存
                with open(f'mail_{mail_counter}.html', 'w', encoding='utf-8') as f:
                    f.write(mail_content_html)

                # 内容をテキストファイルに保存
                with open(f'mail_{mail_counter}.txt', 'w', encoding='utf-8') as f:
                    f.write(content_text)

                mail_counter += 1

        except Exception as e:
            print(f"メッセージの取得に際しエラーが発生しました: {e}")            
            driver.quit()
            print("end")
            exit()

    try:
        # 現在のページの数字を取得
        page_elements = driver.find_elements(By.CSS_SELECTOR, "td > a, td > span")
        page_numbers = [int(el.text) for el in page_elements if el.text.isdigit()]
        
        if page_number in page_numbers:
            next_page_number = page_number + 1
            if next_page_number in page_numbers:
                next_page_element = driver.find_element(By.XPATH, f"//td/a[text()='{next_page_number}']")
                next_page_element.click()
                page_number = next_page_number
            else:
                # 「...」をクリックして次のページへ
                ellipsis_elements = driver.find_elements(By.XPATH, "//td/a[text()='...']")
                if len(ellipsis_elements) == 1:
                    ellipsis_elements[0].click()
                elif len(ellipsis_elements) == 2:
                    ellipsis_elements[1].click()
                # ページ番号のインクリメント
                page_number += 1

        else:
            # 最後のページ
            break

    except Exception as e:
        print(f"ページ遷移中にエラーが発生しました: {e}")
        break

# ブラウザを閉じる
driver.quit()
print("end")

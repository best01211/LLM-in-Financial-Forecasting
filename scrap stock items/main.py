from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Selenium WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 숨김 모드
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

# URL 설정
url = "https://finance.naver.com/sise/lastsearch2.naver"
driver.get(url)

# JavaScript 로드 확인 및 데이터 대기
wait = WebDriverWait(driver, 30)
try:
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contentarea > div.box_type_l > table > tbody")))
    print("데이터가 로드되었습니다.")
except Exception as e:
    print("데이터 로드에 실패했습니다:", e)
    driver.quit()
    raise Exception("HTML 구조를 확인하세요.")

# 데이터 추출
companies = []
try:
    rows = driver.find_elements(By.CSS_SELECTOR, "#contentarea > div.box_type_l > table > tbody > tr")
    for idx, row in enumerate(rows):
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) < 8:  # 열이 8개 미만인 경우 건너뜀
            continue
        
        # 종목명 추출
        try:
            company_name = columns[1].find_element(By.TAG_NAME, "a").text.strip()
        except:
            company_name = "N/A"  # 종목명이 없을 경우 기본값 설정

        company_data = {
            "순위": columns[0].text.strip(),
            "종목명": company_name,
            "검색비율": columns[2].text.strip(),
            "현재가": columns[3].text.strip(),
            "전일비": columns[4].text.strip(),
            "등락률": columns[5].text.strip(),
            "시가총액": columns[7].text.strip()
        }
        companies.append(company_data)
except Exception as e:
    print("데이터 추출에 실패했습니다:", e)

# 브라우저 종료
driver.quit()

# 데이터 저장
if companies:
    df = pd.DataFrame(companies)
    df.to_csv("naver_finance_companies.csv", index=False, encoding="utf-8-sig")
    print("데이터가 'naver_finance_companies.csv' 파일에 저장되었습니다.")
else:
    print("데이터가 비어 있습니다.")

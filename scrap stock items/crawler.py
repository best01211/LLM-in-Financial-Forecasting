from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_all_company_data():
    # Selenium WebDriver 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    url = "https://finance.naver.com/sise/lastsearch2.naver"
    driver.get(url)

    company_list = []

    try:
        # 데이터 로드 대기
        wait = WebDriverWait(driver, 30)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contentarea > div.box_type_l > table > tbody")))

        # 모든 행 가져오기
        rows = driver.find_elements(By.CSS_SELECTOR, "#contentarea > div.box_type_l > table > tbody > tr")
        filtered_rows = [row for row in rows if len(row.find_elements(By.TAG_NAME, "td")) > 0]  # 빈 행 제거

        for row in filtered_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 8:
                company_data = {
                    "순위": columns[0].text.strip(),
                    "종목명": columns[1].find_element(By.TAG_NAME, "a").text.strip(),
                    "검색비율": columns[2].text.strip(),
                    "현재가": columns[3].text.strip(),
                    "전일비": columns[4].text.strip().replace("\n", " "),
                    "등락률": columns[5].text.strip(),
                    "거래량": columns[6].text.strip(),
                    "시가총액": columns[7].text.strip()
                }
                company_list.append(company_data)

    except Exception as e:
        print(f"크롤링 오류: {e}")
    finally:
        driver.quit()
    
    return company_list

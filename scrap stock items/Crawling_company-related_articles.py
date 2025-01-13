import requests
from bs4 import BeautifulSoup
import csv

def crawl_news_links(url, output_file):
    # HTTP 요청 보내기
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to fetch URL {url}")
        return

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, "html.parser")

    # 기사 링크 크롤링
    article_links = []
    sections = soup.select("#newsct > div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div")

    for section in sections:
        articles = section.select("ul > li")
        for article in articles:
            link_tag = article.select_one("div > div > div.sa_thumb._LAZY_LOADING_ERROR_HIDE > div > a")
            if link_tag and link_tag.get("href"):
                article_links.append(link_tag["href"])

    # CSV로 저장
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Article Link"])
        for link in article_links:
            writer.writerow([link])

    print(f"{len(article_links)} article links have been saved to {output_file}.")

# URL과 저장할 파일 경로 설정
news_url = "https://news.naver.com/breakingnews/section/101/259?date=20250113"
output_csv = "news_links.csv"

# 크롤링 실행
crawl_news_links(news_url, output_csv)

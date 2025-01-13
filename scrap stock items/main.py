import Crawling_listed_companies as crawler # crawler.py 모듈을 불러옴

def main():
    # 모든 회사 데이터를 가져오기
    print("전체 데이터를 크롤링 중입니다...")
    all_data = crawler.get_all_company_data()

    if not all_data:
        print("데이터를 가져오는 데 실패했습니다.")
        return

    # 사용자 입력 받기
    try:
        rank = int(input("1에서 30 사이의 순위를 입력하세요: "))
        if rank < 1 or rank > len(all_data):
            raise ValueError("1에서 30 사이의 정수를 입력해야 합니다.")
    except ValueError as e:
        print(f"입력 오류: {e}")
        return

    # 입력한 순위에 해당하는 데이터 출력
    company_data = all_data[rank - 1]
    print(f"순위 {rank}에 해당하는 회사 데이터:")
    for key, value in company_data.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()

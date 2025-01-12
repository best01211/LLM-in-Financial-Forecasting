import pandas as pd

# 올바른 CSV 파일 경로 설정
file_path = "C:/Users/c/Desktop/Git/LLM-in-Financial-Forecasting/naver_finance_companies.csv"

try:
    # CSV 파일 로드
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    
    # 데이터 출력
    print("CSV 파일 내용:")
    print(df)
except FileNotFoundError:
    print(f"파일 '{file_path}'을(를) 찾을 수 없습니다. 파일 경로를 확인하세요.")
except Exception as e:
    print(f"오류 발생: {e}")

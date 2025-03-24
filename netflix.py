from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ChromeDriver 경로 설정 (자신의 chromedriver 경로를 입력하세요)
driver = webdriver.Chrome('/path/to/chromedriver')  # '/path/to/chromedriver'를 실제 경로로 수정하세요.

# 넷플릭스 웹페이지 열기
driver.get('https://www.netflix.com/browse/genre/34399')  # Top 10 페이지 URL

# 페이지 로딩 대기 (5초)
time.sleep(5)

# 상위 10개의 영화 데이터를 담을 리스트
top_10_movies = []

# 1위부터 10위까지 반복하며 영화 제목 추출
for i in range(1, 11):
    try:
        # 영화 제목 추출 (XPath 사용)
        movie_title = driver.find_element(By.XPATH, f'//div[@class="row"][1]//div[@class="title-card-container"][{i}]//a//span').text
        
        # 데이터를 리스트에 저장
        top_10_movies.append({'순위': i, '영화 제목': movie_title})
    except Exception as e:
        print(f"순위 {i}에서 오류 발생: {e}")
        continue

# 결과 출력 (복사할 수 있게 포맷팅)
print("순위\t영화 제목")
for movie in top_10_movies:
    print(f"{movie['순위']}\t{movie['영화 제목']}")

# 브라우저 종료
driver.quit()

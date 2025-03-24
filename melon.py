from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Chrome WebDriver 설정 (자신의 chromedriver 경로를 입력하세요)
driver = webdriver.Chrome('/path/to/chromedriver')  # 여기 경로 수정 필요

# 2. 멜론 차트 페이지 열기
driver.get('https://www.melon.com/chart/index.htm')

# 3. 페이지 로딩을 기다림 (5초)
time.sleep(5)

# 4. 탑 100 데이터를 담을 리스트
music_data = []

# 5. 1위부터 100위까지 반복해서 데이터 추출
for i in range(1, 101):
    try:
        # 곡명, 아티스트명, 앨범명 추출
        song_name = driver.find_element(By.XPATH, f'//table[@class="d_song_list"]/tbody/tr[{i}]/td[4]/div[1]/div[1]/a').text
        artist_name = driver.find_element(By.XPATH, f'//table[@class="d_song_list"]/tbody/tr[{i}]/td[4]/div[1]/div[2]/a').text
        album_name = driver.find_element(By.XPATH, f'//table[@class="d_song_list"]/tbody/tr[{i}]/td[5]/div/a').text

        # 데이터 리스트에 추가
        music_data.append({'순위': i, '곡명': song_name, '아티스트': artist_name, '앨범명': album_name})
    except Exception as e:
        print(f"순위 {i}에서 오류 발생: {e}")
        continue

# 6. 결과 출력 (복사하기 쉬운 형식)
print("순위\t곡명\t아티스트\t앨범명")
for song in music_data:
    print(f"{song['순위']}\t{song['곡명']}\t{song['아티스트']}\t{song['앨범명']}")

# 7. 브라우저 종료
driver.quit()

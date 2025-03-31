import requests
from bs4 import BeautifulSoup

# 멜론 차트 페이지 URL
url = 'https://www.melon.com/chart/index.htm'

# HTTP 요청 보내기
response = requests.get(url)

# 응답 받은 HTML 코드 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 차트에서 노래 제목과 아티스트 정보 추출
songs = soup.find_all('div', {'class': 'ellipsis rank01'})
artists = soup.find_all('div', {'class': 'ellipsis rank02'})

# 순위와 노래 제목, 아티스트 출력
for i in range(len(songs)):
    song_title = songs[i].get_text(strip=True)
    artist_name = artists[i].get_text(strip=True)
    print(f"순위 {i+1}: {song_title} - {artist_name}")

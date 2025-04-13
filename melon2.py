import requests
from bs4 import BeautifulSoup
import random
import time 

# --- 1. 웹 스크래핑 먼저 실행 ---
url = "https://www.melon.com/chart/index.htm"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

print("멜론 차트 정보를 가져오는 중...")
songs = [] # 노래 정보를 담을 리스트 (튜플 형태: (순위, 제목, 가수))

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # 요청 실패 시 예외 발생

    soup = BeautifulSoup(response.text, "html.parser")

    # 'lst50'과 'lst100' 클래스를 가진 tr 태그 찾기
    song_entries = soup.select('tr.lst50, tr.lst100')

    if not song_entries:
        print("오류: 차트 정보를 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
        # 데이터가 없으면 프로그램 종료 또는 다른 처리 가능
        exit() # 간단하게 종료 처리

    for entry in song_entries:
        try:
            rank = entry.select_one('span.rank').get_text()
            title = entry.select_one('div.ellipsis.rank01 a').get_text() # 제목 링크의 텍스트
            
            # 가수는 여러 명일 수 있으나, 예시처럼 첫 번째 가수만 가져오기
            artist = entry.select_one('div.ellipsis.rank02 a').get_text() 
            # # 만약 모든 가수를 가져오고 싶다면:
            # artists_tags = entry.select('div.ellipsis.rank02 a')
            # artist = ', '.join([a.get_text() for a in artists_tags])

            songs.append((rank, title, artist)) # 튜플로 저장
        except AttributeError:
            # 간혹 순위, 제목, 가수 정보가 없는 행이 있을 경우 건너뛰기
            continue
            
    print("차트 정보 로딩 완료!")
    time.sleep(1) # 잠시 대기

except requests.exceptions.RequestException as e:
    print(f"오류: 멜론 차트 페이지에 접속할 수 없습니다. ({e})")
    exit() # 접속 실패 시 종료
except Exception as e:
    print(f"오류: 데이터 처리 중 문제가 발생했습니다. ({e})")
    exit() # 기타 오류 발생 시 종료

# --- 2. 메뉴 표시 ---
print("==============")
print("1. 멜론 100 ")
print("2. 멜론 50 ")
print("3. 멜론 10 ")
print("4. AI 추천 노래 ")
print("5. 가수 이름 검색")
print("==============")

# --- 3. 사용자 입력 및 기능 처리 ---
n = input("메뉴선택(숫자입력):")
# print(f"당신이 입력한 값은? {n}") # 필요하다면 주석 해제

# 입력된 문자열 'n'을 기준으로 조건 처리 (정수 변환 X)
if n == "1":
    print("\n[멜론 TOP 100]")
    # songs 리스트에 100개 이상 데이터가 있는지 확인하는 것이 더 안전
    limit = min(100, len(songs)) # 실제 가져온 노래 수와 100 중 작은 값 사용
    for i in range(limit):
        rank, title, artist = songs[i] # 튜플 언패킹
        print(f"{rank}. {title} - {artist}")
    print("======================")

elif n == "2":
    print("\n[멜론 TOP 50]")
    limit = min(50, len(songs))
    for i in range(limit):
        rank, title, artist = songs[i]
        print(f"{rank}. {title} - {artist}")
    print("======================")

elif n == "3":
    print("\n[멜론 TOP 10]")
    limit = min(10, len(songs))
    for i in range(limit):
        rank, title, artist = songs[i]
        print(f"{rank}. {title} - {artist}")
    print("======================")

elif n == "4":
    print("\n[AI 추천 노래]")
    if songs: # songs 리스트가 비어있지 않은 경우에만 실행
        melon = random.choice(songs) # 리스트에서 무작위 튜플 선택
        random_rank, random_title, random_artist = melon # 튜플 언패킹
        print("오늘 멜론 Top 100 추천곡은")
        print(f"🎵 {random_rank}위 '{random_artist} - {random_title}' 입니다. 🎵")
    else:
        print("추천할 노래 데이터가 없습니다.")
    print("========================")

elif n == "5":
    print("\n[TOP100 가수 검색]")
    search_artist = input("가수 이름을 입력하세요: ")
    found_count = 0
    print(f"--- '{search_artist}' 검색 결과 ---")
    if songs: # 데이터가 있을 때만 검색
        # 가수 이름 비교 (예시 코드처럼 정확히 일치하는 경우)
        # 만약 '포함' 검색을 원하면: if search_artist.lower() in artist.lower():
        for rank, title, artist in songs: # 리스트를 직접 순회하며 언패킹
            if search_artist == artist: # 입력한 이름과 가수가 정확히 같을 때
                print(f"{rank}. {title} - {artist}")
                found_count += 1 # 찾은 횟수 증가
                
    if found_count == 0: # 한 곡도 찾지 못했다면
        print(f"입력하신 가수 '{search_artist}'의 노래를 TOP100 차트에서 찾을 수 없습니다.")
    print("-----------------------------")

else:
    print("잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")
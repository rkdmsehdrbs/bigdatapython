import requests
from bs4 import BeautifulSoup
import random

# 멜론 차트 페이지 URL
# 참고: 웹사이트 구조는 변경될 수 있으므로, 셀렉터가 작동하지 않으면 멜론 웹사이트 HTML 구조 확인 필요
url = 'https://www.melon.com/chart/index.htm'

# 헤더 설정 (멜론은 User-Agent 확인을 통해 봇 접근을 차단할 수 있으므로 설정)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

try:
    # 웹페이지 요청
    response = requests.get(url, headers=headers)
    response.raise_for_status() # 요청 실패 시 예외 발생

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 노래 제목과 아티스트를 담을 리스트
    songs = []

    # 멜론 차트의 노래 제목과 아티스트를 찾습니다.
    # select 사용 시 리스트로 반환되므로, select_one을 사용하거나 인덱스 [0] 접근 필요
    # lst50과 lst100 클래스를 가진 tr 태그를 모두 찾습니다.
    for entry in soup.select('tr.lst50, tr.lst100'):
        try:
            # 순위, 제목, 아티스트 추출 및 공백 제거
            rank_element = entry.select_one('span.rank')
            title_element = entry.select_one('div.ellipsis.rank01 a')
            # 아티스트는 여러 명일 수 있으므로 'a' 태그를 모두 찾아 텍스트를 합칩니다.
            artist_elements = entry.select('div.ellipsis.rank02 a')

            # None 체크: 요소가 없는 경우 건너<0xEB><0x8A><0xB0>
            if rank_element and title_element and artist_elements:
                rank = rank_element.get_text().strip()
                title = title_element.get_text().strip()
                # 여러 아티스트의 이름을 쉼표로 구분하여 합침
                artist = ', '.join([a.get_text().strip() for a in artist_elements])
                songs.append((rank, title, artist))
            else:
                # print(f"경고: 일부 정보가 누락된 항목 발견. 건너<0xEB><0x8A><0xB0>니다.")
                pass # 정보가 부족한 항목은 무시

        except AttributeError as e:
            print(f"데이터 추출 중 오류 발생: {e} - 해당 항목 건너<0xEB><0x8A><0xB0>니다.")
            continue # 오류 발생 시 다음 항목으로 넘어감

    # 성공적으로 곡 목록을 가져왔는지 확인
    if not songs:
        print("멜론 차트 정보를 가져오지 못했습니다. 웹사이트 구조가 변경되었거나 접속에 문제가 있을 수 있습니다.")
    else:
        # --- 메뉴 출력 및 선택 ---
        print("===================")
        print("1. 멜론 TOP 100")
        print("2. 멜론 TOP 50")
        print("3. 멜론 TOP 10")
        print("4. AI 추천 노래")
        print("5. 가수 이름 검색")
        print("===================")

        n = input("메뉴선택(숫자입력): ")
        print(f"당신이 입력한 값은? {n}")

        # --- 메뉴 처리 ---
        if n == "1":
            print("\n=== 멜론 TOP 100 ===")
            # 수집한 데이터가 100개 미만일 수 있으므로 실제 songs 리스트 길이만큼만 출력
            count_to_print = min(100, len(songs))
            if count_to_print == 0:
                print("표시할 곡 정보가 없습니다.")
            else:
                for i in range(count_to_print):
                    print(f"{songs[i][0]}. {songs[i][1]} - {songs[i][2]}")

        elif n == "2":
            print("\n=== 멜론 TOP 50 ===")
            count_to_print = min(50, len(songs)) # 실제 가져온 곡 수가 50 미만일 경우 대비
            if count_to_print == 0:
                print("표시할 곡 정보가 없습니다.")
            else:
                for i in range(count_to_print):
                    print(f"{songs[i][0]}. {songs[i][1]} - {songs[i][2]}")

        elif n == "3":
            print("\n=== 멜론 TOP 10 ===")
            count_to_print = min(10, len(songs)) # 실제 가져온 곡 수가 10 미만일 경우 대비
            if count_to_print == 0:
                print("표시할 곡 정보가 없습니다.")
            else:
                for i in range(count_to_print):
                    print(f"{songs[i][0]}. {songs[i][1]} - {songs[i][2]}")

        elif n == "4":
            print("\n=== AI 추천곡 ===")
            if not songs:
                 print("추천할 곡이 없습니다. 차트 정보를 먼저 가져와야 합니다.")
            else:
                # 멜론 차트 100 중에서 노래 한곡 랜덤 추천
                ai_song = random.choice(songs)
                print(f"AI 추천곡은 [{ai_song[0]}위] {ai_song[1]} - {ai_song[2]} 입니다.")

        elif n == "5":
            print("\n=== 가수 이름 검색 ===")
            if not songs:
                print("검색할 곡 정보가 없습니다. 차트 정보를 먼저 가져와야 합니다.")
            else:
                search_artist = input("검색할 가수 이름을 입력하세요: ").strip()
                found_songs = []
                # 대소문자 구분 없이 검색하기 위해 입력값과 비교 대상 모두 소문자로 변경
                search_artist_lower = search_artist.lower()
                for song in songs:
                    # 아티스트 이름에 검색어가 포함되어 있는지 확인 (부분 일치)
                    if search_artist_lower in song[2].lower():
                        found_songs.append(song)

                if found_songs:
                    print(f"\n--- '{search_artist}' 검색 결과 (멜론 TOP 100 내) ---")
                    for song in found_songs:
                        print(f"{song[0]}. {song[1]} - {song[2]}")
                else:
                    print(f"'{search_artist}'에 대한 곡을 멜론 TOP 100에서 찾을 수 없습니다.")

        else:
            print("잘못된 입력입니다. 1부터 5까지의 숫자를 입력해주세요.")

except requests.exceptions.RequestException as e:
    print(f"웹 페이지에 접속할 수 없습니다: {e}")
except Exception as e:
    print(f"알 수 없는 오류가 발생했습니다: {e}")
# func.py
import requests
from bs4 import BeautifulSoup
import random
import time

# --- 헬퍼 함수: 데이터 가져오기 및 파싱 ---
def fetch_chart_data():
  """멜론 차트 페이지를 요청하고 파싱하여 노래 리스트를 반환 (오류 시 None 반환)"""
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
  url = 'https://www.melon.com/chart/index.htm'
  print("[데이터를 가져오는 중...] ", end="", flush=True) # 진행 상황 표시
  try:
    response = requests.get(url, headers=headers, timeout=10) # 타임아웃 추가
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    print("완료!") # 성공 메시지
    songs = soup.select('tr[data-song-no]')
    song_list = []
    for song in songs:
      try:
        rank = song.select_one('span.rank').text.strip()
        title_element = song.select_one('div.ellipsis.rank01 a')
        artist_element = song.select_one('div.ellipsis.rank02 a')

        if title_element and artist_element:
          title = title_element.text.strip()
          artist = artist_element.text.strip()
          song_list.append({'rank': rank, 'title': title, 'artist': artist})
      except AttributeError:
        # 순위 외 다른 정보 누락 시 건너<0xEB><0x9B><0x99>기 (로그는 선택)
        continue
    return song_list
  except requests.exceptions.RequestException as e:
    print(f"\n[오류: 웹 페이지 접근 실패 - {e}]")
    return None
  except Exception as e:
    print(f"\n[오류: 데이터 처리 중 문제 발생 - {e}]")
    return None

# --- 헬퍼 함수: 화면 표시 ---
def display_chart(title, songs_to_display):
  """주어진 노래 리스트를 제목과 함께 출력"""
  print(f"\n--- {title} ---")
  if not songs_to_display:
    print("[표시할 데이터가 없습니다.]")
    return
  for song in songs_to_display:
    print(f'{song["rank"]}위 | 제목: {song["title"]} | 아티스트: {song["artist"]}')
  print("-" * (len(title) + 6)) # 제목 길이에 맞춰 구분선 길이 조절

# --- 액션 함수: 메뉴 기능 구현 ---

def show_top_n(title, count):
  """Top N 차트를 가져와서 화면에 표시"""
  print(title)
  time.sleep(1)
  all_songs = fetch_chart_data() # 데이터 가져오기
  if all_songs is not None: # 가져오기 성공 시
    display_chart(title, all_songs[:count]) # 상위 count개만 잘라서 표시

def recommend_song(title):
  """AI 추천곡 (랜덤 선택)"""
  print(title)
  time.sleep(1)
  print("[좋아요! 제가 열심히 찾아서 사용자님께 노래를 한 곡 추천할게요.]")
  time.sleep(1)
  print(f"[두구두구둥...]")
  time.sleep(1)

  all_songs = fetch_chart_data() # 데이터 가져오기
  if all_songs: # 데이터가 있고 비어있지 않으면
    random_song = random.choice(all_songs)
    print(f"[이 노래가 좋을 거 같아요!]")
    time.sleep(1)
    print(f'\n[추천 곡: {random_song["title"]} | 아티스트: {random_song["artist"]}] (원래 순위: {random_song["rank"]}위)')
  elif all_songs == []: # 데이터는 가져왔으나 비어있는 경우 (파싱 실패 등)
    print("[추천할 노래를 찾지 못했습니다. 데이터 파싱에 문제가 있을 수 있습니다.]")
  # all_songs가 None인 경우는 fetch_chart_data에서 이미 오류 메시지 출력됨

def search_artist(title, artist_name):
  """가수 이름으로 검색하여 결과 표시"""
  print(title)
  time.sleep(1)
  search_name_processed = artist_name.strip().lower()
  if not search_name_processed:
      print("[검색할 가수 이름을 입력해주세요.]")
      return

  print(f"[<{artist_name}>의 노래를 검색 중이에요...]")
  time.sleep(1)

  all_songs = fetch_chart_data() # 데이터 가져오기
  if all_songs is not None:
    found_songs = []
    for song in all_songs:
      if search_name_processed in song['artist'].strip().lower():
        found_songs.append(song)

    if found_songs:
      display_chart(f"'{artist_name}' 검색 결과 (TOP 100)", found_songs)
    else:
      print(f"[TOP 100 차트 내 <{artist_name}>의 노래를 찾을 수 없습니다.]")

def save_top_100_to_file(title, filename="melon_top100.txt"):
  """Top 100 차트를 파일에 저장"""
  print(title)
  time.sleep(1)
  print(f"['{filename}' 파일에 멜론 TOP 100 차트를 저장합니다...]")

  all_songs = fetch_chart_data() # 데이터 가져오기
  if all_songs: # None 아니고 비어있지 않음
    try:
      with open(filename, 'w', encoding='utf-8') as f:
        f.write("=== 멜론 차트 TOP 100 ===\n")
        f.write(f"(총 {len(all_songs)}곡)\n")
        f.write("=" * 25 + "\n")
        for song in all_songs:
          f.write(f'{song["rank"]}위 | 제목: {song["title"]} | 아티스트: {song["artist"]}\n')
      print(f"['{filename}' 파일 저장 완료!]")
    except Exception as e:
      print(f"[오류: 파일 저장 실패 - {e}]")
  elif all_songs == []:
      print("[저장할 데이터가 없습니다. (파싱 실패 등)]")
  # None인 경우는 fetch_chart_data에서 이미 오류 메시지 출력됨
  
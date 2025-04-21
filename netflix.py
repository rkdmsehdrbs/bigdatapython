import requests
from bs4 import BeautifulSoup
# import pandas as pd # 결과를 더 보기 좋게 출력하고 싶다면 pandas를 사용할 수 있습니다.

# FlixPatrol의 Netflix Top 10 페이지 URL (전 세계 영화 순위)
# 특정 국가를 원하면 URL을 변경해야 할 수 있습니다. (예: 한국은 /kr/)
url = 'https://flixpatrol.com/top10/netflix/world/today/movies/'

# 웹사이트에 요청을 보낼 때 브라우저인 것처럼 속이기 위한 헤더 정보
# User-Agent는 실제 사용하는 브라우저 정보로 바꿔주는 것이 좋습니다.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

top_10_movies = []

try:
    # 1. 웹 페이지 HTML 가져오기
    response = requests.get(url, headers=headers)
    response.raise_for_status() # 요청 실패 시 오류 발생 (e.g., 404 Not Found)

    # 2. HTML 파싱하기
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. 순위 정보가 있는 테이블 찾기
    # FlixPatrol 페이지 구조에 따라 적절한 선택자를 찾아야 합니다.
    # 개발자 도구(F12)를 사용하여 테이블이나 리스트 요소의 태그, 클래스 등을 확인합니다.
    # 예시: 영화 순위 테이블을 찾습니다. (구조가 바뀔 수 있습니다!)
    # 'table-movie' 클래스를 가진 첫 번째 테이블을 찾는다고 가정해봅니다.
    # 또는 테이블 제목을 찾고 그 다음 테이블을 찾는 방식도 가능합니다.
    # 여기서는 간단하게 find_all('tr')로 테이블 행들을 찾고, 그 중 필요한 데이터를 추출합니다.

    # 테이블의 행(tr)들을 찾습니다. tbody 안의 tr을 찾는 것이 더 정확할 수 있습니다.
    table_rows = soup.select('table.table-striped tbody tr') # CSS 선택자 사용

    if not table_rows:
        print("순위 정보를 담고 있는 테이블 행(tr)을 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
    else:
        # 4. 각 행(row)에서 순위와 제목 추출하기
        rank = 1
        for row in table_rows:
            # 각 행(tr) 안의 열(td)들을 찾습니다.
            cols = row.find_all('td')

            # 충분한 열이 있는지, 필요한 정보가 있는지 확인합니다.
            # FlixPatrol 구조상 보통 두 번째 열(index 1)에 제목 링크가 있습니다.
            if len(cols) > 1:
                # 제목은 보통 a 태그 안에 있습니다.
                title_tag = cols[1].find('a')
                if title_tag:
                    title = title_tag.text.strip() # 공백 제거
                    top_10_movies.append({'순위': rank, '영화 제목': title})
                    rank += 1
                    if rank > 10: # 10위까지만 추출
                        break
                else:
                    # 제목 태그를 찾지 못한 경우 (구조 변경 가능성)
                    print(f"{rank}위 항목에서 제목(a 태그)을 찾을 수 없습니다.")
            else:
                # 예상과 다른 행 구조
                print(f"{rank}위 항목에서 데이터 열(td) 개수가 부족합니다.")

except requests.exceptions.RequestException as e:
    print(f"웹 페이지를 가져오는 중 오류 발생: {e}")
except Exception as e:
    print(f"데이터 처리 중 오류 발생: {e}")

# 5. 결과 출력
if top_10_movies:
    print("--- FlixPatrol 기준 Netflix 영화 Top 10 (전 세계) ---")
    print("순위\t영화 제목")
    for movie in top_10_movies:
        print(f"{movie['순위']}\t{movie['영화 제목']}")

    # Pandas DataFrame으로 출력 (선택 사항)
    # try:
    #     df = pd.DataFrame(top_10_movies)
    #     print("\n--- Pandas DataFrame 결과 ---")
    #     print(df.to_string(index=False))
    # except ImportError:
    #     print("\n(Pandas 라이브러리가 설치되지 않아 DataFrame 출력을 생략합니다.)")

else:
    print("영화 순위 정보를 가져오지 못했습니다.")
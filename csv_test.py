import csv

data_to_write = [
    ['순위', '제목', '가수'],
    [1, '1노래', '1가수'],
    [2, '2노래', '2가수'],
    [3, '3노래', '3가수']
]
file_path = 'music.csv'
try:
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_to_write)

        print(f"'{file_path}'파일이 성공적으로 생성되었습니다.")

except Exception as e:
    print(f"파일 쓰기 중 오류 발생: {e}")
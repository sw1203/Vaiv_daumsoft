import json
import heapq
import glob


def solution(filename: str, file_no: int, answer: dict):
    result_file_name = input("결과 파일 이름을 적어주세요: ")+".txt"
    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            review = json.loads(line)

            if review['book_id'] not in answer:
                answer[review['book_id']] = [0 for i in range(6)]
                answer[review['book_id']][review['rating']] += 1
            else:
                answer[review['book_id']][review['rating']] += 1

            if len(answer) == 100000:
                answer = sorted(answer.items(), key=lambda x: int(x[0]))
                with open(f"tmp/count_file_{file_no}.txt", 'w') as write_file:
                    for book_id, rating in answer:
                        write_file.write(f"{book_id} {rating[0]} {rating[1]} {rating[2]} {rating[3]} {rating[4]} {rating[5]}\n")
                answer = dict()
                print(file_no)
                file_no += 1

    if answer:
        answer = sorted(answer.items(), key=lambda x: int(x[0]))
        with open(f"tmp/count_file_{file_no}.txt", 'w') as write_file:
            for book_id, rating in answer:
                write_file.write(f"{book_id} {rating[0]} {rating[1]} {rating[2]} {rating[3]} {rating[4]} {rating[5]}\n")
        answer.clear()
        print(f"{file_no} end")

    merge_files(result_file_name)
    print("Finish Program")


def merge_files(filename: str):
    print("Start merge_files function")
    count_files = glob.glob("tmp/count_file_*.txt")
    files = [open(file, "r") for file in count_files]
    heap = []
    min_book = []

    for index in range(0, len(files)):
        line = files[index].readline()
        book_score = list(map(int, line.split()))
        book_score.append(index)
        heapq.heappush(heap, book_score)

    with open(filename, 'w') as writefile:
        while True:

            if not heap:
                break

            if not min_book:
                min_book = heapq.heappop(heap)
                line = files[min_book[-1]].readline()
                if line:
                    book_score = list(map(int, line.split()))
                    book_score.append(min_book[-1])
                    heapq.heappush(heap, book_score)

            if heap and heap[0][0] == min_book[0]:
                min_book = [min_book[0], min_book[1]+heap[0][1], min_book[2]+heap[0][2], min_book[3]+heap[0][3], min_book[4]+heap[0][4], min_book[5]+heap[0][5], min_book[6]+heap[0][6]]
                line = files[heap[0][-1]].readline()
                if line:
                    book_score = list(map(int, line.split()))
                    book_score.append(heap[0][-1])
                    heapq.heappush(heap, book_score)
                heapq.heappop(heap)

            else:
                writefile.write(f"{min_book[0]} {min_book[1]} {min_book[2]} {min_book[3]} {min_book[4]} {min_book[5]} {min_book[6]}\n")
                min_book.clear()

    for file in files:
        file.close()


file_num = 1
answer_dict = dict()
json_file = "goodreads_reviews_dedup.json"

solution(json_file, file_num, answer_dict)

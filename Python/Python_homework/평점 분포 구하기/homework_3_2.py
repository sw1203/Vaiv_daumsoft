import json
import os


def solution(filename: str, file_no: int, answer: dict):
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
                with open(f"count_file_{file_no}.txt", 'w') as write_file:
                    for book_id, rating in answer:
                        write_file.write(f"{book_id} {rating[0]} {rating[1]} {rating[2]} {rating[3]} {rating[4]} {rating[5]}\n")
                answer = dict()
                print(file_no)
                if file_no % 2 == 0:
                    file_no = merge_file(file_no-1, file_no)
                file_no += 1

    if answer:
        answer = sorted(answer.items(), key=lambda x: int(x[0]))
        with open(f"count_file_{file_no}.txt", 'w') as write_file:
            for book_id, rating in answer:
                write_file.write(f"{book_id} {rating[0]} {rating[1]} {rating[2]} {rating[3]} {rating[4]} {rating[5]}\n")
        answer.clear()
        file_no = merge_file(file_no - 1, file_no)
        print(f"{file_no} end")


def merge_file(first_file_no: int, second_file_no: int) -> int:
    with open(f"count_file_{first_file_no}.txt", "r") as first_file, open(f"count_file_{second_file_no}.txt", "r") as second_file, open(f"count_file_{second_file_no + 1}.txt", "a") as write_file:
        first_line = first_file.readline()
        second_line = second_file.readline()

        while True:
            if not first_line or not second_line:
                break

            first_book = list(map(int, first_line.split()))
            second_book = list(map(int, second_line.split()))

            if first_book[0] == second_book[0]:
                write_file.write(f"{first_book[0]} {first_book[1]+second_book[1]} {first_book[2]+second_book[2]} {first_book[3]+second_book[3]} {first_book[4]+second_book[4]} {first_book[5]+second_book[5]} {first_book[6]+second_book[6]}\n")
                first_line = first_file.readline()
                second_line = second_file.readline()

            elif first_book[0] < second_book[0]:
                write_file.write(first_line)
                first_line = first_file.readline()

            else:
                write_file.write(second_line)
                second_line = second_file.readline()

        if first_line:
            write_file.write(first_line)
            while True:
                first_line = first_file.readline()
                if not first_line:
                    break
                write_file.write(first_line)

        if second_line:
            write_file.write(second_line)
            while True:
                second_line = second_file.readline()
                if not second_line:
                    break
                write_file.write(second_line)

    remove_files(first_file_no, second_file_no)
    print(second_file_no+1)
    return second_file_no+1


def remove_files(first_file_no: int, second_file_no: int):
    if os.path.isfile(f"count_file_{first_file_no}.txt") and os.path.isfile(f"count_file_{second_file_no}.txt"):
        os.remove(f"count_file_{first_file_no}.txt")
        os.remove(f"count_file_{second_file_no}.txt")


file_num = 1
answer_dict = dict()
json_file = "goodreads_reviews_dedup.json"

solution(json_file, file_num, answer_dict)

import json


def solution(json_file):
    answer = {}
    with open(json_file, 'r') as file:
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

    answer = sorted(answer.items(), key=lambda x: int(x[0]))

    with open("answer_2.txt", 'w', encoding='UTF-8') as write_file:
        for book_id, rating in answer:
            write_file.write(f"{book_id} {rating[0]} {rating[1]} {rating[2]} {rating[3]} {rating[4]} {rating[5]}\n")

    print(f"{len(answer)} end")

solution("goodreads_reviews_dedup.json")
import json
import gzip
"""
goodreads_reviews_dedup.json.gz 파일은 https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/reviews에서 다운
"""


def read_lines():
    with gzip.open("goodreads_reviews_dedup.json.gz", 'r') as file:
        while True:
            line = file.readline()
            if not line:
                return 0
            else:
                yield line


text = read_lines()
answer = {}
while True:
    try:
        review = json.loads(next(text))
        if review['book_id'] not in answer:
            answer[review['book_id']] = [0 for i in range(6)]
            answer[review['book_id']][review['rating']] += 1
        else:
            answer[review['book_id']][review['rating']] += 1
    except StopIteration:
        break

answer = sorted(answer.items(), key=lambda x: int(x[0]))

with open("answer.txt", 'w', encoding='UTF-8') as write_file:
    for book_id, rating in answer:
        write_file.write(f"{book_id} {rating[0]} {rating[1]} {rating[2]} {rating[3]} {rating[4]} {rating[5]}\n")

print(f"{len(answer)} end")

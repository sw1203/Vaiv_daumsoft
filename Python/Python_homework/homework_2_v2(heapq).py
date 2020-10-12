import re
import heapq


def extract_bigrams(text, top_n):
    text = re.sub('[^a-zA-Z ]', ' ', text).lower()  # re.sub('패턴', 바꿀문자열, 기존문자열, 바꿀횟수) -> 정규식을 이용하여 특정 문자열을 다른 문자열로 바꾸는 방법
    answer = {}

    for begin in range(len(text) - 1):
        word = text[begin:begin + 2]
        if " " not in word:
            if word in answer:
                answer[word] += 1
            else:
                answer[word] = 1
    heap = list(answer.items())
    heapq.heapify(heap)
    print(heap)
    rank = heapq.nsmallest(top_n, answer.items(), key=lambda x: (-x[1], x[0]))  # str에 대해서는 -가 잘못된 수식이라고 에러발생

    for bigram, count in rank:
        print(f"{bigram} {count}")

text = """
Hello!
This is the first question.
Read a text file, extract alphabet bi-grams and count them.
Finally select most frequent three bi-grams, and print them with count.
"""

extract_bigrams(text, 3)

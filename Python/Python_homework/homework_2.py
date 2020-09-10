import re
from collections import Counter


def extract_bigrams(text, top_n):
    text = re.sub('[^a-zA-Z ]', ' ', text).lower()  # re.sub('패턴', 바꿀문자열, 기존문자열, 바꿀횟수) -> 정규식을 이용하여 특정 문자열을 다른 문자열로 바꾸는 방법
    answer = []

    for begin in range(len(text) - 1):
        word = text[begin:begin + 2]
        if " " not in word:
            answer.append(word)

    answer = Counter(answer)
    answer = sorted(answer.items(), key=lambda x: (-x[1], x[0]))

    for index in range(top_n):
        print(f"{answer[index][0]} {answer[index][1]}")


text = """
Hello!
This is the first question.
Read a text file, extract alphabet bi-grams and count them.
Finally select most frequent three bi-grams, and print them with count.
"""

extract_bigrams(text, 4)

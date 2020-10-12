import re
import heapq
from collections import defaultdict


def extract_bigrams(text, top_n):
    text = re.sub('[^a-zA-Z ]', ' ', text).lower()  # re.sub('패턴', 바꿀문자열, 기존문자열, 바꿀횟수) -> 정규식을 이용하여 특정 문자열을 다른 문자열로 바꾸는 방법
    answer = defaultdict(int)  # key에 대한 value가 없으면 value를 0으로 초기화

    for begin in range(len(text) - 1):
        word = text[begin:begin + 2]
        if " " not in word:
            answer[word] += 1

    rank = heapq.nsmallest(top_n, answer.items(), key=lambda x: (-x[1], x[0]))
    """
    heapq 공식 문서에 따르면 (n,iterable,key)에서 n의 개수가 작을 수록 nsamllest, nlargest가 좋은 성능을 보인다고 한다.
    n이 커질수록 sorted를 사용하는 것이 더 좋은 성능을 보인다고 한다.
    또한, n이 1인 경우는 max나 min함수가 더 효율적이라고 말한다.
    """
    for bigram, count in rank:
        print(f"{bigram} {count}")

text = """
Hello!
This is the first question.
Read a text file, extract alphabet bi-grams and count them.
Finally select most frequent three bi-grams, and print them with count.
"""

extract_bigrams(text, 3)

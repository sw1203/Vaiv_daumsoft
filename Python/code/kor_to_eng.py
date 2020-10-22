"""
한글로 친 것을 초성 중성 종성으로 나눈 후 영어로 변환
ex) 바이브컴퍼니 -> qkdlqmzjavjsl
"""


# 초성 리스트. 00 ~ 18 (한글->영어)
CHOSUNG_LIST = {0: "r", 1: "R", 2: "s", 3: "e", 4: "E", 5: "f", 6: "a", 7: "q", 8: "Q", 9: "t", 10: "T", 11: "d", 12: "w", 13: "W", 14: "c", 15: "z", 16: "x", 17: "v", 18: "g"}

# 중성 리스트. 00 ~ 20 (한글->영어)
JUNGSUNG_LIST = {0: "k", 1: "o", 2: "i", 3: "O", 4: "j", 5: "p", 6: "u", 7: "P", 8: "h", 9: "jk", 10: "ho", 11: "hl", 12: "y", 13: "n", 14: "nj", 15: "np", 16: "nl", 17: "b", 18: "m", 19: "ml", 20: "l"}

# 종성 리스트. 00 ~ 27 + 1(1개 없음) (한글->영어)
JONGSUNG_LIST = {0: " ", 1: "r", 2: "R", 3: "rt", 4: "s", 5: "sw", 6: "sg", 7: "e", 8: "f", 9: "fr", 10: "fa", 11: "fq", 12: "ft", 13: "fx", 14: "fv", 15: "fg", 16: "a", 17: "q", 18: "qt", 19: "t", 20: "T", 21: "d", 22: "w", 23: "c", 24: "z", 25: "x", 26: "v", 27: "g"}


ONLY_CHOSUNG_LIST = {'ㄱ': "r", 'ㄲ': "R", 'ㄴ': "s", 'ㄷ': "e", 'ㄸ': "E", 'ㄹ': "f", 'ㅁ': "a", 'ㅂ': "q", 'ㅃ': "Q", 'ㅅ': "t", 'ㅆ': "T", 'ㅇ': "d", 'ㅈ': "w", 'ㅉ': "W", 'ㅊ': "c", 'ㅋ': "z", 'ㅌ': "x", 'ㅍ': "v", 'ㅎ': "g"}
# 참고: https://github.com/neotune/python-korean-handler/blob/master/korean_handler.py
# 참고: https://frhyme.github.io/python/python_korean_englished/


def kor_to_eng(text: str) -> str:
    tmp = ""
    for char in text:
        if ord("가") <= ord(char) <= ord("힣"):
            cho = (ord(char) - ord("가")) // 588
            tmp += CHOSUNG_LIST[cho]

            jung = ((ord(char) - ord('가')) - (588*cho)) // 28
            tmp += JUNGSUNG_LIST[jung]

            jong = int((ord(char) - ord('가')) - 588*cho - 28*jung)
            if jong != 0:
                tmp += JONGSUNG_LIST[jong]
        elif ord("ㄱ") <= ord(char) <= ord("ㅎ"):
            tmp += ONLY_CHOSUNG_LIST[char]
        else:
            tmp += char
    return tmp


while True:
    text = input()

    if text =='q':
        print("종료")
        break
    
    else:
        print(kor_to_eng(text))

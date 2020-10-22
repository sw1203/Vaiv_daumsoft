"""
한글로 친 것을 초성 중성 종성으로 나누기
ex) 바이브컴퍼니 -> [ㅂ,ㅏ,ㅇ,ㅣ,ㅂ,ㅡ,ㅋ,ㅓ,ㅁ,ㅍ,ㅓ,ㄴ,ㅣ}
"""


# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 참고: https://github.com/neotune/python-korean-handler/blob/master/korean_handler.py
# 참고: https://frhyme.github.io/python/python_korean_englished/


def divide_kor(text: str) -> list:
    tmp = []
    for char in text:
        if ord("가") <= ord(char) <= ord("힣"):
            cho = (ord(char) - ord("가")) // 588
            tmp.append(CHOSUNG_LIST[cho])

            jung = ((ord(char) - ord('가')) - (588*cho)) // 28
            tmp.append(JUNGSUNG_LIST[jung])

            jong = int((ord(char) - ord('가')) - 588*cho - 28*jung)
            if jong != 0:
                tmp.append(JONGSUNG_LIST[jong])
        else:
            tmp.append(char)
    return tmp


if __name__ == '__main__':
    while True:
        text = input()

        if text == "q":
            print("종료")
            break

        else:
            print(divide_kor(text))

from itertools import permutations


def decompose_compound_noun(dic_path, text, option):
    find_noun = []
    answer = []
    with open(dic_path, 'r', encoding="UTF-8") as file:
        nouns = [line.strip() for line in file.readlines()]

    for begin in range(len(text)):
        for end in range(begin, len(text)+1):
            word = text[begin:end]
            if word in nouns:
                find_noun.append(word)

    for num in range(len(find_noun), 0, -1):
        my_permutation = permutations(find_noun, num)
        for i in my_permutation:
            if "".join(i) == text:
                answer.append("+".join(i))

    if not answer:
        print("fail")
    elif option == "all":
        for i in answer:
            print(i)
    elif option == "longest":
        print(answer[-1])
    elif option == "shortest":
        print(answer[0])
    else:
        print("존재하지 않는 옵션입니다.")


decompose_compound_noun("noun.txt", "대학생선교회", "all")

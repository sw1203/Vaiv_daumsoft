def decompose_compound_noun(dic_path, text, option="all"):
    noun = set()
    with open(dic_path, 'r', encoding="UTF-8") as file:
        for line in file.readlines():
            noun.add(line.strip())

    answer = []
    function_options = {
        "all": compound_noun,
        "shortest": shortest_compound_noun,
        "longest": longest_compound_noun
    }

    function_options[option](noun, text, 0, answer)


def compound_noun(dictionary, text, start, answer):
    flag = False
    n = len(text) - start
    for index in range(1, n + 1):
        word = text[start:start+index]
        if word in dictionary:
            answer.append(word)
            if n == index:
                print("+".join(answer))
                flag = True
            elif compound_noun(dictionary, text, start+index, answer):
                flag = True
            answer.pop()


def shortest_compound_noun(dictionary, text, start, answer):
    n = len(text) - start
    for index in range(1, n + 1):
        word = text[start:start + index]
        if word in dictionary:
            answer.append(word)
            if n == index:
                print("+".join(answer))
                return True
            elif shortest_compound_noun(dictionary, text, start + index, answer):
                return True
            answer.pop()
    return False


def longest_compound_noun(dictionary, text, start, answer):
    n = len(text) - start
    for index in range(n, 0, -1):
        word = text[start:start + index]
        if word in dictionary:
            answer.append(word)
            if n == index:
                print("+".join(answer))
                return True
            elif longest_compound_noun(dictionary, text, start + index, answer):
                return True
            answer.pop()
    return False


print("case 1 : all")
decompose_compound_noun("noun.txt", "대학생선교회")
print("-" * 10)
print("case 2: shortest")
decompose_compound_noun("noun.txt", "대학생선교회", "shortest")
print("-" * 10)
print("case 3: longest")
decompose_compound_noun("noun.txt", "대학생선교회", "longest")
f = open("words_crocodile.txt", "r")

words = f.readlines()

words_ease = list(set(words[0].split("'")))

for i in words_ease:
    if i == "]\n":
       words_ease.remove(i)
    elif i == "[":
        words_ease.remove(i)
    elif i == ", ":
        words_ease.remove(i)
words_ease1 = []
for i in words_ease:
    words_ease1.append(i)
print(words_ease[19])
#
# from parser_words import get_ez
#
# print(get_ez()[0])

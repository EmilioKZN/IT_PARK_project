import requests
from bs4 import BeautifulSoup
url = "https://slotobzor.com/populyarnye/interesnye-slova-dlya-igry-krokodil/"
result = requests.get(url).text
soup = BeautifulSoup(result, "html.parser")
lvl = soup("h2", style= "text-align: center;")
words = soup.findAll('ol')

words_light = words[0].text.split('\n')
for i in words_light:
    if i == "":
        words_light.remove(i)



words_middle = words[1].text.split('\n')
for i in words_middle:
    if i == "":
        words_middle.remove(i)



words_hard = words[2].text.split('\n')
for i in words_hard:
    if i == "":
        words_hard.remove(i)

words_file_write = open("words_crocodile.txt", "w+", encoding= "UTF-8")
with open("words_crocodile.txt"):
    words_file_write.write(str(words_light) + "\n")
    words_file_write.write(str(words_middle) + "\n")
    words_file_write.write(str(words_hard) + "\n")
    words_file_write.close()





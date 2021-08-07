
import re
import math

import numpy as np
import matplotlib.pyplot as plt

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
import itertools



urls = [
        "https://www.nasa.gov/specials/artemis/",
        "https://www.kennedyspacecenter.com/blog/what-is-the-artemis-program",
        "https://www.bbc.com/news/science-environment-54156798",
        "https://www.boeing.com/space/space-launch-system/index.page",
        "https://www.space.com/nasa-artemis-1-sls-moon-rocket-stacked-photos",
        "https://www.spacex.com/vehicles/starship/",
        "https://www.space.com/nasa-plans-artemis-moon-base-beyond-2024.html",
        "https://www.spacex.com/human-spaceflight/mars/",
        "https://www.space.com/spacex-launch-astronauts-mars-2024",
        "https://www.space.com/nasa-sls-megarocket-engine-test-artemis-1-march-2021",

]

def all_words_list(urls):

    all_words = []
    
    for url in urls:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()  
        text = soup.get_text()
        text = re.sub(r'[^\w]', ' ', text)
        bagofwords = text.split(' ')
        bagofwords = [x for x in bagofwords if x]
        all_words.append(bagofwords)

    return all_words

def list_struct(): return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



all_words = all_words_list(urls)


words_tf = defaultdict(list_struct)
words_idf = {}
words_tf_idf = defaultdict(list_struct)
words_tf_idf_sum = {}

for i in range(len(all_words)):
    words = all_words[i]
    n = len(words)
    for word in words:
        tf_list = words_tf[word]
        tf_list[i] = ((tf_list[i] * n) + 1) / n
        words_tf[word] = tf_list




for key in words_tf.keys():
    zero = words_tf[key].count(0)
    f = 10 - zero

    words_idf[key] = math.log10(10/f)


for key in words_tf.keys():
    Sum = 0.0
    for i in range(len(words_tf[key])):
        tf = words_tf[key][i]
        score = tf * words_idf[key]
        Sum += score
        words_tf_idf[key][i] = score
    words_tf_idf_sum[key] = Sum




words_tf_idf_sum = dict(sorted(words_tf_idf_sum.items(), key=lambda item: item[1], reverse=True))

print(words_tf_idf)
print()
print()
print(words_tf_idf_sum)

sliced_words_tf_idf_sum = dict(itertools.islice(words_tf_idf_sum.items(), 20))


x = list(sliced_words_tf_idf_sum.keys())
y = list(sliced_words_tf_idf_sum.values())

ind = np.arange(len(y))

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)
fig.savefig('test2png.png', dpi=100)
ax.barh(ind, y)
ax.set_yticks(ind)
ax.set_yticklabels(x)

ax.bar_label(ax.containers[0])
plt.gca().invert_yaxis()
plt.title("Top 20 Most Relevant Word in 10 Websites")
plt.show()











    





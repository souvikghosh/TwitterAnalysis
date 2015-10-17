import json
import pandas as pd
import matplotlib.pyplot as plt
import re

tweets_data_path = '/home/souvik/PythonTwitterAnalysis/twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
    except:
        continue
    if not all(x in tweet for x in ['text', 'lang', 'place']):
        continue
    if tweet['place'] and not 'country' in tweet['place']:
        continue
    tweets_data.append(tweet)


tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet:tweet['text'] if tweet['text'] else '', tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

tweets['real madrid'] = tweets['text'].apply(lambda tweet: word_in_text('real madrid', tweet))
tweets['barcelona'] = tweets['text'].apply(lambda tweet: word_in_text('barcelona', tweet))
tweets['manchester united'] = tweets['text'].apply(lambda tweet: word_in_text('manchester united', tweet))

print tweets['real madrid'].value_counts()[True]
print tweets['barcelona'].value_counts()[True]
print tweets['manchester united'].value_counts()[True]

teams = ['real madrid', 'barcelona', 'manchester united']
tweets_by_teams = [tweets['real madrid'].value_counts()[True], tweets['barcelona'].value_counts()[True], tweets['manchester united'].value_counts()[True]]

x_pos = list(range(len(teams)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_teams, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: real madrid vs. barcelona vs. manchester united (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(teams)
plt.grid()
plt.show()


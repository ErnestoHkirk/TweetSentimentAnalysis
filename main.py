
import twitter
import boto3

AWS_ACCESS_KEY = 'x'
AWS_SECRET_KEY = 'x'
TWITTER_CONSUMER_KEY = 'x'
TWITTER_CONSUMER_SECRET = 'x'
TWITTER_ACCESS_TOKEN_KEY = 'x'
TWITTER_ACCESS_TOKEN_SECRET = 'x'

# twitter authentication
TWITTER_CLIENT = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                             consumer_secret=TWITTER_CONSUMER_SECRET,
                             access_token_key=TWITTER_ACCESS_TOKEN_KEY,
                             access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

# boto3 authentication
SESSION = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)

COMPREHEND = SESSION.client(service_name='comprehend', region_name='us-west-2')


def get_sentiment(text):
    sentiment_response = COMPREHEND.detect_sentiment(Text=text, LanguageCode='en')
    return sentiment_response["Sentiment"]


user = "MotivatinQuotes"

statuses = TWITTER_CLIENT.GetUserTimeline(screen_name=user, count=50)
tweets = [s.text for s in statuses]

positive = 0
neutral = 0
negative = 0
str1 = ""

for index, tweet in enumerate(tweets):
    print(index + 1)
    # print(tweet)
    # print(get_sentiment(tweet), "\n")
    sentiment = get_sentiment(tweet)
    index += 1

    if sentiment == "POSITIVE":
        positive += 1

    if sentiment == "NEUTRAL":
        neutral += 1

    if sentiment == "NEGATIVE":
        negative += 1

# currently redundant, may need in future
# print("Positive Tweets = ", positive)
# print("Neutral Tweets = ", neutral)
# print("Negative Tweets = ", negative)

# api key - plotly
# 'x' also not necessary for functionality on local host

import plotly.graph_objects as go
colors = ['green', 'yellow', 'red']

fig = go.Figure(data=[go.Pie(labels=['Positive', 'Neutral', 'Negative'],
                             values=[positive, neutral, negative])])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))

fig.update(layout_title_text='Tweet Sentiment Analytics, User: @' + user,
           layout_showlegend=True)

fig.show()



# plotly test code
# import plotly
#
# import chart_studio.plotly as py
# import plotly.graph_objs as go
#
# tls.set_credentials_file(“myusername”, “my_API_Key”)
#
# py.sign_in(“myusername”, “my_API_Key”)
#
# trace0 = go.Scatter(
#     x=[1, 2, 3, 4],
#     y=[10, 15, 13, 17]
# )
# trace1 = go.Scatter(
#     x=[1, 2, 3, 4],
#     y=[16, 5, 11, 9]
# )
# data = [trace0, trace1]
#
# first_plot_url = py.plot(data, filename='apple stock moving average', auto_open=True,)
# print(first_plot_url)

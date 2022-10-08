import tweepy
import json

def like_count_of_tweet(tweet : tweepy.Tweet):
    return tweet.public_metrics["like_count"]


if __name__ == "__main__":
    # Load credentials from json file.
    with open("twitter_credentials.json", "r") as file:
        cred_data = json.load(file)

    consumer_key = cred_data['CONSUMER_KEY']
    consumer_secret = cred_data['CONSUMER_SECRET']
    access_token = cred_data['ACCESS_TOKEN']
    access_token_secret = cred_data['ACCESS_SECRET']
    bearer_token = cred_data['BEARER_TOKEN']

    WOEID_germany = 23424829

    auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
    )

    api = tweepy.API(auth)
    client = tweepy.Client(bearer_token=bearer_token,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret)

    # Get the latest trends from germany.
    trends = api.get_place_trends(WOEID_germany)
    trendnames = [t['name'] for t in trends[0]['trends']]

    for name in trendnames[0:3]:
        print(name)

    query = f"{trendnames[2]} -is:retweet lang:de"
    tweet_fields = "created_at,public_metrics,author_id" #,non_public_metrics,public_metrics,organic_metrics,promoted_metrics"

    response = client.search_recent_tweets(query=query, tweet_fields=tweet_fields, sort_order="relevancy", max_results=50)

    tweets:list = response.data
    tweets.sort(key=like_count_of_tweet, reverse=True)

    embed_html_code = []

    for t in tweets[0:10]:
        # Build the html code to embed a twitter post.
        text = t.text
        post_id = t.id
        author_id = t.author_id
        user_resp = client.get_user(id=author_id, user_fields='url')
        user_data = user_resp.data
        name = user_data['name']
        authorname = user_data['username']
        author_url = user_data['url']

        embed_html_code.append(f"""
        <blockquote class="twitter-tweet" data-dnt="true" data-theme="light">
        <p lang="de" dir="ltr">
        {text}
        </p>&mdash; {name} (@{authorname}) 
        <a href="https://twitter.com/{authorname}/status/{post_id}">October 8, 2022</a>
        </blockquote>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script><br><br>
        """)

    with open("index.html", 'w', encoding="utf-8") as html_file:
        for entry in embed_html_code:
            html_file.write(entry)
    

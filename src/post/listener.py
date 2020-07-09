#!/usr/bin/env python

import re
import logging
import tweepy
from api import create_api

logging.basicConfig(level=logging.INFO)

class Command:

    hashtag = '#jobpost'

    def __init__(self, name_of_command):
        self.bot_username = '@post_mee'
        self.name_of_command = name_of_command

    def create_command(self):
        """Concatenates the command"""
        return f'{self.bot_username} {self.name_of_command}'

update_post = Command('update post').create_command()
delete_post = Command('delete post').create_command()
beautify_post = Command('beautify post').create_command()
follow_company = Command('follow').create_command()
currently_looking = Command('looking for work').create_command()

class BotListener(tweepy.StreamListener):
    """Listens for keywords real-time"""

    def __init__(self, api):
        """Passes in the api for API functionality"""
        self.api = api
        self.retweet_id = None

    def on_status(self, tweet):
        """Responds to the keywords that are on twitter and act accordingly"""

        is_retweeted = True if (not tweet.retweeted) and ('RT @' not in tweet.text) else False

        if is_retweeted and (update_post not in tweet.text) and (delete_post not in tweet.text) and (beautify_post not in tweet.text) and (follow_company not in tweet.text) and (currently_looking not in tweet.text):

            # Store the retweet object in attr.
            self.retweet_id = self.api.retweet(tweet.id) # invoke the retweet method and return an object containing info about the retweet     
            logging.info('Tweet successfully retweeted')

        if is_retweeted:
            if (delete_post in tweet.text):
                
                # Grab User info
                user = self.api.get_status(tweet.id)

                # Unretweet the tweet
                logging.info('Getting retweet info...')
                self.api.unretweet(self.retweet_id.id)

                # Reply to user 
                message = f'Hey @{user.user.screen_name}! I deleted your job post'
                logging.info('Reply to Tweeter User...')
                self.api.update_status(status=message, in_reply_to_status_id=user.id)
                logging.info('Reply successful')
        
        if is_retweeted:
            if (update_post in tweet.text):
                pass

        if is_retweeted:
            if (follow_company in tweet.text):

                # Grab User info
                user = self.api.get_status(tweet.id)

                mentions = re.findall('(@[\w]+)', tweet.text, re.M)

                logging.info('Following users...')
                for screen_name in mentions:
                    if (screen_name == '@post_mee'):
                        continue

                    self.api.create_friendship(screen_name)

                self.api.update_status(status=f'Followed! @{user.user.screen_name}', in_reply_to_status_id=user.id)
                logging.info('Successfully followed all users')



    def on_error(self, error):
        """Logs any errors that occur"""
        logging.error(error)

def main():
    api = create_api()
    bot_listen = BotListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=bot_listen)
    stream.filter(track=[Command.hashtag, update_post, delete_post, beautify_post, follow_company, currently_looking])

if __name__ == "__main__":
    main()
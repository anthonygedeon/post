import tweepy
import logging
from decouple import config

def create_api():
    """ 
        Creates the API that is used to handle the functionality of the Twitter API

        Returns:
        object:API
    """

    # API KEYS
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    access_token = config('ACCESS_TOKEN')
    access_token_secret = config('ACCESS_TOKEN_SECRET')

    # ACTIVATE API
    authorize = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authorize.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authorize, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # CHECK FOR ERRORS
    try:
        api.verify_credentials()
    except Exception as error:
        logging.error('An error occured when creating API')
        raise error

    logging.info('API Created!')
    
    return api
import aiohttp
import random
import json
import time
import sys
import os
import requests
from src.getuseragent import User_Agent
from colorama import Fore, init
from datetime import datetime
data_ora_curenta = datetime.now()
format_data_ora = data_ora_curenta.strftime("%H:%M:%Y")
init()
class Client:
    def __init__(self, username,c, use_proxy):
        self.username = username
        self.use_proxy = use_proxy
        self.session = aiohttp.ClientSession()
        self.csrf_token = os.urandom(int(32/2)).hex()
        self.user_agent_ = User_Agent.make_random_user_agent()
        self.countx = self.get_json_data()
        self.PROXYES = self.countx['TWITTER_PROXY']
        self.c = c
    async def get_proxy(self):
        self.proxy = None
        if self.use_proxy == True:
            self.proxy = self.PROXYES
            
            
    async def test_proxy(self):
        pass
        
    async def get_guest_token(self):
        headers = {'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-csrf-token': self.csrf_token, 'User-Agent': self.user_agent_}
        return await self.session.post("https://api.twitter.com/1.1/guest/activate.json", headers=headers, proxy=self.proxy,timeout=5)
                     
    async def get_username_details(self):
        user_agent_ = User_Agent.make_random_user_agent()
        headers = {
            'User-Agent': self.user_agent_,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'content-type': 'application/json',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-guest-token': self.guest_token,
            'x-twitter-client-language': 'en',
            'x-twitter-active-user': 'yes',
            'Origin': 'https://twitter.com',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://twitter.com/',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }
        params = {
            'variables': '{"screen_name":"'+self.username+'","withSafetyModeUserFields":true}',
            'features': '{"hidden_profile_likes_enabled":true,"hidden_profile_subscriptions_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
            'fieldToggles': '{"withAuxiliaryUserLabels":false}',
        }
        return await self.session.get("https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName",params=params, headers=headers, proxy=self.proxy, timeout=5)
    
    async def login(self):
        try:
            FOLLOWERS_MORE = self.countx['FOLLOWERS_NUMBER']
            response = await self.get_guest_token()
            data = await response.json()
            self.guest_token = data["guest_token"]
            verified_type = ''
            count = 0
            response = await self.get_username_details()
            data = await response.json()
            if 'User is suspended' in str(data):
                user = data['data']['user']['result']['message']
                print(f'{Fore.MAGENTA}[{Fore.RED} {self.c} {Fore.MAGENTA}] [{Fore.RED} {self.username} {Fore.MAGENTA}] [{Fore.RED} {user} {Fore.MAGENTA}] {Fore.RESET}')
            else:
                favourites_count = data['data']['user']['result']['legacy']['friends_count']
                followers_count = data['data']['user']['result']['legacy']['followers_count']
                screen_name = data['data']['user']['result']['legacy']['screen_name']
                screen_name = screen_name.encode('utf-8').decode('utf-8')
                profile_image_url_https = data['data']['user']['result']['legacy']['profile_image_url_https']
                data = f'{self.username}:{followers_count}:{favourites_count}:{profile_image_url_https}'
                if int(followers_count) >= int(FOLLOWERS_MORE) and int(favourites_count) > 0:
                    with open('RESULT/more_than.txt', 'a', encoding='utf-8', errors='ignored') as file_out:
                        file_out.write(f'{data}\n')
                    print(f'{Fore.MAGENTA}[{Fore.GREEN} {self.c} {Fore.MAGENTA}] [{Fore.GREEN} {self.username} {Fore.MAGENTA}] [{Fore.GREEN} {followers_count} {Fore.MAGENTA}] {Fore.RESET}')
                else:
                    with open('RESULT/smaller_than.txt', 'a', encoding='utf-8', errors='ignored') as file_out:
                        file_out.write(f'{data}\n')
                    print(f'{Fore.MAGENTA}[{Fore.RED} {self.c} {Fore.MAGENTA}] [{Fore.RED} {self.username} {Fore.MAGENTA}] [{Fore.RED} {followers_count} {Fore.MAGENTA}] {Fore.RESET}')

        except Exception as e:
            print(f'{Fore.YELLOW} WARNING - {Fore.MAGENTA}[{Fore.RED} {self.c} {Fore.MAGENTA}] [{Fore.RED} {self.username} {Fore.MAGENTA}] [{Fore.RED} {e} {Fore.MAGENTA}] {Fore.RESET}')
            with open('RESULT/error.txt', 'a', encoding='utf-8', errors='ignored') as file_out:
                file_out.write(f'{self.username}\n')
            pass
    
    async def close(self):
        if self.session:
            if not self.session.closed:
                await self.session.close()
    
    def get_json_data(self):
        with open('config.json', 'r') as f:
            data = json.load(f)
        return data
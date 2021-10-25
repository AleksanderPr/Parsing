import scrapy
import re
import json
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 
    inst_pwd = 
    users_for_parse = ['ryzhiknata', 'oxana_metlinskaya']
    url = 'https://i.instagram.com/api/v1/friendships'


    def parse(self, response: HtmlResponse):
        print()
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd},
            headers={'x-csrftoken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user in self.users_for_parse:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_parse,
                    cb_kwargs={'username': user}
                )


    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        followers_page = f'{self.url}/{user_id}/followers/?count=12&search_surface=follow_list_page'
        following_page = f'{self.url}/{user_id}/following/?count=12'
        yield response.follow(followers_page,
                              callback=self.users_followers,
                              cb_kwargs={'username': username,
                                         'user_id': user_id})

        yield response.follow(following_page,
                              callback=self.users_following,
                              cb_kwargs={'username': username,
                                         'user_id': user_id})

    def users_followers(self, response: HtmlResponse, username, user_id):
        j_data = response.json()
        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            followers_page = f'{self.url}/{user_id}/followers/?count=12&max_id={next_max_id}&search_surface=follow_list_page'
            yield response.follow(followers_page,
                                  callback=self.users_followers,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id})
        users = j_data.get('users')
        for user in users:
            item = InstaparserItem(username=username,
                                  user_id=user_id,
                                  folower_username=user.get('username'),
                                  folower_id=user.get('pk'),
                                  folower_photo=user.get('profile_pic_url'),
                                  )
            yield item

    def users_following(self, response: HtmlResponse, username, user_id):
        j_data = response.json()
        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            following_page = f'{self.url}/{user_id}/following/?count=12&max_id={next_max_id}'
            yield response.follow(following_page,
                                  callback=self.users_following,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id})
        users = j_data.get('users')
        for user in users:
            item = InstaparserItem(username=username,
                                 user_id=user_id,
                                 folowwing_username=user.get('username'),
                                 folowwing_user_id=user.get('pk'),
                                 folowwing_photo=user.get('profile_pic_url'),
                                 )
            yield item



    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError
from datetime import datetime

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import webtext
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer


import json
import os.path
import logging
import argparse
import time

from app.client import MyClient
from app.client import getWebAPI

class Comment:

    # структурка для коммента, в которой хранятся id поста, автор, время, текст коммента,
    # также отредактированный текст коммента и его эмоциональный окрас

    def __init__(self, media_id, com_author, com_time, com_text, aggregated_com_text='', emotional_color='neu'):
        self.media_id = media_id
        self.com_author = com_author
        self.com_time = com_time
        self.com_text = com_text
        self.emotional_color = emotional_color


class Post:

    # структурка для поста: id поста и число комментов к нему
    def __init__(self, media_id, comments_count):
        self.media_id = media_id
        self.comments_count = comments_count

class Analyser:
    # возвращает id юзера по нику
    def getUserID(api, username):
        # ждем некоторое время, так как нельзя подряд делать бесконечное число http-запросов
        time.sleep(3)
        return api.user_info2(username)['id']

    # возвращает media_id всех медиа профиля


    def getProfileMediaList(api, username):
        user_id = getUserID(api, username)

        media_list = []
        next_page = ''
        has_next_page = True

        while (has_next_page):

            # ждем некоторое время, так как нельзя подряд делать бесконечное число http-запросов
            time.sleep(3)

            all_media = api.user_feed(
                user_id, count=50, end_cursor=next_page, extract=False)

            # записываем id полученных медиа профиля в лист
            for item in all_media['data']['user']['edge_owner_to_timeline_media']['edges']:
                media_list.append(Post(
                    item['node']['shortcode'], item['node']['edge_media_preview_comment']['count']))

            # смотрим, есть ли следующая страница
            has_next_page = all_media['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

            # присваиваем ссылку на следующую страницу
            next_page = all_media['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

        return media_list

    # возвращает список всех комментов к посту


    def getPostComments(api, media_id):
        res = []
        max_id = ' '
        next_max_id = ''

        while (max_id != next_max_id):

            # ждем некоторое время, так как нельзя подряд делать бесконечное число http-запросов
            time.sleep(3)

            max_id = next_max_id
            post_comments = api.media_comments(
                media_id, count=50, end_cursor=max_id)  # загружаем комменты

            # если комменты кончились, ливаем
            if (len(post_comments) == 0):
                break

            # смотрим, на каком комменте закончилась выгрузка
            # реверсим массив комментов, чтобы итоговый список получился в убывающем порядке
            next_max_id = post_comments[0]['id']
            post_comments.reverse()

            # оставляем только нужную информацию
            for comm in post_comments:
                res.append(
                    Comment(media_id, comm['owner']['username'], comm['created_at'], comm['text']))

        return res

    # возвращает все комменты к списку постов


    def getPostsComments(api, posts):
        res = []
        for item in posts:
            res.extend(getPostComments(api, item.media_id))

        return res

    # возвращает общее число комментариев к списку постов


    def getSumCommentsCount(posts):
        cnt = 0
        for item in posts:
            cnt += item.comments_count

        return cnt

    # возвращает общее число постов с комментариями из заданного списка постов


    def getPostsWithCommentsCount(posts):
        cnt = 0
        for item in posts:
            if (item.comments_count > 0):
                cnt += 1

        return cnt

    # производит следующие операции с текстом комментов:
    # убирает все эмодзи из коммента
    # заменяет все ссылки на никнейм типа @mr_justadog на нейтральное обращение - man


    def filterComments(comments):
        res = []
        return res

    # заполняет поле emotional_color в списке comments


    def getEmotionalColorComments(comments, positive_emojis_list, negative_emojis_list):
        # загружаем анализатор
        sia = SentimentIntensityAnalyzer()

        # относим коммент к одному из 3-х типов
        for i in range(len(comments)):
            scores = sia.polarity_scores(comments[i].com_text)
            neg = scores['neg']
            neu = scores['neu']
            pos = scores['pos']

            if (pos >= neg and pos >= neu):
                comments[i].emotional_color = 'pos'
            elif (neg >= pos and neg >= neu):
                comments[i].emotional_color = 'neg'
            else:
                for emoji in positive_emojis_list:
                    if (emoji in comments[i].com_text):
                        comments[i].emotional_color = 'pos'
                        break
                for emoji in negative_emojis_list:
                    if (emoji in comments[i].com_text):
                        comments[i].emotional_color = 'neg'
                        break

    # возвращает число положительных, отрицательных и нейтральных комментов из предоставленного списка комментов


    def getPosNegNeuCommentsCount(comments):
        pos = 0
        neg = 0
        for i in range(len(comments)):
            if (comments[i].emotional_color == 'neg'):
                neg += 1
            elif (comments[i].emotional_color == 'pos'):
                pos += 1
        return pos, neg, len(comments) - pos - neg

    # возвращает число положительно, отрицательно и нейтрально оцененных постов из предоставленного списка комментов к постам


    def getPosNegNeuPostsCount(comments):
        pos = 0
        neg = 0
        neu = 0
        cur_pos = 0
        cur_neg = 0
        cur_neu = 0
        last_media_id = comments[0].media_id if len(comments) > 0 else ''
        for i in range(len(comments)):
            if (last_media_id != comments[i].media_id):
                if (cur_pos > cur_neg):
                    pos += 1
                elif (cur_neg > cur_pos):
                    neg += 1
                elif (cur_neu + cur_neg + cur_pos > 0):
                    neu += 1
                cur_pos = cur_neg = cur_neu = 0
            if (comments[i].emotional_color == 'neg'):
                cur_neg += 1
            elif (comments[i].emotional_color == 'pos'):
                cur_pos += 1
            else:
                cur_neu += 1
            last_media_id = comments[i].media_id
        if (cur_pos > cur_neg):
            pos += 1
        elif (cur_neg > cur_pos):
            neg += 1
        elif (cur_neu + cur_neg + cur_pos > 0):
            neu += 1
        return pos, neg, neu

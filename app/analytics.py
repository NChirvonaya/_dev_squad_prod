"""Analyze instagram profile."""
import codecs
import hashlib
import os
import random
import string
import time
import random

import threading

import json
from dataclasses import dataclass, asdict

# import nltk
from instagram_web_api import (
    Client,
    ClientCompatPatch,
    ClientError,
    ClientLoginError,
)

# from nltk.corpus import webtext
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# from nltk.stem.porter import PorterStemmer
# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.tokenize import (
#     PunktSentenceTokenizer,
#     sent_tokenize,
#     word_tokenize
# )

import pymongo


# просто Client не работает, поэтому переопределена
# функция _extract_rhx_gis для захода в web инста
class InstClient(Client):
    """Instagram client."""

    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = "".join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode())


class Comment:
    """Cтруктурка для коммента.

    В структуре хранятся id поста, автор, время, текст коммента,
    также отредактированный текст коммента и его эмоциональный окрас
    """

    def __init__(
        self,
        media_id,
        com_author,
        com_time,
        com_text,
        aggregated_com_text="",
        emotional_color="neu",
    ):
        """Cтруктурка для коммента.

        В структуре хранятся id поста, автор, время, текст коммента,
        также отредактированный текст коммента и его эмоциональный окрас
        """
        self.media_id = media_id
        self.com_author = com_author
        self.com_time = com_time
        self.com_text = com_text
        self.aggregated_com_text = aggregated_com_text
        self.emotional_color = emotional_color


class Post:
    """Структурка для поста.

    id поста и число комментов к нему.
    """

    def __init__(self, media_id, comments_count):
        """Структурка для поста.

        id поста и число комментов к нему.
        """
        self.media_id = media_id
        self.comments_count = comments_count


@dataclass
class ProfileStats:
    """Profile stats."""

    username: str
    _id: str = ""

    w_com: int = 0
    wt_com: int = 0
    post_pos: int = 0
    post_neg: int = 0
    post_neu: int = 0
    com_all: int = 0
    com_pos: int = 0
    com_neg: int = 0
    com_neu: int = 0
    com_unq: int = 0


@dataclass
class PostStats:
    """Post stats."""

    post_link: str
    _id: str = ""

    com_pos: int = 0
    com_neg: int = 0
    com_neu: int = 0
    com_unq_cnt: int = 0


class InstAnalytics:
    """Analyze instagram user."""

    def __init__(self):
        """Analyze instagram user."""
        self.username = None

        self._wait_time: int = 3
        self._api: InstClient = self._get_web_api()

        self._mongo_host: str = os.getenv('MONGO_HOST')
        self._mongo_port: int = int(os.getenv('MONGO_PORT'))
        self._mongo_db: str = os.getenv('MONGO_DB')

        self._cache_size: int = 250

        self._post_cache: dict = {}
        self._profile_cache: dict = {}

        self._ordered_profiles: set = set()
        self._ordered_posts: set = set()

    def _get_web_api(self) -> InstClient:
        # ждем некоторое время, так как нельзя подряд делать
        # бесконечное число http-запросов
        time.sleep(self._wait_time)
        return InstClient(auto_patch=True, drop_incompat_keys=False)

    def _get_user_id(self):
        """Возвращает id юзера по нику."""
        time.sleep(self._wait_time)
        return self._api.user_info2(self.username)["id"]

    def _load_symbols_list(self, rel_path: str):
        """Возвращает список символов, прочитанных из файла.

        (для считывания смайликов и разрешенных в нике символов)
        """
        # получаем абссолютный путь до файла
        abs_path = os.path.join(os.getcwd(), os.path.normpath(rel_path))
        symbols_list = []

        with codecs.open(
            abs_path, "r", encoding="utf-8", errors="ignore"
        ) as file_data:
            for line in file_data:
                for symb in line:
                    if symb != "\n" and symb != "\r":
                        symbols_list.append(symb)

        return symbols_list

    def _get_profile_media_list(self):
        """Возвращает media_id всех медиа профиля."""
        user_id = self._get_user_id()

        media_list = []
        next_page = ""
        has_next_page = True

        while has_next_page:
            time.sleep(self._wait_time)

            all_media = self._api.user_feed(
                user_id, count=50, end_cursor=next_page, extract=False
            )

            # записываем id полученных медиа профиля в лист
            for item in all_media["data"]["user"][
                "edge_owner_to_timeline_media"
            ]["edges"]:
                media_list.append(
                    Post(
                        item["node"]["shortcode"],
                        item["node"]["edge_media_preview_comment"]["count"],
                    )
                )

            # смотрим, есть ли следующая страница
            has_next_page = all_media["data"]["user"][
                "edge_owner_to_timeline_media"
            ]["page_info"]["has_next_page"]

            # присваиваем ссылку на следующую страницу
            next_page = all_media["data"]["user"][
                "edge_owner_to_timeline_media"
            ]["page_info"]["end_cursor"]

        return media_list

    def get_post_comments(self, media_id):
        """Возвращает список всех комментов к посту."""
        res = []
        max_id = " "
        next_max_id = ""

        while max_id != next_max_id:
            # ждем некоторое время, так как нельзя подряд
            # делать бесконечное число http-запросов
            time.sleep(3)

            max_id = next_max_id
            post_comments = self._api.media_comments(
                media_id, count=50, end_cursor=max_id
            )  # загружаем комменты

            # если комменты кончились, ливаем
            if len(post_comments) == 0:
                break

            # смотрим, на каком комменте закончилась выгрузка
            # реверсим массив комментов, чтобы итоговый список
            # получился в убывающем порядке
            next_max_id = post_comments[0]["id"]
            post_comments.reverse()

            # оставляем только нужную информацию
            for comm in post_comments:
                res.append(
                    Comment(
                        media_id,
                        comm["owner"]["username"],
                        comm["created_at"],
                        comm["text"],
                    )
                )

        return res

    def _get_posts_comments(self, posts):
        """Возвращает все комменты к списку постов."""
        res = []
        for item in posts:
            res.extend(self.get_post_comments(item.media_id))

        return res

    def _get_sum_comments_count(self, posts):
        """Возвращает общее число комментариев к списку постов."""
        cnt = 0
        for item in posts:
            cnt += item.comments_count

        return cnt

    def _get_posts_with_comments_count(self, posts):
        """Возвращает общее число постов с комментариями.

        (из заданного списка постов)
        """
        cnt = 0
        for item in posts:
            if item.comments_count > 0:
                cnt += 1

        return cnt

    def _filter_comments(
        self, comments, permitted_nickname_symbols, all_emoji_list
    ):
        """Filter comments.

        Производит следующие операции с текстом комментов:
        * убирает все эмодзи из коммента
        * удаляет лишние пробелы
        * заменяет все ссылки на никнейм на нейтральное обращение
        * записывает новую версию коммента в поле aggregated_com_text
        """
        for i in range(len(comments)):
            k = 0
            j = 0
            comments[i].aggregated_com_text = ""
            last_added_symb = "n"
            while k + 1 < len(comments[i].com_text):
                if comments[i].com_text[k] == "@":
                    j += 1
                    while (
                        j + 1 < len(comments[i].com_text)
                        and comments[i].com_text[j]
                        in permitted_nickname_symbols
                    ):
                        j += 1
                    # если это все же никнейм, а не просто символ '@'
                    if j - k > 1:
                        comments[i].aggregated_com_text += "Man"
                        last_added_symb = "n"
                    k = j
                elif comments[i].com_text[k] not in all_emoji_list:
                    comments[i].aggregated_com_text += comments[i].com_text[k]
                    last_added_symb = comments[i].com_text[k]
                    k += 1
                elif last_added_symb != " " or comments[i].com_text[k] != " ":
                    last_added_symb = comments[i].com_text[k]
                    k += 1
                else:
                    k += 1

    def _get_emotional_color_comments(
        self, comments, positive_emoji_list, negative_emoji_list
    ):
        """Заполняет поле emotional color в списке comments."""
        # загружаем анализатор
        sia = SentimentIntensityAnalyzer()

        # относим коммент к одному из 3-х типов
        # запускаем классификатор на аггрегированном комменте
        # если коммент определяется классификатором как нейтральный,
        # смотрим на присутствующие в оригинальном комменте смайлы
        # в таком случае, если присутствуют абсолютно положительные смайлы,
        # то коммент положительный
        # если абсолютно положительных смайлов нет, коммент негативный
        # иначе коммент остается нейтральным
        for i in range(len(comments)):
            scores = sia.polarity_scores(comments[i].aggregated_com_text)
            neg = scores["neg"]
            neu = scores["neu"]
            pos = scores["pos"]

            if pos > neg and pos >= neu:
                comments[i].emotional_color = "pos"
            elif neg > pos and neg >= neu:
                comments[i].emotional_color = "neg"
            else:
                for emoji in negative_emoji_list:
                    if emoji in comments[i].com_text:
                        comments[i].emotional_color = "neg"
                        break
                for emoji in positive_emoji_list:
                    if emoji in comments[i].com_text:
                        comments[i].emotional_color = "pos"
                        break

    def _get_pos_neg_neu_comments_count(self, comments):
        """Возвращает гистаграмму комментов.

        Число положительных, отрицательных и нейтральных комментов
        из предоставленного списка комментов.
        """
        pos = 0
        neg = 0
        for i in range(len(comments)):
            if comments[i].emotional_color == "neg":
                neg += 1
            elif comments[i].emotional_color == "pos":
                pos += 1
        return pos, neg, len(comments) - pos - neg

    def _get_pos_neg_neu_posts_count(self, comments):
        """Возвращает гистаграмму комментов.

        Число положительных, отрицательных и нейтральных комментов
        из предоставленного списка комментов к постам.
        """
        pos = 0
        neg = 0
        neu = 0
        cur_pos = 0
        cur_neg = 0
        cur_neu = 0
        last_media_id = comments[0].media_id if len(comments) > 0 else ""
        for i in range(len(comments)):
            if last_media_id != comments[i].media_id:
                if cur_pos > cur_neg:
                    pos += 1
                elif cur_neg > cur_pos:
                    neg += 1
                elif cur_neu + cur_neg + cur_pos > 0:
                    neu += 1
                cur_pos = cur_neg = cur_neu = 0
            if comments[i].emotional_color == "neg":
                cur_neg += 1
            elif comments[i].emotional_color == "pos":
                cur_pos += 1
            else:
                cur_neu += 1
            last_media_id = comments[i].media_id
        if cur_pos > cur_neg:
            pos += 1
        elif cur_neg > cur_pos:
            neg += 1
        elif cur_neu + cur_neg + cur_pos > 0:
            neu += 1
        return pos, neg, neu

    def _get_post_id_by_link(self, link):
        """Возвращает id поста из ссыслки на пост."""
        parts = link.split("/")
        return parts[4]

    def _get_commentators_count(self, comments):
        """Возвращает число уникальных авторов.

        Авторов комментариев из предоставленного списка комментов.
        """
        commentators = set()
        for i in range(len(comments)):
            if comments[i].com_author not in commentators:
                commentators.add(comments[i].com_author)

        return len(commentators)

    def order_profile_stats(self, username: str):
        """Возвращает статистику профиля."""
        self.username = username
        saved = self.get_profile_results(username, order=False)
        if saved:
            return saved
        print("started")
        # получаем списки смайлов и символов
        all_emoji_list = self._load_symbols_list(
            "app/helper_files/all_emoji_list"
        )
        positive_emoji_list = self._load_symbols_list(
            "app/helper_files/positive_emoji_list"
        )
        negative_emoji_list = self._load_symbols_list(
            "app/helper_files/negative_emoji_list"
        )
        permitted_nickname_symbols = self._load_symbols_list(
            "app/helper_files/nickname_symbols_list"
        )
        print("next_1")

        # получаем список постов в профиле
        posts = self._get_profile_media_list()
        print("next_2")
        # общее число постов с комментами
        posts_with_comments_cnt = self._get_posts_with_comments_count(posts)
        print("next_3")

        # общее число постов без комментов
        posts_without_comments_cnt = len(posts) - posts_with_comments_cnt

        # получаем список всех комментов в профиле
        comments = self._get_posts_comments(posts)
        # немного причесываем комменты
        self._filter_comments(
            comments, permitted_nickname_symbols, all_emoji_list
        )
        print("next_4")
        # вычисляем эмоциональный окрас комментов
        self._get_emotional_color_comments(
            comments, positive_emoji_list, negative_emoji_list
        )

        # число положительных, отрицательных и нейтральных постов в профиле
        (
            pos_posts_cnt,
            neg_posts_cnt,
            neu_posts_cnt,
        ) = self._get_pos_neg_neu_posts_count(comments)

        # общее число комментов к профилю
        comments_cnt = self._get_sum_comments_count(posts)

        # число положительных, отрицательных и нейтральных комментов в профиле
        (
            pos_comms_cnt,
            neg_comms_cnt,
            neu_comms_cnt,
        ) = self._get_pos_neg_neu_comments_count(comments)

        # число различных комментаторов в профиле
        commentators_cnt = self._get_commentators_count(comments)
        print("next_5")

        # заполняем итоговый массив
        stats_dict = {
            "username": username,
            "w_com": posts_with_comments_cnt,
            "wt_com": posts_without_comments_cnt,
            "post_pos": pos_posts_cnt,
            "post_neg": neg_posts_cnt,
            "post_neu": neu_posts_cnt,
            "com_all": comments_cnt,
            "com_pos": pos_comms_cnt,
            "com_neg": neg_comms_cnt,
            "com_neu": neu_comms_cnt,
            "com_unq": commentators_cnt,
        }
        print("finished")
        self._save_profile_result(username, stats_dict)
        return stats_dict

    def order_post_stats(self, link):
        """Возвращает статистику поста."""
        saved = self.get_post_results(link, order=False)
        if saved:
            return saved

        prefix = "https://www.instagram.com/p/"
        post_link = prefix + link
        # получаем списки смайлов и символов
        all_emoji_list = self._load_symbols_list(
            "app/helper_files/all_emoji_list"
        )
        positive_emoji_list = self._load_symbols_list(
            "app/helper_files/positive_emoji_list"
        )
        negative_emoji_list = self._load_symbols_list(
            "app/helper_files/negative_emoji_list"
        )
        permitted_nickname_symbols = self._load_symbols_list(
            "app/helper_files/nickname_symbols_list"
        )

        # получаем id поста
        posts = [Post(self._get_post_id_by_link(post_link), 0)]

        # получаем список всех комментов к посту
        comments = self._get_posts_comments(posts)
        # немного причесываем комменты
        self._filter_comments(
            comments, permitted_nickname_symbols, all_emoji_list
        )
        # вычисляем эмоциональный окрас комментов
        self._get_emotional_color_comments(
            comments, positive_emoji_list, negative_emoji_list
        )

        # число положительных, отрицательных и нейтральных комментов в профиле
        (
            pos_comms_cnt,
            neg_comms_cnt,
            neu_comms_cnt,
        ) = self._get_pos_neg_neu_comments_count(comments)

        # число различных комментаторов к посту
        commentators_cnt = self._get_commentators_count(comments)

        # заполняем итоговый словарь
        stats_dict = {
            "post_link": link,
            "com_pos": pos_comms_cnt,
            "com_neg": neg_comms_cnt,
            "com_neu": neu_comms_cnt,
            "com_unq_cnt": commentators_cnt,
        }

        self._save_post_result(link, stats_dict)

        return stats_dict

    def _store_post_result(self, post_link, stats_dict: dict):
        db = self._get_db()
        print(stats_dict)
        db.post.update_one(
            {"post_link": post_link}, {"$set": stats_dict}, upsert=True
        )

    def _store_profile_result(self, username, stats_dict: dict):
        db = self._get_db()
        db.profile.update_one(
            {"username": username}, {"$set": stats_dict}, upsert=True
        )

    def _save_post_result(self, post_link: str, stats_dict: dict):
        storing_thread = threading.Thread(
            target=self._store_post_result, args=(post_link, stats_dict,)
        )
        storing_thread.start()
        if len(self._post_cache) >= self._cache_size:
            self._post_cache.pop(list(self._post_cache.keys())[0])
        self._post_cache[post_link] = stats_dict

    def _save_profile_result(self, username: str, stats_dict: dict):
        storing_thread = threading.Thread(
            target=self._store_profile_result, args=(username, stats_dict,)
        )
        storing_thread.start()
        if len(self._profile_cache) >= self._cache_size:
            self._profile_cache.pop(list(self._profile_cache.keys())[0])
        self._profile_cache[username] = stats_dict

    def _get_stored_profile(self, username):
        db = self._get_db()
        stored = db.profile.find_one({"username": username})
        if stored:
            stored.pop("_id")
        return stored

    def _get_stored_post(self, post_link):
        db = self._get_db()
        stored = db.post.find_one({"post_link": post_link})
        if stored:
            stored.pop("_id")
        return stored

    def get_post_results(
            self,
            post_link: str,
            order: bool = True
    ):
        cached = self._post_cache.get(post_link)
        if cached:
            if post_link in self._ordered_posts:
                self._ordered_posts.remove(post_link)
            return cached
        stored = self._get_stored_post(post_link)
        if stored:
            if post_link in self._ordered_posts:
                self._ordered_posts.remove(post_link)
            self._save_post_result(post_link, stored)
            return stored
        else:
            if order and post_link not in self._ordered_posts:
                print(self._ordered_posts)
                self._ordered_posts.add(post_link)
                order_thread = threading.Thread(
                    target=self.order_post_stats, args=(post_link,)
                )
                # raise Exception(post_link)
                order_thread.start()
            return dict()

    def get_profile_results(
            self,
            username: str,
            from_date: str = None,
            to_date: str = None,
            order: bool = True
    ):
        cached = self._profile_cache.get(username)
        if cached:
            if username in self._ordered_profiles:
                self._ordered_profiles.remove(username)
            return cached
        stored = self._get_stored_profile(username)
        if stored:
            if username in self._ordered_profiles:
                self._ordered_profiles.remove(username)
            self._save_profile_result(username, stored)
            return stored
        else:
            if order and username not in self._ordered_profiles:
                self._ordered_profiles.add(username)
                order_thread = threading.Thread(
                    target=self.order_profile_stats, args=(username,)
                )
                order_thread.start()
            return dict()

    def _get_db(self) -> pymongo.collection.Collection:
        """Get MongoDB client.

        Args:
            config (dict): host, port, name

        Returns:
            pymongo.MongoClient: database client

        """
        from pymongo import MongoClient

        port = self._mongo_port
        client = MongoClient(self._mongo_host, port)
        database = client[self._mongo_db]

        return database


def test_profile_stats():
    """Test profile stats."""
    username = "msnesarev"
    analytics = InstAnalytics()
    stats = None
    while not stats:
        stats = analytics.get_profile_results(username)
        print('profile stats', stats)
        time.sleep(1)
    print(json.dumps(stats, indent=2))


def test_post_stats():
    """Test post stats."""
    post_link = "BdDdEqrFlPu"
    analytics = InstAnalytics()
    stats = None
    while not stats:
        stats = analytics.get_post_results(post_link)
        print('post stats', stats)
        time.sleep(1)
    print(json.dumps(stats, indent=2))


def test_profile_stats_cached():
    """Test profile stats."""
    username = "msnesarev"
    analytics = InstAnalytics()
    stats = analytics.get_profile_results(username)
    print(json.dumps(stats, indent=2))
    stats = analytics.get_profile_results(username)
    print(json.dumps(stats, indent=2))


def test_post_stats_cached():
    """Test post stats."""
    post_link = "BdDdEqrFlPu"
    analytics = InstAnalytics()
    stats = analytics.get_post_results(post_link)
    print(json.dumps(stats, indent=2))
    stats = analytics.get_post_results(post_link)
    print(json.dumps(stats, indent=2))


def _main():
    test_post_stats()
    test_post_stats_cached()
    test_profile_stats()
    test_profile_stats_cached()


if __name__ == "__main__":
    _main()
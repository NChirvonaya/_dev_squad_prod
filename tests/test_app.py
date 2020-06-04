"""App tests."""
import pytest
import json
from datetime import datetime

from app.analytics import InstAnalytics


with open("tests/testcases.json", "r") as cases:
    TEST_CASES = json.loads(cases.read())


@pytest.mark.parametrize("user", TEST_CASES["get_user_id"]["users"])
def test_get_user_id(user):
    """Тестирование получения id юзера."""
    analytics = InstAnalytics()

    assert bool(analytics._get_user_id(user[0])) == user[1], (
            "Test _test_get_user_id failed."
            f"Username: {user[0]}"
        )
    print(
        f"Test test_get_user_id succeeded. Username: {user[0]}"
    )


@pytest.mark.parametrize("post", TEST_CASES["order_post_stats"]["posts"])
def test_order_post_stats(post):
    """Тестирование получения статистики по посту.

    Тестируем только количество комментов и различных комментариев.
    """
    analytics = InstAnalytics()

    stats = analytics._order_post_stats(post[0])
    curr_comms_cnt = (
        stats["com_pos"] + stats["com_neg"] + stats["com_neu"]
    )
    curr_unique_commentators = stats["com_unq_cnt"]

    error_msg = f"Test _test_order_post_stats failed. Post ID: {post[0]}"
    assert curr_comms_cnt == int(post[1]) \
        or curr_unique_commentators == int(post[2]), error_msg
    print(
        f"Test _test_order_post_stats succeeded. Post ID: {post[0]}"
    )


@pytest.mark.parametrize(
    "media", TEST_CASES["get_profile_media_list"]["media_list"]
)
def test_get_profile_media_list(media):
    """Тестирование получения списка постов пользователя."""
    analytics = InstAnalytics()

    # ВАЖНО: если у пользователя появятся новые посты, тесты будут падать,
    # нужно будет обновлять
    # но так как уже протестили, не нужно обращать на них внимание

    username = list(media.keys())[0]
    media_ids = media[username]

    media = analytics._get_profile_media_list(username)

    fail = "failed"
    success = "succeeded"
    msg = "Test test_get_profile_media_list {}. Username: {}"

    assert len(media) >= len(media_ids), msg.format(fail, username)

    for media_rec in media:
        assert media_rec.media_id in media_ids, msg.format(fail, username)

    print(msg.format(success, username))


@pytest.mark.parametrize(
    "stats", TEST_CASES["order_profile_stats"]["stats"]
)
def test_order_profile_stats(stats):
    """Тестирование получения статистики профиля пользователя."""
    analytics = InstAnalytics()

    # ВАЖНО: если у пользователя появятся новые посты, тесты будут падать,
    # нужно будет обновлять
    # но так как уже протестили, не нужно обращать на них внимание

    query = (
        stats[0],
        datetime.strptime(stats[1], "%Y-%m-%d"),
        datetime.strptime(stats[2], "%Y-%m-%d"),
    )
    # ожидаемые результаты (число постов с комментами,
    # число постов без комментов, чисто комментов
    # , число уникальных комментаторов)
    true_result = stats[3]

    stats = analytics._order_profile_stats(query)

    msg = "Test test_order_profile_stats {}. Query: {} {} {}"
    failed = msg.format("failed", query[0], query[1], query[2])
    successed = msg.format("successed", query[0], query[1], query[2])

    assert stats["w_com"] == true_result[0], failed
    assert stats["wt_com"] == true_result[1], failed
    assert stats["com_all"] == true_result[2], failed
    assert stats["com_unq"] == true_result[3], failed

    print(successed)

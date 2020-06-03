import time
from datetime import datetime

from app.analytics import InstAnalytics, InstClient, Post, Comment

class UnitTests():
    
    # тестирование получения ID юзера
    def _test_get_user_id(self):
        
        analytics = InstAnalytics()
        
        # никнеймы юзеров и метки об их существовании (1 - если существует, -1 - если нет)
        users = [
            ['mr_justadog', '1']
            , ['maxinope', '1']
            , ['msnesarev', '1']
            , ['alenkokoroleva', '1']
            , ['_nastasjushka', '1']
            , ['k1pnis', '1']
            , ['dary.s', '1']
            , ['asafaeva', '1']
            , ['afafafafafaf_sss', '-1']
            , ['sidjsijsjisd', '-1']
        ]
        
        for i in range(len(users)):
            user_id = analytics._get_user_id(users[i][0])
            
            if ((user_id != -1 and users[i][1] == '-1') or (user_id == -1 and users[i][1] != '-1')):
                print("Test _test_get_user_id failed. Username: " + users[i][0])
            else:
                print("Test _test_get_user_id succeeded. Username: " + users[i][0])
        
    # тестирование получения статистики по посту (тестируем только количество комментов и различных комментариев)
    def _test_order_post_stats(self):
        
        analytics = InstAnalytics()
        
        # ID постов + реально количество комментариев к ним + реальное количество уникальных комментаторов
        posts = [
            ['B6UgdDUB4Cz', '3', '3']
            , ['CAVsDLrjdE_', '12', '11']
            , ['Bi0BBKgg_Bm', '13', '4']
            , ['CA5851tJlun', '13057', '11086']
            , ['CA5uPEKBeyJ', '208', '201']
            , ['Bzl-qBXBOv9', '8', '7']
            , ['CA0aM0GgEgK', '12', '8']
            , ['CAs4iYGjEpZ', '35', '19']
            , ['CA04B-Rh96v', '8', '8']
            , ['B8E0hA1lexe', '38', '34']
        ]
        
        for i in range(len(posts)):
            stats = analytics._order_post_stats(posts[i][0])
            curr_comms_cnt = stats['com_pos'] + stats['com_neg'] + stats['com_neu'];
            curr_unique_commentators = stats['com_unq_cnt']
            
            if (curr_comms_cnt != int(posts[i][1]) or curr_unique_commentators != int(posts[i][2])):
                print('Test _test_order_post_stats failed. Post ID: ' + posts[i][0])
            else:
                print('Test _test_order_post_stats succeeded. Post ID: ' + posts[i][0])
            
    # тестирование получения списка постов пользователя
    def test_get_profile_media_list(self):
        
        analytics = InstAnalytics()
        
        # ВАЖНО: если у пользователя появятся новые посты, тесты будут падать, нужно будет обновлять
        # но так как уже протестили, не нужно обращать на них внимание
        
        # список тестируемых юзеров
        usernames = ['torialexus', 'maxinope', 'testinstapp', 'kudriishow', 'tanya.kitt'
                     , 'safilm.35mm', 'kaylalaurenofficial', 'pashk_ch', 'rosso4400', 's.v.lucky']
        # ожидаемый список ID их постов
        media_ids = [
            ['CAqQeI2jnX8', 'CAdaobzDrDm', 'CAYYxfZDljJ', 'CAVsDLrjdE_', 'CATSzDmApzg'
             , 'CAOhz9-ALe9', 'CAEOq5kg8pb', 'CABgc8jDZ2C', 'B__HlQgjo4c', 'B_8WOsNDiIv'
             , 'B_541fEjmMJ', 'B_3PqwJDq7m', 'B_0QVONDPe3']
            , ['B1elEosIrm8', 'BysR59tD7mi', 'Bo1smwvjvK-', 'BnWSvUZDznW', 'BhkEaGwD1sm'
               , 'Bf6UdlgHuEt', 'Be0Y51Sn257', 'BWl90jbnR1Q', 'BQAwNhkFn0Y', 'BP0Ke0XllQ7'
               , 'BPr-ZynjP8i', 'BPoQduwD0Ao', 'BMw5FYEj0Rz', 'BLZt8x5jitL', 'BKMQXFADUUM']
            , ['B_KwrjOJyL3']
            , ['B__Bsf-HC9-', 'B-0kk1DDvjC', 'B-nUCXjDbTb', 'B-iaR9_DHv1', 'B-iX3JWD5Rx'
               , 'B-iD1O-j7Hm']
            , ['CAxOFT9nSQG', 'CAA_NVtHogc', 'B_MbbRYHVTH', 'B-7V3aEn4wc', 'B-2U8JFnPpn'
               , 'B-kI8jdHInq', 'B-VJxjUHlCn', 'B-NCTB1Haui', 'B992DDyHMst', 'B9PgawgHfNl'
               , 'B9HrbreHUeZ', 'B866wdBHLLQ', 'B84SpyKHwxW', 'B813tnlHyUc', 'B8wYUY1H9Ot'
               , 'B8R1ldVnHB3', 'B8D0G_AojiW', 'B76AnvRnBZi', 'B7vqGM8H1Yc', 'B7rOaLZHuOV'
               , 'B7mGvuMnLE4', 'B7b0TftHX3Z', 'B7RbqSEHRL0', 'B7MVvLunNyw', 'B7JwzZuHG9C'
               , 'B7EbMcFnhkP', 'B7B2VgjH8oO', 'B69AuU9nCmo', 'B66Yaf3nsuZ', 'B6vwKhrntl0'
               , 'B6tfNSlHNEY', 'B6qJBlInqYY', 'B6gmHv8HsUh', 'B6dqb-BnIke', 'B6S44xRHieq'
               , 'B6Slu_gnBTY', 'B6ObCMMnUxc', 'B6MGSyJHM0E', 'B6EDIyanh4g', 'B55GI2bnCz3'
               , 'B5s2hbNHgDo', 'B5qVyIOHz4F', 'B5lMyp-n-dO', 'B5VBgMaHlJC', 'B48LzJVHGUn'
               , 'B4wkAmVnsi5', 'B4nlGIqH0VZ', 'B4WsfJnnLGQ', 'B4S18TKHv_l', 'B4J_fqInCIk'
               , 'B3zOi2QHmW9', 'B3tlryCnGyW', 'B3mqmvfnvJp', 'B3eFBrwHmxn', 'B3b2xEMHLWf'
               , 'B3UGpv5H6Vy', 'B3PWaVFnCdn', 'B3K7fCcHdI_', 'B3FGSEkn0b6', 'B2_6TIRH1ox'
               , 'B244C4AltiB', 'B21DIBtHRGQ', 'B2hhYS4nOmN', 'B2Js9UHnXgZ', 'B2Hi3deHKda'
               , 'B2FEcOaHEql', 'B1-0_4nnBjs', 'B14hIn2HyC0', 'B13jGX0ngkm', 'B1q-d9JncLm'
               , 'B1oUGMAnf26', 'B1mVOo2HwMq', 'B1jSKYyHqNL', 'B1a9bcVnTTl', 'B1ToIWTHPxA'
               , 'B1L7p6FHr_C', 'B1HXcLJn_9Y', 'B0oHZBVnKWy', 'B0n7-_nHgfM', 'B0gyTnFHrG7'
               , 'B0Yk0AUHkUg', 'B0K7KSwnahA', 'B0F9IMiHD0i', 'Bzp6rgAnROL', 'BzlAI8dnxBJ'
               , 'BzSuQcungcr', 'BzIbZVpnnp0', 'BzEFmsZH-b4', 'BzBeUe5nrAR', 'BykTWNEn2oG'
               , 'Byf3ZRyHBhu', 'ByNaxvBn_vi', 'Bx_-LYznB7a', 'Bxx0pPNFuTb', 'BxXfiF_FdOF'
               , 'BxDMUq-luak', 'Bwwm_MKF5zA', 'BwsgNwslSxw', 'BwnTEJlFcSN', 'Bwaq_MOle2P'
               , 'BwVOqfJlVpD', 'BwCDDwzF1Yx', 'BwApHxzldOl', 'BvukibFFKDk', 'BvhzD-_l1yD'
               , 'BuTSX_XFzr_', 'BuPfnrQlkqp', 'Bt4CLXMFQhO', 'BtiwsOQl5gq', 'BtePx1SFJQb'
               , 'BtdEx5jlEWt', 'BsQYZeoF-Yo', 'Br-dl3eFP1U', 'BrxJolplNwQ', 'BrTCLhlFcu3'
               , 'BrS-3vdFbXH', 'BrS-Uc9FvFn', 'BrNNOGLF2U_', 'BrGONSWFFla', 'BrFUJQel6Xe'
               , 'Bq2qICnltA-', 'BqcZFwElila', 'BqFNFLFFTiv', 'BpMXfFmhgmw', 'BpIFA8FhIHx'
               , 'BpIC0CRhkki', 'Bozgk3ZB23G', 'BozYtRShpCq', 'BozX0gVhD_s', 'BoWak7OBLGH'
               , 'BoT0VSah_7f', 'BoSUsPLBp4V', 'BnCA2pPhp0Q', 'Bm6KoIdhEZX', 'Bm3hwhGBo_X'
               , 'BmyZ2g5heuv', 'BmQdTF_huFr', 'BkQicxBnq4l', 'BkKlq9JnjTz', 'BkFcklLHPRB'
               , 'BjwieYqnEX3', 'BjmrOg_H9KE', 'BjSdtG3H2td', 'BjIJjNLny-Y', 'BjEFe53Hksc'
               , 'Bi1XtBxnLLH', 'Bizg-3Mng_F', 'BisNE5PnAaW', 'BirHYtpHik6', 'BiZZ564n6_a'
               , 'BiWbzWRnPi_', 'BiR_9c4Hp0i', 'BiCtST4nYK1', 'Bh9mcScHz3B', 'BhwY-WrnLk_'
               , 'BhelO77n2nc', 'BhY-I2FH1q_', 'BhR_MwtnOwC', 'BhHq609FLPF', 'BgqaCtvlQrD'
               , 'BgoAWRXln_H', 'BgYdTe-Aiuu', 'Bf59cjFlHi8', 'Bf1g-gtF2B1', 'BfsoCFJFlCT'
               , 'BfeQDDVls0_', 'Bfabj3yl4CU', 'BfUO4CPlUbZ', 'BfIa-svFxXm', 'Be3Utbmlgl6'
               , 'Bei73vBl9Ni', 'BeEhoKlFxL7', 'Bd8L-YplCkp', 'BdxZ0CilUiq', 'BdmYQTylqPw'
               , 'BdDK_GhFIiW', 'BcnuEhnFtcJ', 'BclH9wHFoAn', 'Bbgtmtpl2p8', 'BbVgLFvFX1A'
               , 'BarhN15F0dC', 'BZPLx6JFkZU', 'BX-sVo8lTAZ', 'BX5GSI9lq7U', 'BXp2F6CFomA'
               , 'BW-CMg4FS0s', 'BWXfiiMlVud', 'BU9fIk0BDJo', 'BU3xhmJBlyC', 'BUZQ3sRA3RL'
               , 'BUDAZQJAxov', 'BT18ycRAByF', 'BTllk0Hh3N3', 'BS63ut6BNb2', 'BSlPP4QB0O6'
               , 'BSXJ9JOhGC1', 'BR0w34sBltr', 'BRwDbguhNCe', 'BRhkfSxBABt', 'BRhdFJdBN1F'
               , 'BRabmamBN0q', 'BP7pK0Mg7FS', 'BPYfzjtAb6V', 'BOu0MdbA8Hp', 'BOAwEH3hWmj'
               , 'BNxv51oA_dI', 'BMWGQR7AyxV', 'BLqrXUdg3BO', 'BKH1zwOgqLW', 'BJ7r4w3B8GS'
               , 'BJ3SILrhBlh', 'BIFPA_iBc65', 'BH-u-vjhB9F', 'BH-cLTChpan', 'BH0L27Aggi8'
               , 'BHiWg3-BZgR', 'BHaSH6JhE57', 'BHK8gvcBmRd', 'BGM8bl0wTXa', 'BEhNY53wTSi'
               , 'BEHIr6dQTTZ', 'BCPaQUlwTfb', 'BB3NNYhwTS2', 'BBI3dy9wTT-', '8XzzqIwTTP'
               , '7Kzg-3QTd8', '6a2ILsQTTr', '55UtinQTSU', '5yzQQFwTVQ', '48_CR1QTa9'
               , '4kQeevwTfz', '4O1aIJQTXT', '4FikUbQTT6', '3j6tI1wTdW', '3E6SfQwTcI'
               , '2_ygRkwTT3', '29FVnQwTaJ', '2yyGQ2QTZt', '2tXxTYwTeu']
            , ['B036ZBNqCcq', 'B0k9NapijqI', 'B0dCLXfCLCd', 'B0Vfc0Gi7ac', 'B0SuK33iEWu']
            , ['CA78IjejkZH', 'CA1o1x-DQyS', 'CAvMzTDDnn9', 'CAs8B5tjxFG', 'CAqYFuojlS5'
               , 'CAgFxqxjldv', 'CAa9QJwjXQJ', 'CAYW5AejDWY', 'CAV9utjD4Rp', 'CATNdbxjPfg'
               , 'CAN9RGOjHyF', 'CAI8WOfjHpg', 'CAGTt-hncZb', 'B_8EqeDj0F2', 'B_5fXpyD01_'
               , 'B_xpCAAj_8y', 'B_vQd8ZjMdt', 'B_sXn0fjCpb', 'B_VsB3RjgJU', 'B_NrTs5jrdS'
               , 'B_GDOreDbMV', 'B_DdPk5DpsM', 'B-xRZslj37w', 'B-u3JaJD3DT', 'B-sPCL3jjS8'
               , 'B-pljzrDtwE', 'B-khvtSDRT5', 'B-fYAO6jrjK', 'B-dOQ4DjhHU', 'B-Xm7NUDA5T'
               , 'B-QPqEpD50D', 'B-KpIQojKsO', 'B-FjLkljFv7', 'B97M8qsjTpQ', 'B94t4CrjUBW'
               , 'B9zhQK_DLPV', 'B9r6hM3DTaO', 'B9pRe1ynuNQ', 'B9hinEXDkgi', 'B9Uw2xJDOnN'
               , 'B9SMAIMjRYM', 'B9H4fDGjoCg', 'B9AKsz0jotO', 'B84cFaQjQ17', 'B8wnNkSD_Nc'
               , 'B8uP6YfjgSu', 'B8ewEKkjOgh', 'B8ZkVhUD8Tg', 'B8R6dOYjJzN', 'B8POcVBjx12'
               , 'B8MmTPnjciO', 'B7wcIKAjie4', 'B7uCknTDuW1', 'B7rMWcwjQC0', 'B7opLE8D2kf'
               , 'B7mG1cVjE15', 'B7jdxPvDG-L', 'B7UCz6Mj4dp', 'B7RUuUmjyE8', 'B7JprFIDAOI'
               , 'B7CAiCNj0U5', 'B6tc1NHjXJ5', 'B6jGwIMj57R', 'B6Yt9cyDltu', 'B6WUuX6D8Fv'
               , 'B6TvClHjncE', 'B6MCv8kj6pY', 'B6JTKczDtXy', 'B6BpP-ZDlmp', 'B58fD1djja4'
               , 'B558eWUja6z', 'B53SwGkjrqO', 'B5yNh49jRWK', 'B5n3UpOjrlS', 'B5TXimTjgrq'
               , 'B5GW7-CD3y6', 'B45jAmfjiKB', 'B40a3lzjcCF', 'B4nl1iMDCTy', 'B4k51AnjnrS'
               , 'B4f-3qSj8db', 'B3nDd5djWpa', 'B2w8ZdLjeEM', 'B2PeAiJDQbU', 'B2FLU5xj2h-'
               , 'B165h6YDpTZ', 'B1ZcJidDd4a', 'B1W1xmPj-Ay', 'B01azlKDnJb', 'B0l3RSRD1km'
               , 'B0MLWLyDxiz', 'B0EbR7Vjnmm', 'Bz_RfxAjeac', 'Bz8s75DjXyb', 'Bz1A_10Daec'
               , 'BztP860DZS9', 'BzlnPQsDoO-', 'Bzi618QjG_H', 'BzJHDNAj0GJ', 'BzEDgL7jOp5'
               , 'BzBe_ecDUm4', 'By5ybIIj6zu', 'Bynos5Zjzkn', 'ByYAoW_jguR', 'ByTMvcOjLnY'
               , 'ByN1uusDPG-', 'ByIt9QXjOAV', 'ByDjvlPD9UB', 'Bx-c2EhjaYB', 'Bx7zbRlDMlA'
               , 'Bx5Eopcjv7Q', 'Bxu9BSjjXX3', 'BxnKVeEj_gF', 'BxiPz70lQqg', 'BxaO75VHE2E'
               , 'BxSnjhBH9Mt', 'BxMCGMBnSZG', 'BxGIla5nyO7', 'BwxLcvtHtDG', 'BwpjWekHJeG'
               , 'Bwh8yPiH05N', 'BwcucdkHUyM', 'BwXzgYhHc61', 'BwVdqsyHGt7', 'BwNMDo-n6-5'
               , 'BwKthL-HdF5', 'BwAR53TBQt1', 'Bv7adpDhnFa', 'BvxLeYVnT9f', 'Bvm6zOrhnMo'
               , 'BvfD0QGh56q', 'BvcLgBVhjqE', 'BvPWfr-hui0', 'BvHoasrBbb4', 'BvFBYBLBDJN'
               , 'Bu6uEuhBRSN', 'BuuIYIHBq8n', 'Burn1IYhJX5', 'Buj31MtBtWZ', 'BuXV1P-BqTh'
               , 'BuPF9N7hhIH', 'BuMUIocBcg4', 'Bt_t-h4BSpB', 'Bt9OjWkBNYw', 'Bt3_ZecBuW-'
               , 'BtjR7i-hLGt', 'BteP8KEBN5t', 'BtWjrHBBvN5', 'BtO2QcHhm3b', 'Bs_ZxaFBcot'
               , 'Bs8jshGBtpd', 'Bs1Nz7LBZWx', 'BsoZfOjhwIH', 'BsipIAPh9lk', 'Bsd0UD6hhg-'
               , 'BsOal-QhVJS', 'BsD_SEVh9o8', 'BrYb4mSh5Kn', 'BrI7bWkhiy8', 'Bq-s2voh-61'
               , 'Bq8F1jkBya2', 'Bq0X3GsBknR', 'BqyItWSBYn_', 'BqalGBABUnE', 'BqQJVdyhuAF'
               , 'BqF_q3cBtLJ', 'Bp5Ddx_BtW1', 'Bp2YIQGhgYq', 'Bpki8KmHJRA', 'BpcsEjNnWfS'
               , 'BpXZL_gHgwb', 'BpPzmspnxx-', 'Boewc9hHuzd', 'Bny8k3YnrR3', 'Bnwb9ISnvuC'
               , 'Bnrz482hI7M', 'BnZRU_ZnL4M', 'BnUOgdynfHX', 'BnRnhNoHzmW', 'BnMzyNPn4LV'
               , 'BnEoF4An7uw', 'Bm_u44_He3S', 'Bm4Ynb5H6mr', 'Bm1ZqMKH86Q', 'BmobXWGHX2P'
               , 'BlwPoaWn22i', 'BlrSkG8n3tz', 'BleOyNFnb4Y', 'BlJBsiMnE7g', 'BlEDAv0HZr4'
               , 'BlBWNKxHQEu', 'Bk-x1kpnRfo', 'Bk5gkG_n91V', 'BkyKG6NnWjp', 'BkSxwjpns8J'
               , 'BihnOGVnuh2', 'BhFUXmWgGtA', 'BfqtDIDg-HH', 'BeyNca4Ap9C', 'Bei9TPqge2r'
               , 'BedwbalgXyM', 'BeUF8OqAf59', 'BeOiW70A6Xr', 'BeOVcYBAXZO', 'Bd_LJFyAEBN'
               , 'Bbxzs2ijeOy', 'BbLNLHkh4xJ', 'BbH_Ld7BtCI', 'Ba-JaLGBdoT', 'Ba2NnT1B1UD'
               , 'BapvkDBDOMa', 'Bac2RNTAOvn', 'BaKpgDpAjbf', 'BZrJ7QdAZ10', 'BZpJXyNA7cs'
               , 'BZfEexGgDZZ', 'BZKCpqXARg6', 'BYUIulagEjy', 'BX1Xk9wA1-U', 'BXwZkfwAYWi'
               , 'BXl6Jh7gsN0', 'BXT7EqfALM0', 'BXO2-s_AScu', 'BWnvRbAAdGM', 'BWdVD7IAP-Y'
               , 'BWTVO_vgP7g', 'BWQTWFIAOnP', 'BWD8yoDAJBI', 'BV3OlYmAq9A', 'BVnrzTcBHzv'
               , 'BVc7RZxAfNh', 'BVVzJ06gE8b', 'BVN-TTYA3E4', 'BVDs326AACY', 'BUiQFUXgeF8'
               , 'BUfrjCDgKZS', 'BUNpaPAAzRZ', 'BT2e_i4gzTi', 'BTw7McAAVTI', 'BTXnJGEgaQL'
               , 'BTAaOxcgkkK', 'BSxNRdKAX43', 'BSuaNNmgO_s', 'BShkF4Kg3lX', 'BSPeHTnAr7J'
               , 'BSIaHWvAiN7', 'BSCrCqVgE3G', 'BR4ap9UAxwU', 'BRynXo2gaCZ', 'BRem0BUATAa'
               , 'BRb_pHKAQky', 'BRWPxo6gUju', 'BRG4fPTgv9V', 'BREcQLDgtIB', 'BQ_n80vAaKe'
               , 'BQD5JvilT-o', 'BP25RXMl0lh', 'BPyWB2Rl6yy', 'BPg6o9gFw2B', 'BOy3VKDFqLR'
               , 'BOqq93ylwb4', 'BOk5sG9hCjO', 'BOa11z4h4Vc', 'BN5YfLcBCfv', 'BN0WA7xhhSh'
               , 'BNcuAh6BpXb', 'BNctnU6hAHW', 'BNSSFP0BIlU', 'BM9u3qPBGOd', 'BMBqwVmhEVI'
               , 'BKzeURCBjL4', 'BKovA7IBOdg', 'BKXBBP5BBOv', 'BKKSUHHh217', 'BJ_K_h6BeXY'
               , 'BJ4EVWUh4JU', 'BJCm4rdBaXY', 'BHckfX5hR6s', 'BHL7ztQB5Po', 'BHLPdE5BQXt'
               , 'BHK3BBeBA6w', 'BHJgh2zBmGE', 'BHGY3L-BHTv', 'BG0IxVlzQYi', 'BGk27OnzQVs'
               , 'BGeveRWTQep', 'BGczhc9zQRu', 'BGYCl7tzQT1', 'BGUbfwTTQQ5', 'BGSS9nuTQTT'
               , 'BGQYlJ8zQcn', 'BGQT3iczQR6', 'BGAX5jezQRF', 'BF5UxTVzQVO', 'BFu_tWVzQau'
               , 'BFp5hh_TQXy', 'BFm_UO9TQaZ', 'BFmmPOETQYX', 'BFWm1uCTQVG', 'BFP5dsLTQf4'
               , 'BFLC8kszQUL', 'BFKs2hGTQe0', 'BFIImsRzQe1', 'BE9J2s3zQSQ', 'BEwUnByzQQE'
               , 'BECjjMLTQXg', 'BD9iUk7TQel', 'BDs7cFTzQaM', 'BDd0QjfTQdn', 'BC6IjxYTQWJ'
               , 'BCTcqZazQaC', 'BCOQXc_TQdy', 'BCN1FtmzQXE', 'BB8L3p5TQRI', 'BBA4mlgzQVy'
               , 'BA-IyJBTQaH', '_pkd5bTQf2', '5XqBHczQT2']
            , ['B9E43-rHIza', 'B8G_BWZHk2T', 'BzVgfrfH_As', 'BzA-J49HTO3', 'ByvaRnin0A0'
               , 'Bvb1vdPnW2S', 'BujoI8lnRvK', 'BuEpzKIgFEy']
            , ['BhTaS8Glwap']
            , ['BUYyhf3F139', 'BUPpwOllvTb', 'BJLzSoiBcUS', 'xugnBJKDpv', 'xpovGKqDs8']
        ]
        
        for i in range(len(usernames)):
            media = analytics._get_profile_media_list(usernames[i])
            correct = True
            if (len(media) != len(media_ids[i])):
                correct = False
            else:
                for j in range(len(media)):
                    if (media_ids[i][j] != media[j].media_id):
                        currect = False
                    break
            
            if (correct == False):
                print('Test test_get_profile_media_list failed. Username: ' + usernames[i])
            else:
                print('Test test_get_profile_media_list succeeded. Username: ' + usernames[i])
                
    # тестирование получения статистики профиля пользователя
    def _test_order_profile_stats(self):
        
        analytics = InstAnalytics()
        
        # ВАЖНО: если у пользователя появятся новые посты, тесты будут падать, нужно будет обновлять
        # но так как уже протестили, не нужно обращать на них внимание
        
        # никнеймы юзеров + даты для сбора статистики
        queries = [
            ('torialexus', datetime.strptime('2000-01-01', '%Y-%m-%d'), datetime.strptime('2020-06-02', '%Y-%m-%d'))
            , ('thehannamae', datetime.strptime('2000-01-01', '%Y-%m-%d'), datetime.strptime('2020-06-02', '%Y-%m-%d'))
            , ('kayla_james_draws', datetime.strptime('2000-01-01', '%Y-%m-%d'), datetime.strptime('2020-06-02', '%Y-%m-%d'))
            , ('zoe_saintval', datetime.strptime('2000-01-01', '%Y-%m-%d'), datetime.strptime('2020-06-02', '%Y-%m-%d'))
            , ('wickswalker', datetime.strptime('2000-01-01', '%Y-%m-%d'), datetime.strptime('2020-06-02', '%Y-%m-%d'))
            , ('wickswalker', datetime.strptime('2020-05-01', '%Y-%m-%d'), datetime.strptime('2020-05-31', '%Y-%m-%d'))
            , ('kayla_james_draws', datetime.strptime('2020-05-01', '%Y-%m-%d'), datetime.strptime('2020-05-31', '%Y-%m-%d'))
            , ('torialexus', datetime.strptime('2020-05-01', '%Y-%m-%d'), datetime.strptime('2020-05-31', '%Y-%m-%d'))
            , ('thehannamae', datetime.strptime('2020-05-01', '%Y-%m-%d'), datetime.strptime('2020-05-31', '%Y-%m-%d'))
            , ('zoe_saintval', datetime.strptime('2020-05-01', '%Y-%m-%d'), datetime.strptime('2020-05-31', '%Y-%m-%d'))
        ]
        # ожидаемые результаты (число постов с комментами, число постов без комментов, чисто комментов
        # , число уникальных комментаторов)
        true_results = [
            [13, 1, 196, 70]
            , [18, 0, 951, 461]
            , [17, 4, 84, 30]
            , [28, 3, 525, 137]
            , [74, 7, 445, 296]
            , [3, 78, 3, 3]
            , [7, 14, 34, 13]
            , [13, 1, 196, 70]
            , [13, 5, 63, 50]
            , [4, 27, 109, 43]
        ]
        
        for i in range(len(queries)):
            stats = analytics._order_profile_stats(queries[i])
            correct = True
            if (stats['w_com'] != true_results[i][0]):
                correct = False
            if (stats['wt_com'] != true_results[i][1]):
                correct = False
            if (stats['com_all'] != true_results[i][2]):
                correct = False
            if (stats['com_unq'] != true_results[i][3]):
                correct = False
            
            if (correct == False):
                print('Test _test_order_profile_stats failed. Query: '
                      + queries[i][0] + ' ' + str(queries[i][1]) + ' ' + str(queries[i][2]))
            else:
                print('Test _test_order_profile_stats succeeded. Query: '
                      + queries[i][0] + ' ' + str(queries[i][1]) + ' ' + str(queries[i][2]))

test = UnitTests()
test._test_get_user_id()
test._test_order_post_stats()
test.test_get_profile_media_list()
test._test_order_profile_stats()
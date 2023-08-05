import pytest
from cutlet import Cutlet


# Note that if there are multiple words, only the first is used
WORDS = [
        ('新橋', 'shinbashi'),
        ('学校', 'gakkou'),
        ('パンダ', 'panda'),
        # without curry, カツ is registered as 人名 (?)
        ('カツカレー', 'cutlet'),
        ('カレー', 'curry'),
        ('繊維', "sen'i"),
        ('専用', "sen'you"),
        ('抹茶', 'matcha'),
        ('重量', 'juuryou'),
        ('ポール', 'Paul'),
        ('ジル', 'jiru'), # test of ジル-外国 style lemmas
        ('1', '1'),
        ]

WORDS_KUNREI = [
        ('新橋', 'sinbasi'),
        ('学校', 'gakkou'),
        ('パンダ', 'panda'),
        # without curry, カツ is registered as 人名
        ('カツカレー', 'cutlet'),
        ('カレー', 'curry'),
        ('繊維', "sen'i"),
        ('専用', "sen'you"),
        ('抹茶', 'mattya'),
        ('重量', 'zyuuryou'),
        ('ポール', 'Paul'),
        ('1', '1'),
        ]

SENTENCES = [
        ("あっ", "A"),
        ("括弧は「こう」でなくちゃ", "Kakko wa \"kou\" de nakucha"),
        ("富士見坂", "Fujimi saka"),
        ("本を読みました。", "Hon wo yomimashita."),
        ("新橋行きの電車に乗った。", "Shinbashiiki no densha ni notta."),
        ("カツカレーは美味しい", "Cutlet curry wa oishii"),
        ("酵素とは、生体で起こる化学反応に対して触媒として機能する分子である。", 
            "Kouso to wa, seitai de okoru kagaku hannou ni taishite shokubai to shite kinou suru bunshi de aru."),
        ("ホッピーは元祖ビアテイスト清涼飲料水です",
            "Hoppy wa ganso beer taste seiryou inryousui desu"),
        ("東京タワーの高さは333mです",
            "Tokyo tower no takasa wa 333 m desu"),
        ("国立国語研究所（NINJAL）は，日本語学・言語学・日本語教育研究を中心とした研究機関です。",
            "Kokuritsu kokugo kenkyuusho (NINJAL) wa, Nippon gogaku/gengogaku/Nippon go kyouiku kenkyuu wo chuushin to shita kenkyuu kikan desu."),
        ("やっちゃった！", "Yacchatta!"),
        ("暖かかった", "Atatakakatta"),
        ("私はテストです", "Watakushi wa test desu"), # issue #4, 私 -> 代名詞
        ("《月》", "(gatsu)"), # issue #7, unfamiliar punctuation
        ("２ 【電子版特典付】", "2 [denshi ban tokutentsuke]"), # issue #7
        # This looks weird but MeCab tokenizes at alpha-num barriers
        ("ｃｕｔｌｅｔ２３", "Cutlet 23"),
        # Test some kana unks - issue #8
        ("アマガミ Sincerely Your S シンシアリーユアーズ", 
            "Amagami Sincerely Your S shinshiariiyuaazu"),
        ("ケメコデラックス", "Kemekoderakkusu"),
        ("プププランド", "Pupupurando"),
        # Add some non-Japanese tests
        ("панда", "?????"),
        ("팬더", "??"),
        ("「彁」は幽霊文字のひとつ", '"?" wa yuurei moji no hitotsu'),
        # Do half-width katakana
        ("ﾎﾟｰﾙ", "Paul"),
        ("ｳｽｲﾎﾝ", "Usuihon"),
        # Test adjective + desu
        ("赤いです", "Akai desu"),
        ("美味しいです", "Oishii desu"),
        # Test repeated 長音符
        ("プラトーーーン", "Puratoo--n"),
        # Ainu kana
        ("イタㇰ", "Itak"),
        # Whatever this is
        ("エィッリィククワッドゥロッウ", "Irrikukuwadduro-u"),
        # small か
        ("夕陽ヵ丘三号館", "Yuuhi kakyuu san goukan"),
        # deal with combining dakuten
        ("青い春よさらば！", "Aoi haru yo saraba!"),
        # small ケ
        ("齋藤タヶオ", "Saitou ta ke o"),
        # っー
        ("ずっーと", "Zu--to"),
        # don't add spaces around apostrophe if it wasn't there
        ("McDonald's", "McDonald's"),
        ("Text McDonald's text", "Text McDonald's text"),
        # Following are quote weirdness. Not good but hard to fix.
        # An issue is that ," or .' is a single token.
        ("It's 'delicious.'", "It's ' delicious .'"),
        ('"Hello," he said.', '" Hello ," he said.'),
        ]

SENTENCES_KUNREI = [
        ("富士見坂", "Huzimi saka"),
        ]

SLUGS = [
        ("東京タワーの高さは？", "tokyo-tower-no-takasa-wa"),
        ("ゲームマーケットとは", "game-market-to-wa"),
        ("香川ゲーム条例、「（パブコメは）賛成多数だから採決しては」と発言したのは誰だったのか", 
            "kagawa-game-jourei-pabukome-wa-sansei-tasuu-dakara-saiketsu-shite-wa-to-hatsugen-shita-no-wa-dare-datta-no-ka"),
        ("コトヤマ「よふかしのうた」3巻発売記念のPV公開、期間限定で1巻の無料配信も", 
            "koto-yama-yo-fukashi-no-uta-3-maki-hatsubai-kinen-no-pv-koukai-kikan-gentei-de-1-maki-no-muryou-haishin-mo"),
        # Include some unks
        ("彁は幽霊文字", "wa-yuurei-moji"),
        ("パンダはロシア語でпанда", "panda-wa-rossiya-go-de"),
        ]

NON_FOREIGN = [
        ("カツカレーは美味しい", "Katsu karee wa oishii"),
        ]

TITLE = [
        ('吾輩は猫である', 'Wagahai wa Neko de Aru'),
        ('お話があります', 'Ohanashi ga Arimasu'),
        ('図書館戦争', 'Toshokan Sensou'),
        ('頑張って', 'Ganbatte'),
        ('さらば愛しき人よ', 'Saraba Itoshiki Hito yo'),
        ('愛せよ乙女', 'Aiseyo Otome'),
        ('巴里は燃えているか', 'Paris wa Moete Iru ka'),
        ]


import pathlib
here = pathlib.Path(__file__).parent.absolute()
import json
with open(here / 'blns.json') as infile:
    NAUGHTY = json.load(infile)

@pytest.mark.parametrize('ja, roma', WORDS)
def test_words(ja, roma):
    cut = Cutlet()
    word = cut.tagger.parseToNodeList(ja)[0]
    assert cut.romaji_word(word) == roma

@pytest.mark.parametrize('ja, roma', WORDS_KUNREI)
def test_words_kunrei(ja, roma):
    cut = Cutlet('kunrei')
    word = cut.tagger.parseToNodeList(ja)[0]
    assert cut.romaji_word(word) == roma

@pytest.mark.parametrize('ja, roma', SENTENCES)
def test_romaji(ja, roma):
    cut = Cutlet()
    assert cut.romaji(ja) == roma

@pytest.mark.parametrize('ja, roma', SENTENCES_KUNREI)
def test_romaji_kunrei(ja, roma):
    cut = Cutlet('kunrei')
    assert cut.romaji(ja) == roma

@pytest.mark.parametrize('ja, roma', SLUGS)
def test_romaji_slugs(ja, roma):
    cut = Cutlet()
    assert cut.slug(ja) == roma

@pytest.mark.parametrize('ja, roma', NON_FOREIGN)
def test_romaji_non_foreign(ja, roma):
    cut = Cutlet()
    cut.use_foreign_spelling = False
    assert cut.romaji(ja) == roma

@pytest.mark.parametrize('ja, roma', TITLE)
def test_romaji_title(ja, roma):
    cut = Cutlet()
    assert cut.romaji(ja, title=True) == roma

@pytest.mark.parametrize('ja, roma', [
    (None, ''),
    ('', '')
])
def test_empty_string(ja, roma):
    cut = Cutlet()
    assert cut.romaji(ja) == roma

@pytest.mark.parametrize('text', NAUGHTY)
def test_naughty(text):
    # Goal here is just to not have an exception
    cut = Cutlet()
    cut.romaji(text)

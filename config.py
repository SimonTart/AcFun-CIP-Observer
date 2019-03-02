import os

contentTypes = {
    'article': 'article',
    'video': 'video'
}

ARTICLE_SECTIONS = [
    {
        'name': '综合',
        'channelId': 110,
        'realmIds': '5,22,3,4',
    }, {
        'name': '工作·情感',
        'channelId': 73,
        'realmIds': '25,34,7,6,17,1,2',
    }, {
        'name': '涂图话画',
        'channelId': 184,
        'realmIds': '18,14,39',
    },
    {
        'name': '动漫文化',
        'channelId': 74,
        'realmIds': '13,31',
    },
    {
        'name': '漫画·轻小说',
        'channelId': 75,
        'realmIds': '15,23,16',
    },
    {
        'name': '游戏',
        'channelId': 164,
        'realmIds': '8,11',
    }
]

VIDEO_SECTIONS = [
    {
        "name": "AC正义",
        "channelId": 177,
        "subSections": [
            {
                "name": "AC正义展览区",
                "channelId": 178
            }
        ]
    },
    {
        "name": "番剧",
        "channelId": 155,
        "subSections": [
            {
                "name": "TV动画",
                "channelId": 67
            },
            {
                "name": "剧场动画",
                "channelId": 180
            },
            {
                "name": "国产动画",
                "channelId": 120
            }
        ]
    },
    {
        "name": "动画",
        "channelId": 1,
        "subSections": [
            {
                "name": "动画综合",
                "channelId": 106
            },
            {
                "name": "短片动画",
                "channelId": 190
            },
            {
                "name": "MAD·AMV",
                "channelId": 107
            },
            {
                "name": "MMD·3D",
                "channelId": 108
            },
            {
                "name": "动画资讯",
                "channelId": 159
            },
            {
                "name": "COSPLAY·声优",
                "channelId": 133
            },
            {
                "name": "布袋·特摄",
                "channelId": 99
            }
        ]
    },
    {
        "name": "音乐",
        "channelId": 58,
        "subSections": [
            {
                "name": "原创·翻唱",
                "channelId": 136
            },
            {
                "name": "演奏·乐器",
                "channelId": 137
            },
            {
                "name": "Vocaloid",
                "channelId": 103
            },
            {
                "name": "综合音乐·现场",
                "channelId": 139
            },
            {
                "name": "音乐选集",
                "channelId": 185
            }
        ]
    },
    {
        "name": "舞蹈·偶像",
        "channelId": 123,
        "subSections": [
            {
                "name": "宅舞",
                "channelId": 134
            },
            {
                "name": "综合舞蹈",
                "channelId": 135
            },
            {
                "name": "偶像",
                "channelId": 129
            },
            {
                "name": "造型·手作",
                "channelId": 127
            }
        ]
    },
    {
        "name": "游戏",
        "channelId": 59,
        "subSections": [
            {
                "name": "主机单机",
                "channelId": 84
            },
            {
                "name": "网络游戏",
                "channelId": 186
            },
            {
                "name": "电子竞技",
                "channelId": 145
            },
            {
                "name": "英雄联盟",
                "channelId": 85
            },
            {
                "name": "手机游戏",
                "channelId": 187
            },
            {
                "name": "桌游卡牌",
                "channelId": 165
            },
            {
                "name": "Mugen",
                "channelId": 72
            }
        ]
    },
    {
        "name": "娱乐",
        "channelId": 60,
        "subSections": [
            {
                "name": "生活娱乐",
                "channelId": 86
            },
            {
                "name": "鬼畜调教",
                "channelId": 87
            },
            {
                "name": "萌宠",
                "channelId": 88
            },
            {
                "name": "美食",
                "channelId": 89
            },
            {
                "name": "娱乐圈",
                "channelId": 188
            }
        ]
    },
    {
        "name": "科技",
        "channelId": 70,
        "subSections": [
            {
                "name": "科技制造",
                "channelId": 90
            },
            {
                "name": "人文科普",
                "channelId": 189
            },
            {
                "name": "汽车",
                "channelId": 122
            },
            {
                "name": "数码",
                "channelId": 91
            },
            {
                "name": "演讲·公开课",
                "channelId": 151
            },
            {
                "name": "广告",
                "channelId": 149
            }
        ]
    },
    {
        "name": "影视",
        "channelId": 68,
        "subSections": [
            {
                "name": "预告·花絮",
                "channelId": 192
            },
            {
                "name": "电影杂谈",
                "channelId": 193
            },
            {
                "name": "剧透社",
                "channelId": 194
            },
            {
                "name": "综艺Show",
                "channelId": 195
            },
            {
                "name": "纪实·短片",
                "channelId": 196
            },
            {
                "name": "特色片场",
                "channelId": 197
            }
        ]
    },
    {
        "name": "体育",
        "channelId": 69,
        "subSections": [
            {
                "name": "综合体育",
                "channelId": 152
            },
            {
                "name": "足球",
                "channelId": 94
            },
            {
                "name": "篮球",
                "channelId": 95
            },
            {
                "name": "搏击健身",
                "channelId": 153
            },
            {
                "name": "极限竞速",
                "channelId": 93
            }
        ]
    },
    {
        "name": "鱼塘",
        "channelId": 125,
        "subSections": [
            {
                "name": "普法安全",
                "channelId": 183
            },
            {
                "name": "国防军事",
                "channelId": 92
            },
            {
                "name": "历史",
                "channelId": 131
            },
            {
                "name": "新鲜事·正能量",
                "channelId": 132
            }
        ]
    }
]

if os.getenv('PYTHON_ENV', 'development') == 'production':
    db = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSPORT'),
        'database': os.getenv('DB_NAME')
    }
else:
    db = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'eva_acfun_dev'
    }

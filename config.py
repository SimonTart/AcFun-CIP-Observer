import os

contentTypes = {
  'article': 'article',
  'video': 'video'
}

ARTICLE_SECTIONS = ({
  'name': '综合',
  'channelId': 110,
  'realmIds': '5,1,2,4',
},{
  'name': '工作·情感',
  'channelId': 73,
  'realmIds': '6,7',
},{
  'name': '动漫文化',
  'channelId': 74,
  'realmIds': '13,14',
},
{
  'name': '漫画·轻小说',
  'channelId': 75,
  'realmIds': '15,16',
},
{
  'name': '游戏',
  'channelId': 164,
  'realmIds': '8,10,11,9,12',
})

VIDEO_SECTIONS = [
    {
        "name": "AC正义",
        "channelId": 178
    },
    {
        "name": "动画",
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
                "name": "短片动画",
                "channelId": 181
            }
        ]
    },
    {
        "name": "二次元",
        "channelId": 1,
        "subSections": [
            {
                "name": "短片·手书",
                "channelId": 106
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
        "name": "国产",
        "channelId": 179,
        "subSections": [
            {
                "name": "国产动画",
                "channelId": 120
            },
            {
                "name": "资讯·延伸",
                "channelId": 182
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
                "name": "演奏",
                "channelId": 137
            },
            {
                "name": "Vocaloid",
                "channelId": 103
            },
            {
                "name": "日系音乐",
                "channelId": 138
            },
            {
                "name": "综合音乐",
                "channelId": 139
            },
            {
                "name": "演唱会",
                "channelId": 140
            }
        ]
    },
    {
        "name": "舞蹈·彼女",
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
                "name": "爱豆",
                "channelId": 129
            },
            {
                "name": "手作",
                "channelId": 130
            },
            {
                "name": "造型",
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
                "name": "游戏集锦",
                "channelId": 83
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
                "name": "守望先锋",
                "channelId": 170
            },
            {
                "name": "桌游卡牌",
                "channelId": 165
            },
            {
                "name": "Mugen",
                "channelId": 72
            },
            {
                "name": "游戏中心",
                "channelId": 0
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
            }
        ]
    },
    {
        "name": "科技",
        "channelId": 70,
        "subSections": [
            {
                "name": "科学技术",
                "channelId": 90
            },
            {
                "name": "教程",
                "channelId": 151
            },
            {
                "name": "数码",
                "channelId": 91
            },
            {
                "name": "汽车",
                "channelId": 122
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
                "name": "国产剧",
                "channelId": 141
            },
            {
                "name": "网络剧",
                "channelId": 121
            },
            {
                "name": "纪录片",
                "channelId": 100
            },
            {
                "name": "综艺",
                "channelId": 98
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
                "name": "搏击",
                "channelId": 153
            },
            {
                "name": "11区体育",
                "channelId": 154
            },
            {
                "name": "惊奇体育",
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
    },
    {
        "name": "文章",
        "channelId": 63,
        "subSections": [
            {
                "name": "游记·涂鸦",
                "channelId": 184
            },
            {
                "name": "综合",
                "channelId": 110
            },
            {
                "name": "工作·情感",
                "channelId": 73
            },
            {
                "name": "动漫文化",
                "channelId": 74
            },
            {
                "name": "漫画·文学",
                "channelId": 75
            },
            {
                "name": "游戏",
                "channelId": 164
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
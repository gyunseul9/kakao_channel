# -*- coding: utf-8 -*- 

import re
import os
import sys
import time
import json
import requests
import datetime
from ast import literal_eval
from config import Configuration
from db import DBConnection,Query
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def db_access():
    configuration = Configuration.get_configuration('aws')
    _host = configuration['host']
    _user = configuration['user']
    _password = configuration['password']
    _database = configuration['database']
    _port = configuration['port']
    _charset = configuration['charset']

    conn = DBConnection(host=_host,
            user=_user,
            password=_password,
            database=_database,
            port=_port,
            charset=_charset)
    return conn

def get_fishing():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "서비스가 원할하지 않아, 사이트 링크로 대체합니다. 이점 양해 부탁드립니다.",
                        "description": "출처: 물반고기반",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/moolban_logo.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "물반고기반 바로가기",
                                "webLinkUrl": "https://www.moolban.com/talk/list?talk_key=6&tc_key=0&srch_sort=newest&filter_fish=&acz_key=&write_btn=N&tui_state=&tui_item_name=&tui_price_min=&tui_price_max=&tui_free_shipping=&tui_exchange=&tui_kind=&tui_price_nego="
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data        

def get_seaweather():
    
    conn = db_access()
    data = conn.exec_only_list('seaweather',17)
    
    items = []

    for item in data:
        title = '{"title" : "출처: '+item['src']+'\\n지역: '+item['area']+'\\n측정일: '+item['oday'][0:4]+'년 '+item['oday'][4:6]+'월 '+item['oday'][6:8]+'일 '+item['oday'][8:10]+'시 '+item['oday'][10:12]+'분",'
        description = '"description" : "풍향: '+item['wdir']+'\\n풍속: '+item['wspd']+'\\n풍속: '+item['wspd']+'\\nGust: '+item['gust']+'\\n기압: '+item['hpa']+'\\n습도: '+item['hum']+'\\n온도: '+item['temp']+'\\n수온: '+item['wtemp']+'\\n파고(최대): '+item['hwave']+'\\n파고(유의): '+item['nwave']+'\\n파고(평균): '+item['awave']+'\\n파주기: '+item['cwave']+'\\n파향: '+item['dwave']+'"},'
        #print(title,description)
        items.append(title+description)

    items = ''.join(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data

def get_weather():
    
    conn = db_access()
    data = conn.exec_only_list('weather',18)
    
    items = []

    for item in data:
        title = '{"title" : "출처: '+item['src']+'\\n지역: '+item['area']+'\\n측정일: '+item['mdate'][0:4]+'년 '+item['mdate'][5:7]+'월 '+item['mdate'][8:10]+'일 '+item['mdate'][11:13]+'시 '+item['mdate'][14:16]+'분",'
        description = '"description" : "상태: '+item['state']+'\\n온도: '+item['temp']+'\\n체감온도: '+item['dis']+'\\n습도: '+item['hum']+'\\n풍향: '+item['wdir']+'\\n풍속: '+item['wspeed']+'\\n기압: '+item['hpa']+'"},'
        items.append(title+description)

    items = ''.join(items)

    #print(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data

def get_yes24(kind):
    
    conn = db_access()
    data = conn.exec_kakao_yes24('yes24',kind,10)
    
    items = []

    for item in data:
        title = '{"title" : "출처: '+item['src']+'\\n구분: '+item['kname']+'\\n순위: '+item['ranking']+'\\n제목: '+item['title']+'",'
        thumbnail = '"thumbnail": {"imageUrl": "'+item['cover']+'"},'
        button = '"buttons": [{"action":  "webLink","label": "페이지로 이동","webLinkUrl": "'+item['link']+'"}]},'        
        items.append(title+thumbnail+button)

    items = ''.join(items)

    #print(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data

def get_aladin():
    
    conn = db_access()
    data = conn.exec_select(7)
    
    items = []

    for item in data:
        title = '{"title" : "출판사: '+item['publisher']+'\\n출판일: '+item['pdate']+'\\n순위: '+item['ranking']+'\\n제목: '+item['title']+'",'
        thumbnail = '"thumbnail": {"imageUrl": "'+item['src']+'"},'
        button = '"buttons": [{"action":  "webLink","label": "페이지로 이동","webLinkUrl": "'+item['link']+'"}]},'        
        items.append(title+thumbnail+button)

    items = ''.join(items)

    #print(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data    

def get_bizinfo():

    conn = db_access()
    data = conn.exec_select(1)
    
    items = []

    for item in data:
        description = '{"description" : "*과제: '+item['title']+'\\n*기한: '+item['period']+'",'
        thumbnail = '"thumbnail": {"imageUrl": "https://fishing.run.goorm.io/static/bizinfo2.png"},'
        button = '"buttons": [{"action":  "webLink","label": "페이지로 이동","webLinkUrl": "'+item['summary']+'"}]},'        
        items.append(description+thumbnail+button)

    items = ''.join(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data  

def get_thevc_invest():

    conn = db_access()
    data = conn.exec_select(10)
    
    items = []

    for item in data:
        description = '{"description" : "*투자날짜: '+item['link']+'\\n*구분: 투자/M&A\\n*투자단계: '+item['step']+'\\n*투자대상: '+item['target']+'\\n*서비스: '+item['service']+'\\n*분야: '+item['field']+'",'
        thumbnail = '"thumbnail": {"imageUrl": ""},'
        button = '"buttons": [{"action":  "webLink","label": "페이지로 이동","webLinkUrl": "https://thevc.kr/"}]},'        
        items.append(description+thumbnail+button)

    items = ''.join(items)

    #print(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data               

def get_news():

    conn = db_access()
    data = conn.exec_select(2)
    
    items = []

    for item in data:
        title = '{"title" : "수집일: '+item['rdate']+'\\n출처: '+item['src']+'\\n'+item['title']+'",'
        thumbnail = '"thumbnail": {"imageUrl": "'+item['thumbnail']+'"},'
        button = '"buttons": [{"action":  "webLink","label": "페이지로 이동","webLinkUrl": "'+item['link']+'"}]},'        
        items.append(title+thumbnail+button)

    items = ''.join(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data  
    

def get_report():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "기상특보",
                        "description": "출처: 기상청",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/kweather.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "낚다 기상특보",
                                "webLinkUrl": "http://fishing.run.goorm.io/only_list?keyword=weatherreport&limit=10"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_outgoingfish():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "낚다",
                        "description": "기상특보, 오늘의물때, 오늘의파고, 오늘의바다날씨(풍향/파향) 서비스 제공.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/outgoingfish.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "낚다 바로가기",
                                "webLinkUrl": "http://fishing.run.goorm.io"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data    

def get_caveup():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "케이브업",
                        "description": "크리에이티브 멤버십 라운지\n창업과 투자를 구독하다.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/caveup_symbol.jpg"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "케이브업 바로가기",
                                "webLinkUrl": "https://www.caveup.co.kr/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data  

def get_isdn():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "ISDN검색",
                        "description": "출처: 네이버책",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/outgoingfish.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "네이버책 ISDN검색",
                                "webLinkUrl": "https://fishing.run.goorm.io/requested?api=book"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_wave():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "오늘의 파고",
                        "description": "출처: 바다누리",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/outgoingfish.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "오늘의 파고",
                                "webLinkUrl": "http://fishing.run.goorm.io/bouy_search"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_tide():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "오늘의 물때",
                        "description": "출처: 기상청",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/outgoingfish.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "오늘의 물때",
                                "webLinkUrl": "https://fishing.run.goorm.io/tide_search"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_github():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "앤비소스",
                        "description": "출처: 앤비소스",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/gyunseul9.jpeg"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "깃허브로 바로가기",
                                "webLinkUrl": "https://github.com/gyunseul9"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data                 

def get_google_blog():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "구글 앤비매뉴얼",
                        "description": "출처: 구글 앤비매뉴얼",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/codit.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "구글 앤비매뉴얼 바로가기",
                                "webLinkUrl": "https://lonbekim.blogspot.com/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_yaporder():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "얍오더 부산",
                        "description": "점주와 고객 모두 편하고 즐거운 얍오더!\n\n[고객님]\n맛집에서 미리 주문하고 결제까지 완료하세요.⭐️\n\n[사장님]\n여러분의 고객에게 온라인으로도 최고의 경험을 보여주세요.\n\n👇자세한 내용 알아보기",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/yaporder.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "알아보기",
                                "webLinkUrl": "https://www.yaporder.com"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data 

def get_insta_nbbookshelf():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "인스타그램 앤비책장",
                        "description": "책속의 의미있는 문장을 한문장으로 요약합니다.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/nbbookshelf2.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://www.instagram.com/nbbookshelf/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_youtube_nbbookshelf():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "유튜브채널 앤비책장",
                        "description": "책속의 의미있는 문장을 한문장으로 요약합니다.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/nbbookshelf2.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://www.youtube.com/channel/UCto3cdRXEsV-UgicAElnaoQ"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_youtube_fishing():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "유튜브채널 낚다",
                        "description": "다양한 낚시정보를 공유합니다. 오늘의 조황,오늘의 물때,오늘의 날씨 등을 공유합니다.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/outgoingfish.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://www.youtube.com/channel/UCJSDgOZdf26xZKA80i5s9vw"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data         

def get_insta_nbetips():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "인스타그램 앤비팁스",
                        "description": "Startup의 Trend 정보를 공유합니다.\n특히, 요즘 Issue가 되고 있는 기술로\n투자받은 기술과 R&D 과제 정보를 공유합니다.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/cat.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://www.instagram.com/nbetips/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def get_insta_outgoingfish():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "인스타그램 낚다",
                        "description": "다양한 낚시 정보를 공유합니다.\n오늘의 조황,오늘의 물때,오늘의 날씨, 오늘의 바다날씨, 오늘의 대기정보 등을 공유합니다.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/outgoingfish.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://www.instagram.com/outgoingfish/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data                                

def call_yaporder():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "얍오더 부산",
                        "description": "고객이 원하는 비대면 모바일주문",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/yaporder.png"
                        },
                        "buttons": [
                            {
                                "action":  "phone",
                                "label": "공형조 전화연결",
                                "phoneNumber": "010-4303-1111"
                            },
                            {
                                "action":  "phone",
                                "label": "석수진 전화연결",
                                "phoneNumber": "010-2446-0977"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def call_caveup():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "케이브업",
                        "description": "크리에이티브 멤버십 라운지\n\n창업과 투자를 구독하다",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/caveup_symbol.jpg"
                        },
                        "buttons": [
                            {
                                "action":  "phone",
                                "label": "전화연결",
                                "phoneNumber": "010-9278-0866"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def call_viruszero():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "균이제로",
                        "description": "감염병 예방법에 의한 등록업체\n\n깨끗하고 안전한 일상을 위해 최선을 다하겠습니다.\n\n메트리스 청소 / 입주청소 / 마루코팅\n\n👇서비스상담",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/viruszero.jpeg"
                        },
                        "buttons": [
                            {
                                "action":  "phone",
                                "label": "전화연결",
                                "phoneNumber": "010-5804-0215"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data         

def get_airkorea():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "우리동네 대기정보",
                        "description": "출처: 에어코리아",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/airkorea.jpg"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "우리동네 대기정보 바로가기",
                                "webLinkUrl": "https://m.airkorea.or.kr/main"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data   

def go_external_footlab():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "로플랫 발자국연구소",
                        "description": "브랜드 매장과 상권들의 최근 4주간 방문자 추이를 발자국 연구소에서 확인해보세요.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/footlab.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://footlab.loplat.com/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data

def go_external_smallbiz():
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "소상공인시장진흥공단, 상권정보시스템",
                        "description": "창업가진단, 상권분석, 시장분석, 상권현황, 정책통계, 서비스 제공.",
                        "thumbnail": {
                            "imageUrl": "https://fishing.run.goorm.io/static/smallbiz.png"
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "바로가기",
                                "webLinkUrl": "https://sg.sbiz.or.kr/"
                            }
                        ]
                    }
                }
            ]
        }
    }

    return data                  

def get_branch_caveup():

    conn = db_access()
    data = conn.exec_select(14)
    
    items = []

    for item in data:
        title = '{"title" : "지점: '+item['caveupnm']+'",'
        description = '"description" : "주소: '+item['lnmadr']+'\\n정보: '+item['summary']+'",'
        thumbnail = '"thumbnail": {"imageUrl": "'+item['img180']+'"},'
        button = '"buttons": [{"action":  "webLink","label": "페이지로 이동","webLinkUrl": "'+item['link']+'"}]},'        
        items.append(title+description+thumbnail+button)

    items = ''.join(items)

    #print(items)

    prefix = '{"version": "2.0","template": {"outputs": [{"carousel": {"type" : "basicCard","items": ['
    
    postfix = ']}}]}}'

    data = prefix + items + postfix

    data = literal_eval(data)

    return data         

@app.route('/')
def main():
    set_logs('index')
    teams_messages('index')
    return render_template('index.html')
 
@app.route('/kakao', methods=['POST'])
def Message():
    
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']
    
    if content == u"낚다":
        dataSend = get_outgoingfish()
    elif content == u"케이브업":
        dataSend = get_caveup()        
    elif content == u"오늘의 조황":
        dataSend = get_fishing()
    elif content == u"기상특보":
        dataSend = get_report()
    elif content == u"오늘의 날씨":
        dataSend = get_weather()        
    elif content == u"오늘의 바다날씨":
        dataSend = get_seaweather()
    elif content == u"베스트셀러(경제/경영)":
        dataSend = get_yes24(0)
    elif content == u"베스트셀러(사회/정치)":
        dataSend = get_yes24(1)
    elif content == u"베스트셀러(소설/시/희곡)":
        dataSend = get_yes24(2)
    elif content == u"베스트셀러(에세이)":
        dataSend = get_yes24(3)
    elif content == u"베스트셀러(인문)":
        dataSend = get_yes24(4)
    elif content == u"오늘의 과제":
        dataSend = get_bizinfo()
    elif content == u"오늘의 플래텀":
        dataSend = get_news()
    elif content == u"네이버책(ISDN검색)":
        dataSend = get_isdn()
    elif content == u"오늘의 파고":
        dataSend = get_wave()
    elif content == u"오늘의 바다날씨(풍향)":
        dataSend = get_dwind()
    elif content == u"오늘의 바다날씨(파향)":
        dataSend = get_dwave()
    elif content == u"오늘의 물때":
        dataSend = get_tide()
    elif content == u"앤비코딩":
        dataSend = get_github()
    elif content == u"네이버 앤비매뉴얼":
        dataSend = get_naver_blog()
    elif content == u"앤비매뉴얼":
        dataSend = get_google_blog()
    elif content == u"얍오더란?":
        dataSend = get_yaporder()  
    elif content == u"오늘의 대기":
        dataSend = get_airkorea()
    elif content == u"오늘의 블로터":
        dataSend = get_bloter()
    elif content == u"오늘의 책":
        dataSend = get_reader()
    elif content == u"오늘의 중고책":
        dataSend = get_aladin()
    elif content == u"인스타그램 앤비책장":
        dataSend = get_insta_nbbookshelf()
    elif content == u"인스타그램 앤비팁스":
        dataSend = get_insta_nbetips()
    elif content == u"인스타그램 낚다":
        dataSend = get_insta_outgoingfish()
    elif content == u"오늘의 머니투데이":
        dataSend = get_mt()
    elif content == u"코로나 거리두기 단계":
        dataSend = get_coronastatus()
    elif content == u"유튜브채널 앤비책장":
        dataSend = get_youtube_nbbookshelf()
    elif content == u"더브이씨 투자/M&A":
        dataSend = get_thevc_invest()
    elif content == u"유튜브채널 케이브업":
        dataSend = get_youtube_caveup()
    elif content == u"앤비책장 채널 바로가기":
        dataSend = move_nbbookshelf()
    elif content == u"유튜브채널 낚다":
        dataSend = get_youtube_fishing()
    elif content == u"로플랫 발자국연구소":
        dataSend = go_external_footlab()
    elif content == u"상권정보 시스템":
        dataSend = go_external_smallbiz()
    elif content == u"케이브업 지점소개":
        dataSend = get_branch_caveup()                                                                                                                                                                                                                                                                     
    else :
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText":{
                            "text" : "다양한 컨텐츠를 준비하고 있는 중입니다."
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.
# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20150517',headers=headers)
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')
# tr들 불러오기
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > tr
daily_rank = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# 순위, 곡제목, 가수  copy selector
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

rank = 0 # 반복문 시작점 정해주기, 난 1위부터 볼거니까 0부터 스타트!
for song in daily_rank:
	number = song.select_one('td.number').text
	title = song.select_one('td.info > a.title.ellipsis').text.strip()
	artist = song.select_one('td.info > a.artist.ellipsis').text.strip()
	rank += 1 # 50위까지 계속 반복! 다른 숫자 넣어보면 다 1등 만들수도 있음! 샤이니도 1등! 아이유도 1등!

	if not title == None:
		adddb = {
			'number': number,
			'title': title,
			'artist': artist
		}
		db.daily_rank.insert_one(adddb) #insert 개념 확실히 알앗다..어젠 뉴개념이엇는데..숙제 꼭 하기..
		print(rank,title,artist)
		#샤이니 일간순위 안에 있는 리스트 보고 싶어서 만든 웹 크롤링 끝.

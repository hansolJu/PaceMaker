#서버를 처음 킬 때, 데이터를 업데이트 해야함. 물론, 기존의 디비에 데이터가 없다면 새로 생성할 것.
from dataParser.parser import ServerParser
from datetime import datetime
from dataParser.models import Course

serverParser = ServerParser('admin', 'wjd123123')

todayYear = datetime.today().year
todayMonth = datetime.today().month
todayDay = datetime.today().day

try: #2018년 1학기 전공 정보 저장 및 업데이트
    courses = Course.objects.filter(year = '2018', semester = '10')
except Course.DoesNotExist: #해당 데이터가 없음
    serverParser.save_course_major(serverParser.parse_course_major('2018', '10'))
    serverParser.save_course_detail(serverParser.par)

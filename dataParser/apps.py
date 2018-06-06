from django.apps import AppConfig


class DataparserConfig(AppConfig):
    name = 'dataParser'

    # def ready(self):
    #     # 서버를 처음 킬 때, 데이터를 업데이트 해야함. 물론, 기존의 디비에 데이터가 없다면 새로 생성할 것.
    #     from dataParser.parser import ServerParser
    #     from datetime import datetime
    #     from dataParser.models import Course, Professor, Subject_desription, Core_Competence, Learning_Objectives, \
    #         Lecture_method, Assignment, School_composition_ratio, Weekly_course_contents, Book
    #
    #     serverParser = ServerParser('201511858', 'Eunjin1221')
    #
    #     serverParser.save_course_detail(287,serverParser.parse_course_detail(1,2,3,4))
    #
    #
    #
    def ready(self):
            from dataParser.parser import ServerParser
            from datetime import datetime
            admin_id = "201511868"
            admin_pw = "1019711"
            print("init")
            parser = ServerParser(admin_id, admin_pw)
            for year in range(2010, 2018):
                print(year)
                print(datetime.today().year)
                for semester in range(1, 3):
                    print(semester)
                    tmp= parser.parse_course_major(year, semester*10)
                    print(tmp)
                    parser.save_course_major(year, semester*10, tmp)
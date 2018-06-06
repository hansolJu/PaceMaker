from django.apps import AppConfig


class ClassesConfig(AppConfig):
    name = 'classes'

    def ready(self):
        from dataParser.models import Course
        from classes.models import classCourse, necessaryCourse, promotedCourse

        year = 2017
        child = '자바프로그래밍'
        parent = '소프트웨어공학'

        # dic = dict()
        # dic['창의기초설계'] = '자바프로그래밍'
        # dic['자바프로그래밍'] = '소프트웨어공학'
        # dic['소프트웨어공학'] = '캡스톤설계'
        # dic['데이터베이스'] = '데이터베이스프로그래밍'
        # dic['운영체제'] = '내장형시스템'
        # dic['컴퓨터그래픽스'] = '멀티미디어처리기술'
        # dic['컴퓨터네트워크'] = '네트워크시스템프로그래밍'




        # dic = dict()
        # dic['이산수학'] = '계산이론'
        # dic['컴퓨터구조'] = '시스템소프트웨어'
        # dic['계산이론'] = '알고리듬'
        # dic['자료구조론'] = '컴퓨터네트워크'
        # dic['워크플로우관리시스템'] = '캡스톤설계'
        # dic['운영체제'] = '분산및병렬처리'
        # dic['네트워크시스템프로그래밍'] = '분산및병렬처리'
        # dic['네트워크시스템프로그래밍'] = '웹서비스설계'
        # dic['프로그래밍언어론'] = '웹서비스설계'
        # dic['데이터베이스프로그래밍'] = '웹서비스설계'
        # dic['수치계산'] = '컴퓨터보안'
        # dic['수치계산'] = '알고리듬'
        #
        #
        #
        #
        # for child, parent in dic.items():
        #     try:
        #         temp = promotedCourse(year=year,
        #                                childCourse_id=classCourse.objects.filter(subjectName=child).order_by('year').last().id,
        #                                parentCourse_id = classCourse.objects.filter(subjectName=parent).order_by('year').last().id)
        #         temp.save()
        #     except:
        #         pass

    # def ready(self):
    #     from dataParser.models import Course
    #     from classes.models import classCourse, necessaryCourse, promotedCourse
    #     allDataCourses = Course.objects.all()
    #     for dataCourse in allDataCourses:
    #         """
    #         나는 데이터코스에서 모든 정보를 가져온다. 여기서 난 각 year의 subject를 하나만 가져오고 싶다.'
    #         따라서, 데이터코스에서 해당 이름으로 모두 가져온담에, classCourse을 해당 이름으로 가져온다.
    #         그리고나서 둘이 intersection으로
    #         """
    #         preClassCourse = classCourse.objects.filter(subjectName=dataCourse.subjectName)
    #         if dataCourse.subjectName in preClassCourse.values_list('subjectName', flat=True) and dataCourse.year in preClassCourse.values_list('year', flat=True):
    #             continue
    #         classCourse(
    #             year= dataCourse.year,
    #             semester = dataCourse.semester,
    #             subjectCode = dataCourse.subjectCode,
    #             subjectName = dataCourse.subjectName,
    #             grade = dataCourse.grade,
    #             eisu = dataCourse.eisu,
    #             score = dataCourse.score,
    #             professor = dataCourse.professor,
    #             remarks = dataCourse.remarks,
    #             time = dataCourse.time,
    #             lectureRoom = dataCourse.lectureRoom,
    #             huksu_code = dataCourse.huksu_code,
    #             course_time = dataCourse.course_time,
    #             design_score = dataCourse.design_score,
    #
    #             description = dataCourse.desription,
    #             Knowledge_application= dataCourse.Knowledge_application,
    #             verification_ability = dataCourse.verification_ability,
    #             problem_solving = dataCourse.problem_solving,
    #             tool_utilization = dataCourse.tool_utilization,
    #             design_ability = dataCourse.design_ability,
    #             teamwork_skill = dataCourse.teamwork_skill,
    #             communication =  dataCourse.communication,
    #             understanding_of_influence =  dataCourse.understanding_of_influence,
    #             responsibility =  dataCourse.responsibility,
    #             self_led =  dataCourse.self_led,
    #
    #             # # table[3] 교과목 학습목표
    #             # # [핵심역량, 세부핵심역량, 반영률, 학습목표, 수행준거, 성취목표, 평가방법]
    #             # core_competencies =  dataCourse.core_competencies
    #             # detailed_core_competencies =  dataCourse.detailed_core_competencies
    #             # reflectance =  dataCourse.reflectance
    #             # learning_objectives =  dataCourse.learning_objectives
    #             # performance_criteria =  dataCourse.performance_criteria
    #             # achievement_goals =  dataCourse.achievement_goals
    #             # evaluation_methods =  dataCourse.evaluation_methods
    #
    #             # table[4] 강의방법
    #             # [강의형태, 수업방식, 교육용기자재]
    #             Lecture_type =  dataCourse.Lecture_type,
    #             teaching_method =  dataCourse.teaching_method,
    #             educational_equipment =  dataCourse.educational_equipment,
    #
    #             # table[5] 과제물
    #             # [과제물]
    #             Assignment =  dataCourse.Assignment,
    #
    #             # table[6] 성적 구성비율 존나 머리 안돌아가서 하드코딩되있음.
    #             # ['중간시험', '기말시험', '출석', '과제물및기타', '성적평가구분']
    #             Midterm_exam =  dataCourse.Midterm_exam,
    #             final_exam =  dataCourse.final_exam,
    #             attendance =  dataCourse.attendance,
    #             assignments_and_others =  dataCourse.assignments_and_others,
    #             grading_division =  dataCourse.grading_division,
    #
    #             # table[7] 주별 강좌내용
    #
    #             # table[8] 책
    #             # [도서명, 저자, 출판사, 출판년도]
    #             title =  dataCourse.title,
    #             author =  dataCourse.author,
    #             publisher =  dataCourse.publisher,
    #             year_of_publication =  dataCourse.year_of_publication
    #         ).save()


from django.apps import AppConfig

class ClassesConfig(AppConfig):
    name = 'classes'

    def ready(self):
        from dataParser.models import Course as dataCourse
        from classes.models import Course as classCourse, necessaryCourse, promotedCourse
        allDataCourses = dataCourse.objects.all()
        for dataCourse in allDataCourses:
            if classCourse.objects.filter(subjectName=dataCourse.subjectName).count() == 0:
                classCourse(
                    year= dataCourse.year,
                    semester = dataCourse.semester,
                    subjectCode = dataCourse.subjectCode,
                    subjectName = dataCourse.subjectName,
                    grade = dataCourse.grade,
                    eisu = dataCourse.eisu,
                    score = dataCourse.score,
                    professor = dataCourse.professor,
                    remarks = dataCourse.remarks,
                    time = dataCourse.time,
                    lectureRoom = dataCourse.lectureRoom,
                    huksu_code = dataCourse.huksu_code,
                    course_time = dataCourse.course_time,
                    design_score = dataCourse.design_score,

                    description = dataCourse.desription,
                    Knowledge_application= dataCourse.Knowledge_application,
                    verification_ability = dataCourse.verification_ability,
                    problem_solving = dataCourse.problem_solving,
                    tool_utilization = dataCourse.tool_utilization,
                    design_ability = dataCourse.design_ability,
                    teamwork_skill = dataCourse.teamwork_skill,
                    communication =  dataCourse.communication,
                    understanding_of_influence =  dataCourse.understanding_of_influence,
                    responsibility =  dataCourse.responsibility,
                    self_led =  dataCourse.self_led,

                    # # table[3] 교과목 학습목표
                    # # [핵심역량, 세부핵심역량, 반영률, 학습목표, 수행준거, 성취목표, 평가방법]
                    # core_competencies =  dataCourse.core_competencies
                    # detailed_core_competencies =  dataCourse.detailed_core_competencies
                    # reflectance =  dataCourse.reflectance
                    # learning_objectives =  dataCourse.learning_objectives
                    # performance_criteria =  dataCourse.performance_criteria
                    # achievement_goals =  dataCourse.achievement_goals
                    # evaluation_methods =  dataCourse.evaluation_methods

                    # table[4] 강의방법
                    # [강의형태, 수업방식, 교육용기자재]
                    Lecture_type =  dataCourse.Lecture_type,
                    teaching_method =  dataCourse.teaching_method,
                    educational_equipment =  dataCourse.educational_equipment,

                    # table[5] 과제물
                    # [과제물]
                    Assignment =  dataCourse.Assignment,

                    # table[6] 성적 구성비율 존나 머리 안돌아가서 하드코딩되있음.
                    # ['중간시험', '기말시험', '출석', '과제물및기타', '성적평가구분']
                    Midterm_exam =  dataCourse.Midterm_exam,
                    final_exam =  dataCourse.final_exam,
                    attendance =  dataCourse.attendance,
                    assignments_and_others =  dataCourse.assignments_and_others,
                    grading_division =  dataCourse.grading_division,

                    # table[7] 주별 강좌내용

                    # table[8] 책
                    # [도서명, 저자, 출판사, 출판년도]
                    title =  dataCourse.title,
                    author =  dataCourse.author,
                    publisher =  dataCourse.publisher,
                    year_of_publication =  dataCourse.year_of_publication
                ).save()

        #저장완료

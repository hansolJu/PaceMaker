from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.auth.hashers import make_password


# Create your models here.
class StudentInfo(AbstractUser):
    hukbun = models.CharField(max_length=15, primary_key=True)
    # name = models.CharField(max_length=10, blank=True, null=True) username으로 사용합시다
    jumin = models.CharField(max_length=12, blank=True, null=True)
    # 과정구분
    course = models.CharField(max_length=5, blank=True, null=True)
    # 학적구분
    state = models.CharField(max_length=10, blank=True, null=True)
    # 학적변동
    variance = models.CharField(max_length=10, blank=True, null=True)
    # 졸업학점
    graduationCredit = models.CharField(max_length=10, blank=True, null=True)
    # 전공
    major = models.CharField(max_length=20, blank=True, null=True)
    # 지도교수
    advisor = models.CharField(max_length=10, blank=True, null=True)
    # 현학년학기
    currentGrade = models.CharField(max_length=10, blank=True, null=True)
    # 이수학기/현입인정학기
    compleSemester = models.CharField(max_length=3, blank=True, null=True)
    # 조기졸업대상여부 ???이거 못정하겠음.
    earlyGraduation = models.CharField(max_length=1, blank=True, null=True)
    # 입학일자
    admission = models.CharField(max_length=10, blank=True, null=True)
    # 공학인증구분
    enginCertification = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'hukbun'
    REQUIRED_FIELDS = ['username', 'email']

    # is_anonymous = models.NullBooleanField()
    # is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    #
    # @property
    # def is_authenticated(self):
    #     """
    #     Always return True. This is a way to tell if the user has been
    #     authenticated in templates.
    #     """
    #     return True
    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #     self._password = raw_password

    def __str__(self):
        return self.username


class StudentGrade(models.Model):
    hukbun = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    # 이수구분
    eisu = models.CharField(max_length=50, blank=True, null=True)
    # 인증구분
    certification = models.CharField(max_length=50, blank=True, null=True)
    # 년도학기
    yearNsemester = models.CharField(max_length=50, blank=True, null=True)
    # 학수코드
    subject_code = models.CharField(max_length=50, blank=True, null=True)
    # 교과목명
    subject = models.CharField(max_length=50, blank=True, null=True)
    # 학점
    score = models.CharField(max_length=50, blank=True, null=True)
    # 설계학점
    grade_design = models.CharField(max_length=50, blank=True, null=True)
    # 등급
    grade = models.CharField(max_length=50, blank=True, null=True)
    # 유효구분
    valid = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.subject


class StudentHopeCareers(models.Model):
    "개인 신상정보 -- 학생취업신상정보"
    hukbun = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    # 진로구분
    careers = models.CharField(max_length=50, blank=True, null=True)
    # 지망순위
    ranking = models.IntegerField()
    # 직업(중분류)

    # 직업(소분류)
    job = models.CharField(max_length=50, blank=True, null=True)
    # 희망기업
    Enterprise = models.CharField(max_length=50, blank=True, null=True)
    # 희망연봉
    Salary = models.CharField(max_length=50, blank=True, null=True)
    # 희망근무지역
    Address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.ranking


class Professor(models.Model):
    hukbun = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20, null=False)


class Course(models.Model):
    # 년도
    year = models.CharField(max_length=15)
    # 학기
    semester = models.CharField(max_length=15)
    # 과목번호
    subjectCode = models.CharField(max_length=15)
    # 과목이름
    subjectName = models.CharField(max_length=50, blank=True, null=True)
    # 추천학년(학교에서)
    grade = models.CharField(max_length=50, blank=True, null=True)
    # 이수구분
    eisu = models.CharField(max_length=50, blank=True, null=True)
    # 학점
    score = models.CharField(max_length=50, blank=True, null=True)
    # 담당교수
    professor = models.CharField(max_length=50, blank=True, null=True)
    # 비고
    remarks = models.CharField(max_length=50, blank=True, null=True)
    # 교시
    time = models.CharField(max_length=50, blank=True, null=True)
    # 강의실
    lectureRoom = models.CharField(max_length=100, blank=True, null=True)
    # 학수코드
    huksu_code = models.CharField(max_length=50, blank=True, null=True)
    # 강의시수
    course_time = models.CharField(max_length=15, blank=True, null=True)
    # 설계시수
    design_score = models.CharField(max_length=15, blank=True, null=True)

    # table[1] 교과목 해설
    desription = models.CharField(max_length=1000,blank=True, null=True)

    # table[2] 새부핵심역량 과의 관계
    # [지식응용, 검증능력, 문제해결, 도구활용, 설계능력, 팀웍스킬, 의사전달, 영향이해, 책임의식, 자기주도]
    Knowledge_application = models.CharField(max_length=5,blank=True, null=True)
    verification_ability = models.CharField(max_length=5,blank=True, null=True)
    problem_solving = models.CharField(max_length=5,blank=True, null=True)
    tool_utilization = models.CharField(max_length=5,blank=True, null=True)
    design_ability = models.CharField(max_length=5,blank=True, null=True)
    teamwork_skill = models.CharField(max_length=5,blank=True, null=True)
    communication = models.CharField(max_length=5,blank=True, null=True)
    understanding_of_influence = models.CharField(max_length=5,blank=True, null=True)
    responsibility = models.CharField(max_length=5,blank=True, null=True)
    self_led = models.CharField(max_length=5,blank=True, null=True)

    # # table[3] 교과목 학습목표
    # # [핵심역량, 세부핵심역량, 반영률, 학습목표, 수행준거, 성취목표, 평가방법]
    # core_competencies = models.CharField(max_length=10,blank=True, null=True)
    # detailed_core_competencies = models.CharField(max_length=10,blank=True, null=True)
    # reflectance = models.CharField(max_length=5,blank=True, null=True)
    # learning_objectives = models.CharField(max_length=200,blank=True, null=True)
    # performance_criteria = models.CharField(max_length=200,blank=True, null=True)
    # achievement_goals = models.CharField(max_length=5,blank=True, null=True)
    # evaluation_methods = models.CharField(max_length=10,blank=True, null=True)

    # table[4] 강의방법
    # [강의형태, 수업방식, 교육용기자재]
    Lecture_type = models.CharField(max_length=100,blank=True, null=True)
    teaching_method = models.CharField(max_length=100,blank=True, null=True)
    educational_equipment = models.CharField(max_length=100,blank=True, null=True)

    # table[5] 과제물
    # [과제물]
    Assignment = models.CharField(max_length=500,blank=True, null=True)

    # table[6] 성적 구성비율 존나 머리 안돌아가서 하드코딩되있음.
    # ['중간시험', '기말시험', '출석', '과제물및기타', '성적평가구분']
    Midterm_exam = models.CharField(max_length=10,blank=True, null=True)
    final_exam = models.CharField(max_length=10,blank=True, null=True)
    attendance = models.CharField(max_length=10,blank=True, null=True)
    assignments_and_others = models.CharField(max_length=10,blank=True, null=True)
    grading_division = models.CharField(max_length=10,blank=True, null=True)

    # table[7] 주별 강좌내용

    # table[8] 책
    # [도서명, 저자, 출판사, 출판년도]
    title = models.CharField(max_length=200,blank=True, null=True)
    author = models.CharField(max_length=300,blank=True, null=True)
    publisher = models.CharField(max_length=100,blank=True, null=True)
    year_of_publication = models.CharField(max_length=20,blank=True, null=True)

    # class Meta:
    #     unique_together = ('year', 'semester', 'subjectCode')z

    def __str__(self):
        return self.subjectName



# table[6] 주별 강좌내용
class Weekly_course_contents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # [주, 교수내용, 방법, 관련자료, 과제물]
    week = models.CharField(max_length=1,blank=True, null=True)
    contents = models.CharField(max_length=500,blank=True, null=True)
    methods = models.CharField(max_length=20,blank=True, null=True)
    related_materials = models.CharField(max_length=20,blank=True, null=True)
    assignments = models.CharField(max_length=200,blank=True, null=True)

from django.db import models

# Create your models here.

class StudentInfo(models.Model):
    hukbun = models.IntegerField()
    name = models.CharField(max_length=10)
    jumin = models.CharField(max_length=12)
    #과정구분
    course = models.CharField(max_length=5)
    #학적구분
    state = models.CharField(max_length=10)
    #학적변동
    variance = models.CharField(max_length=10)
    #졸업학점
    gradeCredit = models.IntegerField()
    #전공
    major = models.CharField(max_length=20)
    #지도교수
    advisor = models.CharField(max_length=10)
    #현학년학기
    cntCredit = 13
    #이수학기/현입인정학기
    compleSemester = models.CharField(max_length=3)
    #조기졸업대상여부 ???이거 못정하겠음.
    earlyGradu = models.CharField(max_length=1)
    #입학일자
    admission = models.DateField()
    #공학인증구분
    enginCertifi = models.CharField(max_length=20)


class StudentGrade(models.Model):
    hukbun = models.ForeignKey(StudentInfo,on_delete=models.CASCADE)
    #이수구분
    eisu = models.CharField(max_length=50, blank=True,null=True)
    # 인증구분
    certification = models.CharField(max_length=50, blank=True,null=True)
    # 년도학기
    yearNsemester = models.CharField(max_length=50, blank=True,null=True)
    # 학수코드
    subject_code = models.CharField(max_length=50, blank=True,null=True)
    # 교과목명
    subject = models.CharField(max_length=50, blank=True,null=True)
    # 학점
    score = models.CharField(max_length=50, blank=True,null=True)
    # 설계학점
    grade_design = models.CharField(max_length=50, blank=True,null=True)
    # 등급
    grade = models.CharField(max_length=50, blank=True,null=True)
    # 유효구분
    valid = models.CharField(max_length=50, blank=True,null=True)


class StudentHopeCareers(models.Model):
    "개인 신상정보 -- 학생취업신상정보"
    hukbun = models.ForeignKey(StudentInfo,on_delete=models.CASCADE)
    # 진로구분
    careers = models.CharField(max_length=50, blank=True,null=True)
    # 지망순위
    ranking = models.IntegerField()
    # 직업(중분류)

    # 직업(소분류)
    job = models.CharField(max_length=50, blank=True, null=True)
    # 희망기업
    Enterprise = models.CharField(max_length=50, blank=True,null=True)
    # 희망연봉
    Salary = models.CharField(max_length=50, blank=True,null=True)
    # 희망근무지역
    Address = models.CharField(max_length=50, blank=True,null=True)

    def __str__(self):
        return self.ranking


class Schedule(models.Model):
    # 과목번호
    subjectCode = models.IntegerField()
    # 과목이름
    subjectName = models.CharField(max_length=50, blank=True,null=True)
    # 추천학년(학교에서)
    grade = models.IntegerField()
    # 이수구분
    eisu = models.CharField(max_length=50, blank=True,null=True)
    # 학점
    score = models.IntegerField()
    # 담당교수
    professor = models.CharField(max_length=50, blank=True,null=True)
    # 비고
    remarks = models.CharField(max_length=50, blank=True, null=True)
    # 교시
    time = models.CharField(max_length=50, blank=True,null=True)
    # 강의실
    lectureRoom = models.CharField(max_length=100, blank=True,null=True)

    def __str__(self):
        return self.subjectName
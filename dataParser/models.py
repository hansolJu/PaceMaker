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

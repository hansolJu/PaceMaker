from django.shortcuts import render
from dataParser.models import StudentInfo, Course, StudentGrade
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
import operator


# Create your views here.
class majorLV(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'classes/majorAll.html'
    context_object_name = 'subjects'
    paginate_by = 2


class majorDV(LoginRequiredMixin, DetailView):
    model = Course


class recommand(LoginRequiredMixin, View):
    """
    1. 내가 들을 수 있는 아직 듣지 않은 전공 수업들 보여줌
    2. 제일 잘 나가는 타 학생의 전공 수업들을 보여줌
    3. 재수강 추천 과목을 보여줌 (낮은 성적부터)
    4. 학년과 맞지 않는 수업을 들은 케이스를 보여줌
    """
    takenCoursesPKList = []
    notTakenCoursesPKList = []
    topStudentCourses = []
    retakeCourses = []
    def get(self, request):
        student = StudentInfo.objects.get(hukbun=request.user.hukbun)
        takenCoursesGrades = StudentGrade.objects.filter(hukbun=student.hukbun)

        self.getCoursesPKList()


    def getSpecialCase(self): #자신의 학년과 맞지 않게 다른 학년의 수업을 들은 경우를 보여줌
        """
        grade에 yearNsemester에서 yyyy년도s학기 정보가 나옴.
        filter로 학생의 모든 grade정보를 가져와서 yearNsemester를 중복제거한 리스트로 보자. 이의 개수 하나당 학기 하나 -> 들었을 때 학년을 알 수 있다.
        얻어진 학년과 studentGrade에서 year,semester,subject_code를 이용해서 얻어진 course의 학년과 비교해서 다를 경우
            과목, 들었을 때의 학년 정보를 딕셔너리화해서 저장하자
        :return: 
        """
        allStudents = StudentInfo.objects.all()
        allGrades = StudentGrade.objects.all()
        
    def getRetakeCourses(self, student, takenCoursesGrades):
        takenCoursesScoresDic = {}
        for takenCourseGrade in takenCoursesGrades:   #딕셔너리에 과목코드:(int)점수 저장
            takenCoursesScoresDic[takenCourseGrade.subject_code] = self.getIntScore(takenCourseGrade.grade)
        takenCoursesScoresDic = sorted(takenCoursesScoresDic.items(), key=operator.itemgetter(1)) #오름차순 정렬
        self.retakeCourses = takenCoursesScoresDic.keys()
    def getTopStudentCourses(self):
        #지훈이가 하길 기다리자
        pass
    def getCoursesPKList(self, student, takenCoursesGrades): #들었던 전공 수업의 리스트와 듣지 않은 전공 수업의 리스트 보여줌
        for grade in takenCoursesGrades:
            try:
                self.takenCoursesPKList.append(Course.objects.get(year=grade.year, semester=grade.semester, subjectCode=grade.subject_code))
            except Course.DoesNotExist:
                continue
        self.takenCoursesPKList = list(set(self.takenCoursesPKList)) #들은 수업들 구함

        allCoursesPKList = []
        for course in Course.objects.all():
            allCoursesPKList.append(course.id)
        self.notTakenCoursesPKList = list(set(allCoursesPKList) - set(self.takenCoursesPKList)) #안 들은 전공 수업

    def getIntScore(self, score):
        if score == 'A+':
            return 4.5
        elif score == 'A':
            return 4.0
        elif score == 'B+':
            return 3.5
        elif score == 'B':
            return 3.0
        elif score == 'C+':
            return 2.5
        elif score == 'C':
            return 2.0
        elif score == 'D+':
            return 1.5
        elif score == 'D':
            return 1.0
        elif score == 'F':
            return 4.0
        else :
            return None
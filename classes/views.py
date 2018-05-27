from django.shortcuts import render
from dataParser.models import StudentInfo, Course, StudentGrade
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


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
    4.

    """
    takenCoursesPKList = []
    notTakenCoursesPKList = []
    def get(self, request):
        student = StudentInfo.objects.get(hukbun=request.user.hukbun)
        takenCoursesGrades = StudentGrade.objects.filter(hukbun=student.hukbun)

        self.getCoursesPKList()

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



from django.shortcuts import render
from dataParser.models import (StudentInfo, Course, StudentGrade, Subject_desription,
                               Core_Competence, Learning_Objectives, Lecture_method,
                               Assignment, School_composition_ratio, Weekly_course_contents, Book)
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from datetime import datetime


# Create your views here.
class majorLV(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'classes/majorAll.html'
    context_object_name = 'subjects'
    paginate_by = 20

    def get_queryset(self):
        return Course.objects.filter(year=datetime.today().year).order_by('grade', 'subjectName')


class majorDV(LoginRequiredMixin, TemplateView):
    template_name = 'classes/majorDetail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(majorDV, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        # Subject_desription, Core_Competence, Learning_Objectives,
        # Lecture_method, Assignment, School_composition_ratio, Weekly_course_contents, Book
        try:
            context['subjectName'] = Course.objects.get(id=context['pk'])
        except:
            context['subjectName'] = None
        try:
            context['subjectDescriptions'] = Subject_desription.objects.filter(course=context['pk'])
        except:
            context['subjectDescriptions'] = None
        try:
            context['coreCompetences'] = Core_Competence.objects.filter(id=context['pk'])
        except:
            context['coreCompetences'] = None
        try:
            context['learningObjectives'] = Learning_Objectives.objects.filter(id=context['pk'])
        except:
            context['learningObjectives'] = None
        try:
            context['lectureMethods'] = Lecture_method.objects.filter(id=context['pk'])
        except:
            context['lectureMethods'] = None
        try:
            context['assignments'] = Assignment.objects.filter(id=context['pk'])
        except:
            context['assignments'] = None
        try:
            context['schoolCompositionRatios'] = School_composition_ratio.objects.filter(id=context['pk'])
        except:
            context['schoolCompositionRatios'] = None
        try:
            context['weeklyCourseContents'] = Weekly_course_contents.objects.filter(id=context['pk'])
        except:
            context['weeklyCourseContents'] = None
        try:
            context['books'] = Book.objects.filter(id=context['pk'])
        except:
            context['books'] = None
        return context


class SpecialCourseRecommandView(LoginRequiredMixin, TemplateView):
    template_name = "classes/special_recommand.html"

    def get_context_data(self, **kwargs):
        context = super(SpecialCourseRecommandView, self).get_context_data(**kwargs)
        student = StudentInfo.objects.get(hukbun=self.request.user.hukbun)

        context['specialCoursesDic'] = self.getSpecialCase()
        return context

    def getSpecialCase(self):  # 자신의 학년과 맞지 않게 다른 학년의 수업을 들은 경우를 보여줌
        """
        grade에 yearNsemester에서 yyyy년도s학기 정보가 나옴.
        filter로 학생의 모든 grade정보를 가져와서 yearNsemester를 중복제거한 리스트로 보자. 이의 개수 하나당 학기 하나 -> 들었을 때 학년을 알 수 있다.
        얻어진 학년과 studentGrade에서 year,semester,subject_code를 이용해서 얻어진 course의 학년과 비교해서 다를 경우
            과목, 들었을 때의 학년 정보를 딕셔너리화해서 저장하자
        """
        specialCoursesDic = dict()
        for student in StudentInfo.objects.all():  # 모든 학생
            studentGrades = StudentGrade.objects.filter(hukbun=student.hukbun)  # 학생의 grade 쿼리셋
            semesterList = studentGrades.values_list('yearNsemester', flat=True)  # 학생의 학기 list
            semesterList = sorted(list(set(semesterList)))  # 중복제거하여 정렬
            for grade in studentGrades:  # 학생이 과목을 들었을 때 학년이 일치하는 지 확인한다.
                semester = semesterList.index(  # semester = 학생이 들었던 해당 수업을 들었을 때의 학기
                    grade.yearNsemester)  # 해당 과목의 학기가 semesterList에서 검색해 index를 반환한다 => 해당 과목이 몇학기에 들은 과목인가 검사
                courses = Course.objects.filter(subjectName=grade.subject)  # 해당 수업의 이름과 동일한 course 쿼리셋 가져오기
                if courses.count() == 0:  # 만약 해당하는 수업이 없다면 걍 무시
                    continue
                courseInfoes = []
                course = courses.first()
                courseGrade = courses.first().grade  # 수업을 대충 하나 가져와서 추천 학년을 저장
                if int(semester / 2) + 1 != int(courseGrade):  # 추천 학년대로 과목을 안 들었을 경우
                    courseInfoes.append(course.grade)  # 추천 학년
                    courseInfoes.append(int(semester / 2) + 1)  # 들었던 학년
                    courseInfoes.append(course.eisu)  # 이수
                    courseInfoes.append(course.score)  # 학점
                    specialCoursesDic[grade] = courseInfoes

        # 이제 중복된 전공을 없애고 카운트하는게 필요
        grades = list(specialCoursesDic.keys())  # grade 객체 리스트
        gradesSubjectName = []
        for grade in grades:  # grades := grades의 과목 이름 리스트
            gradesSubjectName.append(grade.subject)
        notDuplicatedGrades = list(set(gradesSubjectName))
        print(notDuplicatedGrades)
        for notDuplicatedGrade in notDuplicatedGrades:
            count = 0
            for grade in specialCoursesDic.keys():
                if notDuplicatedGrade == grade.subject:
                    count += 1
            print(grades)
            for grade in grades:
                if grade.subject == notDuplicatedGrade:
                    specialCoursesDic[grade].append(count)

        return specialCoursesDic


class TopStudentRecommandView(LoginRequiredMixin, TemplateView):
    pass


class RetakeRecommandView(LoginRequiredMixin, TemplateView):
    template_name = "classes/retaking_recommand.html"
    """
    1. 내가 들을 수 있는 아직 듣지 않은 전공 수업들 보여줌
    2. 제일 잘 나가는 타 학생의 전공 수업들을 보여줌
    3. 재수강 추천 과목을 보여줌 (낮은 성적부터)
    """
    topStudentCourses = []

    def get_context_data(self, **kwargs):
        context = super(RetakeRecommandView, self).get_context_data(**kwargs)
        student = StudentInfo.objects.get(hukbun=self.request.user.hukbun)
        takenCoursesGrades = StudentGrade.objects.filter(hukbun=student.hukbun)
        # self.getRetakeCourses(student, takenCoursesGrades)
        context['retakeGrades'] = self.getRetakeCourses(student, takenCoursesGrades).order_by('yearNsemester',
                                                                                              'subject')

        return context

    def getRetakeCourses(self, student, takenCoursesGrades):
        takenCoursesScoresDic = dict()
        retakeCoursesName = []
        canceledList = []
        for takenCourseGrade in takenCoursesGrades:  # 딕셔너리에 과목코드:(int)점수 저장
            try:
                if self.getIntScore(takenCourseGrade.grade) <= 2.5:  # 2.5
                    takenCoursesScoresDic[takenCourseGrade.subject] = self.getIntScore(takenCourseGrade.grade)
            except:
                continue

        sortedTakenCoursesScoresList = sorted(takenCoursesScoresDic.items(), key=lambda x: x[1])
        for sortedTakenCoursesScores in sortedTakenCoursesScoresList:
            retakeCoursesName.append(sortedTakenCoursesScores[0])

        resultGrades = StudentGrade.objects.filter(subject__in=retakeCoursesName,
                                                   hukbun=student.hukbun)  # 재수강 추천 과목 쿼리셋을 리턴
        for resultGrade in resultGrades:
            try:
                if self.getIntScore(resultGrade.grade) >= 2.5:
                    resultGrades.difference(resultGrades.filter(subject=resultGrade.subject))
            except:
                continue
        canceledList = resultGrades.filter(valid='재수강무효').values_list('subject')
        return resultGrades.difference(resultGrades.filter(valid='재수강무효')).difference(
            resultGrades.filter(subject__in=canceledList))

    def getTopStudentCourses(self):
        # 지훈이가 하길 기다리자
        pass

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
        else:
            return None
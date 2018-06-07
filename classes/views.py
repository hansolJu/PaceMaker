from django.shortcuts import render
from dataParser.models import StudentInfo, Course, StudentGrade, Weekly_course_contents
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, TemplateView
from datetime import datetime
from django.db.models import Q
from grades.views import getIntScore
import operator
from .models import classCourse, necessaryCourse, promotedCourse
from django.db.models import Count

def get_score_sum(hukbun):
    s = hukbun
    sum = 0
    scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
    scorelist = scorelist.exclude(grade__contains='P').values_list('score', flat=True)
    for i in scorelist:
        sum = sum + int(i)

    return sum

def get_avgGrade(hukbun):
    s = hukbun
    avg = 0.0
    sum = 0.0
    gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
        Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(
            grade='D'))
    for i in range(0, gradelist.count()):
        temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
        sum = sum + temp
    score_sum = get_score_sum(hukbun)
    avg = sum / score_sum
    avg = round(avg, 3)
    return avg

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
            context['subjectName'] = Course.objects.get(id=context['pk']).subjectName
        except:
            context['subjectName'] = None
        try:
            context['subjectDescriptions'] = Course.objects.get(id=context['pk']).desription
        except:
            context['subjectDescriptions'] = None
        try:
            temp = []
            temp.append(Course.objects.get(id=context['pk']).Knowledge_application)
            temp.append(Course.objects.get(id=context['pk']).verification_ability)
            temp.append(Course.objects.get(id=context['pk']).problem_solving)
            temp.append(Course.objects.get(id=context['pk']).tool_utilization)
            temp.append(Course.objects.get(id=context['pk']).design_ability)
            temp.append(Course.objects.get(id=context['pk']).teamwork_skill)
            temp.append(Course.objects.get(id=context['pk']).communication)
            temp.append(Course.objects.get(id=context['pk']).understanding_of_influence)
            temp.append(Course.objects.get(id=context['pk']).responsibility)
            temp.append(Course.objects.get(id=context['pk']).self_led)
            context['coreCompetences'] = temp
        except:
            context['coreCompetences'] = None
        try:
            temp = []
            temp.append(Course.objects.get(id=context['pk']).Lecture_type)
            temp.append(Course.objects.get(id=context['pk']).teaching_method)
            temp.append(Course.objects.get(id=context['pk']).educational_equipment)
            context['lectureMethods'] = temp
        except:
            context['lectureMethods'] = None
        try:
            temp = []
            temp.append(Course.objects.get(id=context['pk']).Assignment)
            context['assignments'] = temp
        except:
            context['assignments'] = None
        try:
            temp = []
            temp.append(Course.objects.get(id=context['pk']).Midterm_exam)
            temp.append(Course.objects.get(id=context['pk']).final_exam)
            temp.append(Course.objects.get(id=context['pk']).attendance)
            temp.append(Course.objects.get(id=context['pk']).assignments_and_others)
            temp.append(Course.objects.get(id=context['pk']).grading_division)
            context['schoolCompositionRatios'] = temp
        except:
            context['schoolCompositionRatios'] = None
        try:
            context['weeklyCourseContents'] = Weekly_course_contents.objects.filter(course_id=context['pk'])
        except:
            context['weeklyCourseContents'] = None
        try:
            temp = []
            temp.append(Course.objects.get(id=context['pk']).title)
            temp.append(Course.objects.get(id=context['pk']).author)
            temp.append(Course.objects.get(id=context['pk']).publisher)
            temp.append(Course.objects.get(id=context['pk']).year_of_publication)
            context['books'] = temp
        except:
            context['books'] = None

        subjectName = Course.objects.get(id=context['pk']).subjectName
        context['cnt'] = self.get_gradelist(subjectName)
        return context


    # 학번을 가진 학생의 이수한 학기 리스트를 가져옴
    def get_semesterlist(self, hukbun):
        semesterlist = []
        temp = StudentGrade.objects.filter(hukbun=hukbun).filter(valid='유효').values_list('yearNsemester', flat=True).order_by('yearNsemester').distinct()
        for i in range(0, temp.count()):
            semesterlist.append(temp[i])
        return semesterlist

    # 인덱스를 넣으면 학년을 리턴함
    def get_year(self, idx):
        if (idx == 7) or (idx == 6):
            return 4
        elif (idx == 5) or (idx == 4):
            return 3
        elif (idx == 3) or (idx == 2):
            return 2
        elif (idx == 1) or (idx == 0):
            return 1
        else:
            return 0

    def check_year(self, yearNsemester, semesterlist):
        idx = semesterlist.index(yearNsemester)

        return idx
    # 학번을 가진 학생의 이수한 학기 리스트를 가져옴
    # 과목 코스의 pk를 가지고 과목 이름을 리턴
    # 그 과목이름을 가진 그레이드 객체들을 리스트에 넣는다.
    # 그 성적 리스트에서 학번들만 가져와서 그 학번들이 몇학년인지 알아내어 딕셔너리에 {성적객체, 학년} 으로 추가 한다.
    # 딕셔너리를 학년별로 정렬한다.(오름차순)
    # 딕셔너리에 있는 학년별로 성적 객체의 수를 카운트한다.
    # 리스트 2개를 반환한다. [1학년, 2학년, ..,], [cnt1, cnt2, ...]
    def get_gradelist(self, subjectName):
        gradelist = []
        cnt = [0,0,0,0]
        dic = {}

        temp = StudentGrade.objects.filter(subject=subjectName)
        for i in range(0, temp.count()):
            gradelist.append(temp[i]) # 같은 과목이름을 가진 StudentGrade객체들을 리스트에 넣는다.

        print(gradelist)
        for i in range(0, len(gradelist)):
            semesterlist = self.get_semesterlist(gradelist[i].hukbun)
            idx = self.check_year(gradelist[i].yearNsemester, semesterlist)
            year = self.get_year(idx)
            dic[gradelist[i]] = year

        print("dic", end="")
        print(dic)
        dic = sorted(dic.items(), key=operator.itemgetter(1))
        print(dic)

        for object in dic:
            if object[1] == 1:
                cnt[0] = cnt[0] + 1
            elif object[1] == 2:
                cnt[1] = cnt[1] + 1
            elif object[1] == 3:
                cnt[2] = cnt[2] + 1
            elif object[1] == 4:
                cnt[3] = cnt[3] + 1
            else:
                continue

        print("cnt",end="")
        print(cnt)

        return cnt

class SpecialCourseRecommandView(LoginRequiredMixin, TemplateView):
    template_name = "classes/special_recommand.html"

    def get_context_data(self, **kwargs):
        context = super(SpecialCourseRecommandView, self).get_context_data(**kwargs)
        student = StudentInfo.objects.get(hukbun=self.request.user.hukbun)

        context['specialCoursesDic'] = self.getSpecialCase()
        return context

    def getSpecialCase(self):  # 자신의 학년과 맞지 않게 다른 학년의 수업을 들은 경우를 보여줌
        specialCoursesDic = dict()

        for student in StudentInfo.objects.all():  # 모든 학생
            studentGrades = StudentGrade.objects.filter(hukbun=student.hukbun)  # 학생의 grade 쿼리셋
            semesterList = studentGrades.values_list('yearNsemester', flat=True)  # 학생의 학기 list
            semesterList = sorted(list(set(semesterList)))  # 중복제거하여 정렬
            retakeList = [] #재수강한 과목들 -> 이 과목은 무시하자
            for grade in studentGrades:  # 학생이 과목을 들었을 때 학년이 일치하는 지 확인한다.
                if grade.valid == '재수강무효' or grade.valid == 'F학점일괄무효' or grade.subject in retakeList: #해당 과목이 재수강과목이라면 무시
                    retakeList.append(grade.subject)
                    continue
                semester = semesterList.index(grade.yearNsemester)  # 해당 과목의 학기가 semesterList에서 검색해 index를 반환한다 => 해당 과목이 몇학기에 들은 과목인가 검사
                courses = Course.objects.filter(year__in=[datetime.today().year-1, datetime.today().year], subjectName=grade.subject)  # 해당 수업의 이름과 동일한 course 쿼리셋 가져오기
                if courses.count() == 0:  # 만약 해당하는 수업이 없다면 걍 무시
                    continue
                courseInfoes = []
                course = courses.last() #수업을 대충 하나 가져와서 추천 학년을 저장
                courseGrade = course.grade  #해당 수업의 추천 학년 가져옴
                if int(semester / 2) + 1 != int(courseGrade):  # 추천 학년대로 과목을 안 들었을 경우
                    courseInfoes.append(course.grade)  # 추천 학년
                    courseInfoes.append(int(semester / 2) + 1)  # 들었던 학년
                    courseInfoes.append(course.eisu)  # 이수
                    courseInfoes.append(course.score)  # 학점
                    specialCoursesDic[grade] = courseInfoes

        # 이제 중복된 전공을 없애고 카운트하는게 필요
        grades = list(specialCoursesDic.keys())  # grade 객체 리스트
        gradesSubjectName = []
        resultDic = specialCoursesDic.copy()
        for grade in grades:  # grades := grades의 과목 이름 리스트
            gradesSubjectName.append(grade.subject)
        notDuplicatedGrades = list(set(gradesSubjectName))
        for notDuplicatedGrade in notDuplicatedGrades:
            count = 0
            for grade in specialCoursesDic.keys():
                if notDuplicatedGrade == grade.subject:
                    if count > 0:
                        del resultDic[grade]
                    count += 1
            grades = list(resultDic.keys())  # grade 객체 리스트
            for grade in grades:
                if grade.subject == notDuplicatedGrade:
                    resultDic[grade].append(count)

        return resultDic

class TopStudentRecommandView(LoginRequiredMixin, TemplateView):
    template_name = "classes/topStudent_recommand.html"

    def get_context_data(self, **kwargs):
        context = super(TopStudentRecommandView, self).get_context_data(**kwargs)
        student = StudentInfo.objects.get(hukbun=self.request.user.hukbun)
        top5Info = self.getTop5Grades(student)
        scoreList = []
        top5GradesList = []
        for info in top5Info:
            infoList = [info[0], info[1]]
            scoreList.append(infoList)
            top5GradesList.append(info[2])

        context['Top5GradesList'] = top5GradesList
        context['ScoreList'] = scoreList

        dicList = []
        for topGrade in  context['Top5GradesList']:
            semesterList = topGrade.values_list('yearNsemester', flat=True)
            semesterList = sorted(list(set(semesterList)))
            semesterGradeDic = dict()
            for semester in semesterList:
                semesterCount = semesterList.index(semester) + 1
                if (semesterCount % 2 == 1):  # 홀수라면
                    grade = str(int((semesterCount + 1) / 2)) + "학년 1학기"
                else:  # 짝수일 경우
                    grade = str(int((semesterCount + 1) / 2)) + "학년 2학기"

                semesterGradeDic[semester] = grade
            dicList.append(semesterGradeDic)
        context['dicList'] = dicList

        return context

    def getTop5Grades(self, student):
        gradeList = ['1학년 1학기','1학년 2학기','2학년 1학기','2학년 2학기','3학년 1학기','3학년 2학기','4학년 1학기','4학년 2학기']
        try:
            studentCurrentGradeList = gradeList[gradeList.index(student.currentGrade) + 1:]
        except:
            return None
        upperGradeStudentHukbun = StudentInfo.objects.filter(currentGrade__in=studentCurrentGradeList).values_list('hukbun')
        upperStudentGrades = StudentGrade.objects.filter(hukbun__in=upperGradeStudentHukbun).values_list('hukbun', flat=True)

        upperStudentScoreDic = dict() #선배 학생의 총점을 저장할 dic
        for hukbun in upperGradeStudentHukbun: #각 학생의 총점 저장
            upperStudentScoreDic[hukbun] = get_avgGrade(hukbun)  # 학번 : 총점
        sortedUpperStudentScoreList = sorted(upperStudentScoreDic.items(), key = operator.itemgetter(1), reverse=True) #value를 기준으로 내림차순 정렬
        topStudentGradesScoreDic = dict()
        resultList = []
        rank = 1
        for topStudent in sortedUpperStudentScoreList[:5]: #top 5학생의 [학번,총점]을 가져옴
            studentValueList = []
            studentValueList.append(rank) #등수
            studentValueList.append(topStudent[1]) #총점
            studentValueList.append(StudentGrade.objects.filter(hukbun=topStudent[0]).order_by('yearNsemester', 'subject'))
            rank += 1
            resultList.append(studentValueList)

        return resultList

class RetakeRecommandView(LoginRequiredMixin, TemplateView):
    template_name = "classes/retaking_recommand.html"
    """
    1. 내가 들을 수 있는 아직 듣지 않은 전공 수업들 보여줌
    2. 제일 잘 나가는 타 학생의 전공 수업들을 보여줌
    3. 재수강 추천 과목을 보여줌 (낮은 성적부터)
    """

    def get_context_data(self, **kwargs):
        context = super(RetakeRecommandView, self).get_context_data(**kwargs)
        student = StudentInfo.objects.get(hukbun=self.request.user.hukbun)
        takenCoursesGrades = StudentGrade.objects.filter(hukbun=student.hukbun)
        # self.getRetakeCourses(student,dent) takenCoursesGrades)
        context['retakeGrades'] = self.getRetakeCourses(student, takenCoursesGrades)
        context['retakeGradesCountList'] = self.topRetakeCourses()
        context['retakeCourceTopTen'] = self.getTopTeReTakeCourse()

        return context

    def topRetakeCourses(self):
        allRetakeGrades = StudentGrade.objects.filter(valid='재수강무효').order_by('yearNsemester', 'subject')
        allRetakeGradesNameList = allRetakeGrades.values_list('subject', flat=True).distinct()
        retakeGradesNameCountDic = dict()

        for retakeCourseName in allRetakeGradesNameList:
            retakeGradesNameCountDic[retakeCourseName] = 0  # count
        for retakeGrade in allRetakeGrades:
            retakeGradesNameCountDic[retakeGrade.subject] += 1 #재수강인거 count해주자
        retakeGradesCountList = sorted(retakeGradesNameCountDic.items(), key = operator.itemgetter(1))

        return retakeGradesCountList


    def disapprovalCourses(self, student):
        studentGrade = int(student.currentGrade[0])
        studentSemester = int(student.currentGrade[-3])
        if studentGrade < 3:
            return None
        gradeYearNSemesters = StudentGrade.objects.filter(hukbun=student.hukbun).values_list('yearNsemester')
        gradeYearNSemesters = sorted(list(set(gradeYearNSemesters)))
        studentYearNSemesterLen = (studentGrade - 1) * 2 + studentSemester

        resultQuerySetList = []
        for semester in range(1, studentYearNSemesterLen-4):
            resultQuerySetList.append(
                StudentGrade.objects.filter(hukbun=student.hukbun, yearNsemester__in=gradeYearNSemesters[semester - 1]))

        resultQuerySet = StudentGrade.objects.none()
        for gradeQuerySet in resultQuerySetList:
            resultQuerySet = resultQuerySet | gradeQuerySet

        return resultQuerySet

    def getRetakeCourses(self, student, takenCoursesGrades):
        takenCoursesScoresDic = dict()
        retakeCoursesName = []
        canceledList = []
        for takenCourseGrade in takenCoursesGrades:  # 딕셔너리에 과목코드:(int)점수 저장
            try:
                if getIntScore(takenCourseGrade.grade) <= 3.0:  # 2.5
                    takenCoursesScoresDic[takenCourseGrade.subject] = getIntScore(takenCourseGrade.grade)
            except:
                continue

        sortedTakenCoursesScoresList = sorted(takenCoursesScoresDic.items(), key=lambda x: x[1]) #정렬
        for sortedTakenCoursesScores in sortedTakenCoursesScoresList:
            retakeCoursesName.append(sortedTakenCoursesScores[0])

        resultGrades = StudentGrade.objects.filter(subject__in=retakeCoursesName,
                                                   hukbun=student.hukbun)  # 재수강 추천 과목 쿼리셋을 리턴
        if resultGrades.count() == 0:
            return None
        for resultGrade in resultGrades:
            differenceList  = []
            try:
                if getIntScore(resultGrade.grade) >= 2.5:
                    differenceList.append(resultGrades.filter(subject=resultGrade.subject))
            except:
                continue
        canceledList = resultGrades.filter(Q(valid='재수강무효') | Q(grade='P')).values_list('subject')
        for differenceGrade in differenceList:
            resultGrades.difference(differenceGrade)
        try:
            resultGrades =  resultGrades.difference(resultGrades.filter(valid='재수강무효')).difference(
                resultGrades.filter(subject__in=canceledList)).difference(self.disapprovalCourses(student))
        except:
            return None

        return resultGrades.order_by('-grade', 'yearNsemester', 'subject')

    def getTopTeReTakeCourse(self):
        # Members.objects.order_by('disignation').values('designation').annotate(dcount=Count('designation'))
        gradelist = StudentGrade.objects.filter(valid='재수강무효').order_by('subject').values('subject').annotate(cnt=Count('subject'))
        temp = []
        list_subject = []
        grade = []
        dic = {}

        print(gradelist)
        for i in range(0, gradelist.count()):
            temp.append(gradelist[i])

        print(temp)
        for i in range(0, len(temp)):
            valuelist = list(temp[i].values())
            dic[valuelist[0]] = valuelist[1]
        dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
        print(dic)
        dic = dic[:5]

        return dic

class preCourseRecommandView(LoginRequiredMixin, TemplateView):
    template_name = "classes/pre_recommand.html"
    scoreList = []
    def get_context_data(self, **kwargs):
        context = super(preCourseRecommandView, self).get_context_data(**kwargs)
        context['necessaryGrades'] = self.getNecessrayGrades()
        context['promotedGrades'] = self.getPromotedGrades()

        return context

    def getNecessrayGrades(self): #선수 과목
        student = self.request.user #현재 로그인된 학생
        takenGrades = StudentGrade.objects.filter(hukbun=student.hukbun).values_list('subject', flat=True).distinct()
        allCourseList = Course.objects.filter(year__in=[datetime.today().year-1, datetime.today().year], semester__in=[10, 20]).values_list('subjectName', flat=True).distinct()
        notTakenGrades = list(set(allCourseList) - set(takenGrades))
        necessaryCourses = necessaryCourse.objects.filter(parentCourse__subjectName__in = notTakenGrades) #내가 듣지 않은 전공들의 선수과목 쿼리셋

        childList = []
        scoreList = []
        returnList = []
        studentList = []
        for nCourse in necessaryCourses:
            subjectName = nCourse.parentCourse.subjectName
            if subjectName in studentList:
                continue
            studentList.append(subjectName)

            childList = necessaryCourse.objects.filter(parentCourse__subjectName=subjectName).values_list('childCourse__subjectName', flat=True).distinct()
            scoreList = StudentGrade.objects.filter(hukbun=student.hukbun, subject__in=childList).values_list('grade', flat=True).distinct()

            returnList.append([subjectName, childList, scoreList])

        return returnList

        # currentSemester = len((list(set(StudentGrade.objects.all().values_list('yearNsemester'))))) #학생이 현재까지 들은 학기
        # if(currentSemester%2 == 1): #홀수라면
        #     nextGrade = (currentSemester+1)/2
        # else: #짝수일 경우
        #     nextGrade = currentSemester/2 + 1
        # recommendedCoursesNameList = Course.objects.filter(grade=nextGrade).values_list('subjectName') #해당 학년에 해당하는 추천 course 이름 리스트를 가져옴
        # recommendedCoursesNameList = list(set(recommendedCoursesNameList)) #중복제거
        # necessrayCourses = necessaryCourse.objects.filter(childCourse__in=recommendedCoursesNameList)
        # necessaryCourseNameList = []
        # for necessaryCourse1 in necessrayCourses:
        #     if necessaryCourse1.childCourse.subjectName in recommendedCoursesNameList:
        #         necessaryCourseNameList.append(necessaryCourse1.childCourse.subjectName)

        #return StudentGrade.objects.filter(subject__in=necessaryCourseNameList).order_by('yearNsemester', 'subject')

    def getPromotedGrades(self): #권장 과목
        student = self.request.user  # 현재 로그인된 학생
        takenGrades = StudentGrade.objects.filter(hukbun=student.hukbun).values_list('subject', flat=True).distinct()
        allCourseList = Course.objects.filter(year__in=[datetime.today().year - 1, datetime.today().year],
                                              semester__in=[10, 20]).values_list('subjectName', flat=True).distinct()
        notTakenGrades = list(set(allCourseList) - set(takenGrades))
        promotedCourses = promotedCourse.objects.filter(
            parentCourse__subjectName__in=notTakenGrades)  # 내가 듣지 않은 전공들의 선수과목 쿼리셋

        childList = []
        scoreList = []
        returnList = []
        studentList = []
        for pCourse in promotedCourses:
            subjectName = pCourse.parentCourse.subjectName
            if subjectName in studentList:
                continue
            studentList.append(subjectName)

            childList = promotedCourse.objects.filter(parentCourse__subjectName=subjectName).values_list(
                'childCourse__subjectName', flat=True).distinct()
            scoreList = StudentGrade.objects.filter(hukbun=student.hukbun, subject__in=childList).values_list('grade',
                                                                                                              flat=True).distinct()

            returnList.append([subjectName, childList, scoreList])

        return returnList
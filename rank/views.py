from django.shortcuts import render
from django.views.generic import ListView
from dataParser.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import operator



# Create your views here.

def getIntScore(score):
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
        return 0.0
    elif score == 'P':
        return 0.0
    else:
        return None


semester_list = ['1학년 1학기', '1학년 2학기', '2학년 1학기', '2학년 2학기', '3학년 1학기', '3학년 2학기', '4학년 1학기', '4학년 2학기']


class Rank_One(LoginRequiredMixin,ListView):
    # 구현 방식
    # 학기 리스트를 만든다.
    # 학기별로 사용자들의 리스트를 만든다.
    # 학기(사용자들, 각각의 성적), 학기 : dic, 사용자:StudentInfo 객체, 성적: get_gradeAvg리턴값)
    # 학기객체 리턴

    model = StudentGrade
    template_name = 'rank/rank1.html'
    # context_object_name = 'rank_grade_list'

    # 현재 1학년인 사용자들의 리스트를 반환한다.
    def get_queryset(self):
        return StudentInfo.objects.filter(Q(currentGrade='1학년 1학기') | Q(currentGrade='1학년 2학기'))

    # 학번을 입력하면 평점 산출 학점을 반환한다.
    def get_score_sum(self, s):
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
        scorelist = scorelist.exclude(grade__contains='P').values_list('score', flat=True)
        print(scorelist)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    # 학번을 입력하면 평점을 반환한다.
    def get_avgGrade(self, s):
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D'))

        for i in range(0, gradelist.count()):
            print(gradelist[i].subject+","+gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            print(temp)
            sum = sum + temp
        score_sum = self.get_score_sum(s)
        print("score_sum:%d" % score_sum)
        avg = sum/score_sum
        return avg

    def get_user_sort_list(self):
        user_grade_list = {}
        user_list = []
        user_sort = {}

        user_list = self.get_queryset()
        for i in range(0, user_list.count()):
            user_grade_list[user_list[i]] = self.get_avgGrade(user_list[i].hukbun)

        # sortedArr = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        user_sort = sorted(user_grade_list.items(), key=operator.itemgetter(1), reverse=True)

        return user_sort

    # key : 사용자 객체 , value : 사용자의 평점 return: dic(사용자들, 성적들)
    def get_context_data(self, **kwargs):
        context = super(Rank_One, self).get_context_data(**kwargs)
        context['user_grade'] = self.get_user_sort_list()

        return context


class Rank_Two(LoginRequiredMixin, ListView):
    model = StudentGrade
    template_name = 'rank/rank2.html'

    # 현재 2학년인 사용자들의 리스트를 반환한다.
    def get_queryset(self):
        return StudentInfo.objects.filter(Q(currentGrade='2학년 1학기') | Q(currentGrade='2학년 2학기'))

    # 학번을 입력하면 평점 산출 학점을 반환한다.
    def get_score_sum(self, s):
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
        scorelist = scorelist.exclude(grade__contains='P').values_list('score', flat=True)
        print(scorelist)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    # 학번을 입력하면 평점을 반환한다.
    def get_avgGrade(self,s):
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(grade='D'))
        print(gradelist)
        for i in range(0, gradelist.count()):
            print(gradelist[i].subject + "," + gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            print(temp)
            sum = sum + temp
        score_sum = self.get_score_sum(s)
        print(score_sum)
        avg = sum / score_sum
        return avg

    def get_user_sort_list(self):
        user_grade_list = {}
        user_list = []
        user_sort = {}
        user_list = self.get_queryset()
        for i in range(0, user_list.count()):
            user_grade_list[user_list[i]] = self.get_avgGrade(user_list[i].hukbun)

        # sortedArr = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        user_grade_list = sorted(user_grade_list.items(), key=operator.itemgetter(1), reverse=True)

        return user_grade_list

    # key : 사용자 객체 , value : 사용자의 평점 return: dic(사용자들, 성적들)
    def get_context_data(self, **kwargs):
        context = super(Rank_Two, self).get_context_data(**kwargs)
        context['user_grade'] = self.get_user_sort_list()

        return context


class Rank_Three(LoginRequiredMixin, ListView):
    model = StudentGrade
    template_name = 'rank/rank3.html'
    # context_object_name = 'rank_grade_list'

    # 현재 1학년인 사용자들의 리스트를 반환한다.
    def get_queryset(self):
        return StudentInfo.objects.filter(Q(currentGrade='3학년 1학기') | Q(currentGrade='3학년 2학기'))

    # 학번을 입력하면 평점 산출 학점을 반환한다.
    def get_score_sum(self, s):
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
        scorelist = scorelist.exclude(grade__contains='P').values_list('score', flat=True)
        print(scorelist)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    # 학번을 입력하면 평점을 반환한다.
    def get_avgGrade(self, s):
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(grade='D'))
        print(gradelist)
        for i in range(0, gradelist.count()):
            print(gradelist[i].subject + "," + gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            print(temp)
            sum = sum + temp
        score_sum = self.get_score_sum(s)
        print(score_sum)
        avg = sum / score_sum
        return avg

    def get_user_sort_list(self):
        user_grade_list = {}
        user_list = []
        user_sort = {}
        user_list = self.get_queryset()
        for i in range(0, user_list.count()):
            user_grade_list[user_list[i]] = self.get_avgGrade(user_list[i].hukbun)

        # sortedArr = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        user_sort = sorted(user_grade_list.items(), key=operator.itemgetter(1), reverse=True)

        return user_sort

    # key : 사용자 객체 , value : 사용자의 평점 return: dic(사용자들, 성적들)
    def get_context_data(self, **kwargs):
        context = super(Rank_Three, self).get_context_data(**kwargs)
        context['user_grade'] = self.get_user_sort_list()

        return context


class Rank_Four(LoginRequiredMixin, ListView):
    model = StudentGrade
    template_name = 'rank/rank4.html'
    # context_object_name = 'rank_grade_list'

    # 현재 1학년인 사용자들의 리스트를 반환한다.
    def get_queryset(self):
        return StudentInfo.objects.filter(Q(currentGrade='4학년 1학기') | Q(currentGrade='4학년 2학기'))

    # 학번을 입력하면 평점 산출 학점을 반환한다.
    def get_score_sum(self, s):
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
        scorelist = scorelist.exclude(grade__contains='P').values_list('score', flat=True)
        print(scorelist)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    # 학번을 입력하면 평점을 반환한다.
    def get_avgGrade(self, s):
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(grade='D'))
        print(gradelist)
        for i in range(0, gradelist.count()):
            print(gradelist[i].subject + "," + gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            print(temp)
            sum = sum + temp
        score_sum = self.get_score_sum(s)
        print(score_sum)
        avg = sum / score_sum
        return avg

    # 학번을 입력하면 전공 학점을 반환한다.
    def major_gradelist(self):
        s = self.request.user.hukbun
        return  StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(
        valid='유효').filter(
        Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
            grade='D+') | Q(
            grade='D') | Q(grade='F')).values_list('grade', flat=True)

    # 학번을 입력하면 msc학점을 반환한다.
    def msc_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자')|Q(eisu='수리')).filter(
        Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
            grade='D+') | Q(
            grade='D') | Q(grade='F')).values_list('grade', flat=True)


    # key : 사용자 객체 , value : 사용자의 평점 return: dic(사용자들, 성적들)
    def get_user_sort_list(self):
        user_grade_list = {}
        user_list = []
        user_sort = {}
        user_list = self.get_queryset()
        for i in range(0, user_list.count()):
            user_grade_list[user_list[i]] = self.get_avgGrade(user_list[i].hukbun)

        # sortedArr = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        user_sort = sorted(user_grade_list.items(), key=operator.itemgetter(1), reverse=True)

        return user_sort

    def get_context_data(self, **kwargs):
        context = super(Rank_Four, self).get_context_data(**kwargs)
        context['user_grade'] = self.get_user_sort_list()

        return context
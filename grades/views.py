from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *
from dataParser.models import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  get_object_or_404
from django.db.models import Sum
import requests
from dataParser import parser
# Create your views here.


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
        return 0.0
    else:
        return None


class GradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/grades_list.html'
    context_object_name = 'grades_list'

    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid = '유효').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + i

        return sum


    def get_avgGrade(self):
        s = self.request.user.hukbun
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid = '유효').filter(Q(grade='A+') | Q(grade='A') | Q(grade='B+') |Q(grade='B') |Q(grade='C+') |Q(grade='C') |Q(grade='D+') |Q(grade='D') |Q(grade='F')).values_list('grade', flat=True)
        count = len(gradelist)
        for g in gradelist:
            s = getIntScore(self, g)
            if s == None:
                continue
            else:
                sum = sum + s
        avg = sum/count
        return avg

    def get_queryset(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s)

    def get_fake_grade_sum(self):
        s = self.request.user.hukbun
        fake_grade_sum = StudentGrade.objects.filter(hukbun=s).values_list('score', flat=True)
        sum = 0
        for i in fake_grade_sum:
            sum = sum + i

        return sum

    def get_context_data(self,**kwargs):
        context = super(GradeLV, self).get_context_data(**kwargs)
        context['grade_list'] = self.get_queryset()
        context['grade_sum'] = self.get_score_sum()
        context['avgGrade'] = self.get_avgGrade()
        context['fake_grade_sum'] = self.get_fake_grade_sum()
        return context


class MajorGradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/major_subject_list.html'
    context_object_name = 'major_list'


    def get_queryset(self):
        # 학번과 이수로 filter를 사용해서 리스트를 가져와야 한다.
        test = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=test).filter(Q(eisu='컴과') | Q(eisu='전필'))


class GeGradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/ge_subject_list.html'
    context_object_name = 'ge_list'

    def get_queryset(self):
        test = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=test).filter(Q(eisu='M자') | Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회'))
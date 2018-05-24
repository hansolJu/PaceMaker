from django.shortcuts import render
from django.views.generic import *
from dataParser.models import *
from django.db.models import Q
import requests
from dataParser import parser
# Create your views here.


class GradeLV(ListView):
    model = StudentGrade
    template_name = 'grades/grades_list.html'
    context_object_name = 'grades_list'

    def get_queryset(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s)


class MajorGradeLV(ListView):
    model = StudentGrade
    template_name = 'grades/major_subject_list.html'
    context_object_name = 'major_list'

    def get_queryset(self):
        # 학번과 이수로 filter를 사용해서 리스트를 가져와야 한다.
        test = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=test).filter(Q(eisu='컴과') | Q(eisu='전필'))


class GeGradeLV(ListView):
    model = StudentGrade
    template_name = 'grades/ge_subject_list.html'
    context_object_name = 'ge_list'

    def get_queryset(self):
        test = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=test).filter(Q(eisu='M자') | Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회'))
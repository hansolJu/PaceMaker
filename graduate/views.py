from django.views.generic import *
from dataParser.models import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class GraduateLV(LoginRequiredMixin, ListView):
    model = StudentGrade
    template_name = 'graduate/graduate_confirm.html'

    # 전체 학점
    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
        scorelist = scorelist.values_list('score', flat=True)
        print(scorelist)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # 설계 학점
    def get_design_grade_sum(self):
        s = self.request.user.hukbun
        design_gradelist = StudentGrade.objects.filter(hukbun=s).values_list('grade_design', flat=True)
        sum = 0.0
        for i in design_gradelist:
            sum = sum + float(i)


        return sum

    # 전공 학점
    def get_major_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(valid = '유효').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # 교양 학점
    def get_ge_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자') | Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회') |Q(eisu='과기')|Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') | Q(eisu='언문')).filter(valid = '유효').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # MSC 학점
    def get_msc_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(eisu='M자').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # 공학 인증 교양 학점
    def get_eg_ge_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(subject='창의적문제해결전략')|Q(subject='특허와기술개발')|Q(subject='공학윤리')|Q(subject='인간심리의이해')).values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    def get_context_data(self,**kwargs):
        context = super(GraduateLV, self).get_context_data(**kwargs)
        context['total_grade'] = self.get_score_sum()
        context['design_grade'] = self.get_design_grade_sum()
        context['major_grade'] = self.get_major_score_sum()
        context['ge_grade'] = self.get_ge_score_sum()
        context['msc_grade'] = self.get_msc_score_sum()
        context['engineer_cer_ge_grade'] = self.get_eg_ge_score_sum()
        return context
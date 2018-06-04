from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.base import TemplateView

# login_required()함수는 데코레이터로 사용되는 함수로, 일반 함수에 적용
# 사용자가 로그인 했는지를 확인해 로그인한 경우는 원래 함수로 실행하고, 로그인 되지 않은 경우는 로그인 페이지로 리다이렉트.
from dataParser.models import StudentGrade


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


#--- TemplateView
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    def ge_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(
        Q(eisu='M자') | Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회')).filter(
        valid='유효').filter(
        Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
            grade='D+') | Q(
            grade='D') | Q(grade='F')).values_list('grade', flat=True)


    def major_gradelist(self):
        s = self.request.user.hukbun
        return  StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(
        valid='유효').filter(
        Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
            grade='D+') | Q(
            grade='D') | Q(grade='F')).values_list('grade', flat=True)


    def msc_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자')|Q(eisu='수리')).filter(
        Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
            grade='D+') | Q(
            grade='D') | Q(grade='F')).values_list('grade', flat=True)

    def get_avgGrade(self,gradelist):
        avg = 0.0
        sum = 0.0
        count = len(gradelist)
        for g in gradelist:
            s = getIntScore(self, g)
            if s == None:
                continue
            else:
                sum = sum + s
        print(count)
        avg = sum/count
        return avg

    def Make_chart_data(self):
        # 전공 교양 msc 성장률
        result = []
        #전공
        result.append(self.get_avgGrade(self.major_gradelist()))
        # 교양
        result.append(self.get_avgGrade(self.ge_gradelist()))
        # msc
        result.append(self.get_avgGrade(self.msc_gradelist()))
        # 성장률
        ''' (2016년2학기−2016년2학기 직전학기)/(4.5−2016년2학기 직전학기)'''
        tmp = 3.0
        result.append(tmp)
        print(result)
        return result


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['chart_data'] =  self.Make_chart_data()
        return context

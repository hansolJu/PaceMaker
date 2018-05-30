from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# login_required()함수는 데코레이터로 사용되는 함수로, 일반 함수에 적용
# 사용자가 로그인 했는지를 확인해 로그인한 경우는 원래 함수로 실행하고, 로그인 되지 않은 경우는 로그인 페이지로 리다이렉트.
from django.contrib.auth.decorators import login_required


#--- TemplateView
class HomeView(TemplateView, LoginRequiredMixin):
    template_name = 'index.html'

    def Make_chart_data(self):
        # 전공 교양 msc 성장률
        result = []
        #전공
        from grades.views import MajorGradeLV
        major = MajorGradeLV()
        result.append(major.get_avgGrade())
        # 교양
        from grades.views import GeGradeLV
        msc = GeGradeLV()
        result.append("3")
        # msc
        result.append("")
        # 성장률
        ''' (2016년2학기−2016년2학기 직전학기)/(4.5−2016년2학기 직전학기)'''
        



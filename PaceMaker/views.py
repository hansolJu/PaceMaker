from django.views.generic.base import TemplateView

# login_required()함수는 데코레이터로 사용되는 함수로, 일반 함수에 적용
# 사용자가 로그인 했는지를 확인해 로그인한 경우는 원래 함수로 실행하고, 로그인 되지 않은 경우는 로그인 페이지로 리다이렉트.
from django.contrib.auth.decorators import login_required


#--- TemplateView
class HomeView(TemplateView):
    template_name = 'index.html'
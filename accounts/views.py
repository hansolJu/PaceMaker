from django.http import HttpResponse
from django.shortcuts import render, redirect

from dataParser.models import StudentInfo
from dataParser.parser import *
from .forms import LoginForm, AgreeForm
from .my_auth import *


def agree(request):
    if request.method == 'POST':
        agreeDataUsing = request.POST.get('agreeDataUsing')
        if agreeDataUsing:
            form = LoginForm()
            # TO-DO : 동의성공 창 띄우기
            # TO-DO : 디비에 데이터 저장하기
            return redirect('accounts:login')
    else:
        form = AgreeForm()
        return render(request, 'agree.html', {'form': form})


def login(request):
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)

        # 유효성 검증에 성공할 경우
        # form으로부터 username, password값을 가져옴
        hukbun = request.POST.get('hukbun', '')
        print(hukbun)
        password = request.POST['password']
        print(password)

        # parser = KutisParser()
        # kutis_login_success = parser.login(hukbun, password)  # 쿠티스 로그인 시도
        #
        # if kutis_login_success:  # 쿠티스 로그인에 성공했다면
        #     user = UserBackend.authenticate(hukbun=hukbun)  # 장고 custom auth
        #
        #     if not user: # 모든 로그인 성공('user'변수안에 내용이 존재하지 않으면 None임)
        #         return render(request, 'index.html', {})
        #     # 첫 사용자
        #     else:
        #         passingdata = parser.parse_item(parser.studentgradeUrl)
        #         parser.save_info("201511868", passingdata)
        #         agree(request)
        # else:
        #     return redirect('accounts:login')
            #HttpResponse('로그인 실패. 학번과 비밀번호를 확인해주세요.')  # TO DO : 창 띄우기
        # test = StudentParser()
        # test.login(hukbun,password)
        # test.save_info(hukbun,test.parse_info())

        kutisLog = UserBackend()
        kutisLog.authenticate(hukbun,password)

    else:
        form = LoginForm()
        return render(request, 'loginTest.html', {'form': form})

    # def logout(request):
    # django_logout(request)
    # return redirect('accounts:login')

    def get_queryset(self):
        return StudentInfo.objects.all()
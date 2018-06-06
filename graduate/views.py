from django.views.generic import *
from dataParser.models import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


eisu_2012_list = [
    # 1-1 1
    ['창의기초설계', '컴퓨터과학전공및진로탐색'],
    # 1-2 2
    ['C프로그래밍'],
    # 2-1 3
    ['컴퓨터구조', '자료구조론', '자바프로그래밍1', '이산수학', '수치계산'],
    # 2-2 4
    ['컴퓨터네트워크', '시스템소프트웨어', '계산이론', '자료구조설계', '자바프로그래밍2'],
    # 3-1 5
    ['프로그래밍언어론', '운영체제', '네트워크프로그래밍', '데이터베이스', '컴퓨터교육론', '워크플로우관리시스템'],
    # 3-2 6
    ['인공지능', '소프트웨어공학', '컴퓨터그래픽스', '웹서비스설계', '분산및병렬처리', '소프트웨어공학'],
    # 4-1 7
    ['컴퓨터보안', '알고리듬', '캡스톤설계'],
    # 4-2 8
    ['컴퓨터과학특강', '컴파일러', '데이터베이스응용', '내장형시스템']
]
eisu_2012_list_check = ['창의기초설계', '컴퓨터과학전공및진로탐색','C프로그래밍','컴퓨터구조', '자료구조론', '자바프로그래밍1', '이산수학', '수치계산'
                  ,'컴퓨터네트워크', '시스템소프트웨어', '계산이론', '자료구조설계', '자바프로그래밍2',
                  '프로그래밍언어론', '운영체제', '네트워크프로그래밍', '데이터베이스', '컴퓨터교육론', '워크플로우관리시스템',
                  '인공지능', '소프트웨어공학', '컴퓨터그래픽스', '웹서비스설계', '컴퓨터교재연구지도법', '분산및병렬처리', '소프트웨어공학',
                  '컴퓨터보안', '알고리듬', '캡스톤설계','컴퓨터과학특강', '컴파일러', '데이터베이스응용', '종합설계', '내장형시스템']


class GraduateLV(LoginRequiredMixin, ListView):
    model = StudentGrade
    template_name = 'graduate/graduate_confirm.html'

    # 전체 학점
    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').exclude(grade__contains='F')
        scorelist = scorelist.values_list('score', flat=True)
        print(scorelist)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # 설계 학점
    def get_design_grade_sum(self):
        s = self.request.user.hukbun
        design_gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').exclude(grade__contains='F').values_list('grade_design', flat=True)
        sum = 0.0
        for i in design_gradelist:
            sum = sum + float(i)


        return sum

    # 전공 학점
    def get_major_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(valid = '유효').exclude(grade__contains='F').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # 교양 학점
    def get_ge_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(
            valid='유효').filter(Q(eisu='M자') | Q(eisu='수리') | Q(eisu='필수') |Q(eisu='언문')|Q(eisu='진') |Q(eisu='창융')|Q(eisu='체육')|Q(eisu='취봉') |Q(eisu='예술') |Q(eisu='인문') | Q(eisu='이계')|Q(eisu='사고') | Q(eisu='역철')| Q(eisu='문화') | Q(eisu='경사')
                | Q(eisu='체기') | Q(eisu='사회') |Q(eisu='과기')| Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') |
                    Q(eisu='문예') | Q(eisu='언문')).exclude(grade__contains='F').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # MSC 학점
    def get_msc_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자')|Q(eisu='수리')|Q(eisu='이계')).filter(valid='유효').exclude(grade__contains='F').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)


        return sum

    # 공학 인증 교양 학점
    def get_eg_ge_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(subject='창의적문제해결전략')|Q(subject='특허와기술개발')|Q(subject='공학윤리')|Q(subject='인간심리의이해')).exclude(grade__contains='F').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    # 0. 이수한 학기 리스트를 가져옴
    # 1. 학기별로 들은 전공 과목을 가져옴 : [[grade, grade], [grade, grade], ...]
    # 2. 학기별로 들은 과목을 리턴하면 이수체계도에 맞는 학년/학기를 찾아서 듣지 않는 과목 리스트를 리턴한다. [[듣지않은과목, 듣지않은과목](학기), ....]
    # 3. 과목리스트를 context객체에 담아서 리턴한다.

    # 0. 이수한 학기 리스트를 가져온다.
    def get_semesterlist(self):
        s = self.request.user.hukbun
        semesterlist = StudentGrade.objects.filter(
            hukbun=s).values_list('yearNsemester',flat=True).distinct().order_by('yearNsemester')

        print("semesterlist:", end="")
        print(semesterlist)

        return semesterlist

    # 1. 학기별로 들은 전공 과목을 가져옴 : [[grade, grade...], [grade, grade...], ....]
    def get_semesterGradelist(self):
        s = self.request.user.hukbun
        semesterlist = self.get_semesterlist()

        semesterGradelist = []
        t = []

        for i in range(0, semesterlist.count()):
            temp = StudentGrade.objects.filter(hukbun=s).filter(
            valid='유효').filter(Q(eisu='컴과')|Q(eisu='전필')).filter(yearNsemester=semesterlist[i]).order_by('yearNsemester')
            for j in range(0, temp.count()):
                t.append(temp[j])
            semesterGradelist.append(t)

        print("semesterGradelist:", end="")
        print(semesterGradelist)

        return semesterGradelist

    #2. 들은 전공 과목 리스트를 가져옴
    def get_gradelist(self):
        s = self.request.user.hukbun
        list = []

        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(eisu='컴과') | Q(eisu='전필')).values_list('subject', flat=True)

        for i in range(0, gradelist.count()):
            list.append(gradelist[i])

        return gradelist

    # 3. 학기별로 들은 과목을 리턴하면 이수체계도에 맞는 학년/학기를 찾아서 듣지 않은 과목 리스트를 리턴한다.
    def check_semesterGradelist(self):
        dic = {}
        temp = {}
        gradelist = self.get_gradelist()
        not_gradelist = []  # 안들은 과목 이름을 넣을거다.
        semesterlist = self.get_semesterlist()
        list = []
        list0 = []
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        list5=[]
        list6=[]
        list7=[]

        if len(gradelist) == 0:
            return eisu_2012_list
        else:
            for i in range(0, len(eisu_2012_list_check)):
                if eisu_2012_list_check[i] not in gradelist:
                    not_gradelist.append(eisu_2012_list_check[i])

            print("not_gradelist:", end="")
            print(not_gradelist)


            # 안들은 과목 리스트가 있는데
            # 이수 체계도 안에서 체크 후에not_gradelist
            for i in range(0, len(not_gradelist)):
                for j in range(0, len(eisu_2012_list)):
                    if not_gradelist[i] in eisu_2012_list[j]:
                        temp[not_gradelist[i]] = j

            for key, item in temp.items():
                if item == 0:
                    list0.append(key)
                elif item == 1:
                    list1.append(key)
                elif item == 2:
                    list2.append(key)
                elif item == 3:
                    list3.append(key)
                elif item == 4:
                    list4.append(key)
                elif item == 5:
                    list5.append(key)
                elif item == 6:
                    list6.append(key)
                elif item == 7:
                    list7.append(key)

            list.append(list0)
            list.append(list1)
            list.append(list2)
            list.append(list3)
            list.append(list4)
            list.append(list5)
            list.append(list6)
            list.append(list7)

        print(list)

        return list

    def get_context_data(self,**kwargs):
        context = super(GraduateLV, self).get_context_data(**kwargs)
        context['total_grade'] = self.get_score_sum()
        context['design_grade'] = self.get_design_grade_sum()
        context['major_grade'] = self.get_major_score_sum()
        context['ge_grade'] = self.get_ge_score_sum()
        context['msc_grade'] = self.get_msc_score_sum()
        context['engineer_cer_ge_grade'] = self.get_eg_ge_score_sum()
        context['semesterlist'] = self.get_semesterlist()
        context['list'] = self.check_semesterGradelist()

        return context
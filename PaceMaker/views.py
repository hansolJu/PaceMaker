from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.base import TemplateView
import operator

# login_required()함수는 데코레이터로 사용되는 함수로, 일반 함수에 적용
# 사용자가 로그인 했는지를 확인해 로그인한 경우는 원래 함수로 실행하고, 로그인 되지 않은 경우는 로그인 페이지로 리다이렉트.
from dataParser.models import StudentGrade, StudentInfo


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


# --- TemplateView
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'

    def total_gradelist(self, s):
        return StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D')| Q(grade='F'))

    def ge_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(
            Q(eisu='M자') | Q(eisu='수리') |Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회') |
            Q(eisu='과기')|Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') | Q(eisu='언문')).filter(
            valid = '유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(
                grade='D') | Q(grade='F'))

    def major_gradelist(self):
        s = self.request.user.hukbun
        return  StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(
            valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(
                grade='D') | Q(grade='F'))

    def msc_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자')|Q(eisu='수리')).filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(
                grade='D') | Q(grade='F'))

    def get_avgGrade(self,gradelist):
        avg = 0.0
        sum = 0.0
        temp = 0.0
        #count = len(gradelist)
        for g in gradelist:
            s = getIntScore(self, g.grade)
            if s == None:
                continue
            else:
                sum = sum + (float(s) * float(g.score))
        for sc in gradelist:
            if sc.score == None:
                continue
            else:
                temp = temp + float(sc.score)
        avg = sum/temp
        return avg


    # 성장률 리턴
    # 성장률
    # 2학년 1학기 이상 학생들만 확인(currentGrade가 1학년 1학기인 학생은 0으로 고정)
    # CurrentGrade가 4학년 1학기이면 3학년 2학기, 3학년 1학기를 가지고 계산
    # (2016년2학기−2016년1학기)/(4.5−2016년1학기)
    def get_growth(self):
        s = self.request.user.hukbun
        currentSemester = StudentInfo.objects.filter(hukbun=s).values_list('currentGrade', flat=True).distinct()
        yearlist = self.get_course_taken()
        currentSemester = currentSemester[0]

        if ((currentSemester == '1학년 1학기') or (currentSemester == '1학년 2학기')):
            return 0
        else:
            idx = yearlist.count()
            print(idx)
            pre_semester = yearlist[idx-1]
            past_semester = yearlist[idx-2]
            pre_avg = self.get_semesterAvg(pre_semester)
            print("pre_avg:%f" % pre_avg)
            past_avg = self.get_semesterAvg(past_semester)
            print("past_avg:%f" % past_avg)

            grow = (pre_avg - past_avg) / (4.5 - pre_avg)

            # up_scale
            grow = grow * 5
            return grow

    # 성적데이터에서 현재까지 들은 학기리스트를 가져옴
    def get_course_taken(self):
        s = self.request.user.hukbun
        yearNsemesterlist = StudentGrade.objects \
            .filter(hukbun=s) \
            .filter(valid='유효') \
            .order_by('yearNsemester') \
            .values_list('yearNsemester', flat=True) \
            .distinct()

        return yearNsemesterlist

    # input : 학기 , return : 학기의 평균
    def get_semesterAvg(self, semester):
        s = self.request.user.hukbun
        sum = 0.0
        score_sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(yearNsemester=semester).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D')| Q(grade='F'))

        gradelist = gradelist.exclude(grade__contains='P')

        for i in range(0, gradelist.count()):
            temp = (getIntScore(self, gradelist[i].grade)*int(gradelist[i].score))
            sum = sum + temp
            score_sum = score_sum + int(gradelist[i].score)
            print(score_sum)

        avg = sum / score_sum
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
        result.append(self.get_growth())
        ''' (2016년2학기−2016년1학기)/(4.5−2016년1학기)'''
        tmp = 3.0
        #result.append(tmp)
        print(result)
        return result



    # 랭크 퍼센트 통계 기능
    def rank_statistic(self):
        s = self.request.user.hukbun
        user_object = StudentInfo.objects.filter(hukbun=s).distinct()[0]
        if self.total_gradelist(s).count() == 0:
            return 1
        user_object = (user_object, self.get_avgGrade(self.total_gradelist(s)))

        user_list = StudentInfo.objects.distinct()
        user_avgList = {}

        for i in range(0, user_list.count()):
            user_avgList[user_list[i]] = self.get_avgGrade(self.total_gradelist(user_list[i].hukbun))

        # sortedArr = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        user_sort = sorted(user_avgList.items(), key=operator.itemgetter(1), reverse=True)
        idx = user_sort.index(user_object)
        size = len(user_sort)

        percent = ((idx+1)/size)

        return percent

    def user_info(self):
        s = self.request.user.hukbun
        user_info = []
        username = StudentInfo.objects.filter(hukbun=s).values_list('username', flat=True)[0]
        currentSemester = StudentInfo.objects.filter(hukbun=s).values_list('currentGrade', flat=True)[0]
        engineCertificate = StudentInfo.objects.filter(hukbun=s).values_list('enginCertification', flat=True)[0]

        user_info.append(s)
        user_info.append(username)
        user_info.append(currentSemester)
        user_info.append(engineCertificate)

        return user_info


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['chart_data'] =  self.Make_chart_data()
        context['percent'] = self.rank_statistic()
        context['user_info'] = self.user_info()
        return context


class UserView(TemplateView):
    template_name = 'user.html'

    def total_gradelist(self, s):
        return StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D')| Q(grade='F'))

    def ge_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(
            Q(eisu='M자') | Q(eisu='수리') |Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회') |
            Q(eisu='과기')|Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') | Q(eisu='언문')).filter(
            valid = '유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(
                grade='D') | Q(grade='F'))

    def major_gradelist(self):
        s = self.request.user.hukbun
        return  StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(
            valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(
                grade='D') | Q(grade='F'))

    def msc_gradelist(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자')|Q(eisu='수리')).filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(
                grade='D+') | Q(
                grade='D') | Q(grade='F'))

    def get_avgGrade(self,gradelist):
        avg = 0.0
        sum = 0.0
        temp = 0.0
        #count = len(gradelist)
        for g in gradelist:
            s = getIntScore(self, g.grade)
            if s == None:
                continue
            else:
                sum = sum + (float(s) * float(g.score))
        for sc in gradelist:
            if sc.score == None:
                continue
            else:
                temp = temp + float(sc.score)
        avg = sum/temp
        return avg


    # 성장률 리턴
    # 성장률
    # 2학년 1학기 이상 학생들만 확인(currentGrade가 1학년 1학기인 학생은 0으로 고정)
    # CurrentGrade가 4학년 1학기이면 3학년 2학기, 3학년 1학기를 가지고 계산
    # (2016년2학기−2016년1학기)/(4.5−2016년1학기)
    def get_growth(self):
        s = self.request.user.hukbun
        currentSemester = StudentInfo.objects.filter(hukbun=s).values_list('currentGrade', flat=True).distinct()
        yearlist = self.get_course_taken()
        currentSemester = currentSemester[0]

        if ((currentSemester == '1학년 1학기') or (currentSemester == '1학년 2학기')):
            return 0
        else:
            idx = yearlist.count()
            print(idx)
            pre_semester = yearlist[idx-1]
            past_semester = yearlist[idx-2]
            pre_avg = self.get_semesterAvg(pre_semester)
            print("pre_avg:%f" % pre_avg)
            past_avg = self.get_semesterAvg(past_semester)
            print("past_avg:%f" % past_avg)

            grow = (pre_avg - past_avg) / (4.5 - pre_avg)

            # up_scale
            grow = grow * 5
            return grow

    # 성적데이터에서 현재까지 들은 학기리스트를 가져옴
    def get_course_taken(self):
        s = self.request.user.hukbun
        yearNsemesterlist = StudentGrade.objects \
            .filter(hukbun=s) \
            .filter(valid='유효') \
            .order_by('yearNsemester') \
            .values_list('yearNsemester', flat=True) \
            .distinct()

        return yearNsemesterlist

    # input : 학기 , return : 학기의 평균
    def get_semesterAvg(self, semester):
        s = self.request.user.hukbun
        sum = 0.0
        score_sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(yearNsemester=semester).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D')| Q(grade='F'))

        gradelist = gradelist.exclude(grade__contains='P')

        for i in range(0, gradelist.count()):
            temp = (getIntScore(self, gradelist[i].grade)*int(gradelist[i].score))
            sum = sum + temp
            score_sum = score_sum + int(gradelist[i].score)
            print(score_sum)

        avg = sum / score_sum
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
        result.append(self.get_growth())
        ''' (2016년2학기−2016년1학기)/(4.5−2016년1학기)'''
        tmp = 3.0
        #result.append(tmp)
        print(result)
        return result



    # 랭크 퍼센트 통계 기능
    def rank_statistic(self):
        s = self.request.user.hukbun
        user_object = StudentInfo.objects.filter(hukbun=s).distinct()[0]
        if self.total_gradelist(s).count() == 0:
            return 1
        user_object = (user_object, self.get_avgGrade(self.total_gradelist(s)))

        user_list = StudentInfo.objects.distinct()
        user_avgList = {}

        for i in range(0, user_list.count()):
            user_avgList[user_list[i]] = self.get_avgGrade(self.total_gradelist(user_list[i].hukbun))

        # sortedArr = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        user_sort = sorted(user_avgList.items(), key=operator.itemgetter(1), reverse=True)
        idx = user_sort.index(user_object)
        size = len(user_sort)

        percent = ((idx+1)/size)

        return percent

    def user_info(self):
        s = self.request.user.hukbun
        user_info = []
        username = StudentInfo.objects.filter(hukbun=s).values_list('username', flat=True)[0]
        currentSemester = StudentInfo.objects.filter(hukbun=s).values_list('currentGrade', flat=True)[0]
        engineCertificate = StudentInfo.objects.filter(hukbun=s).values_list('enginCertification', flat=True)[0]

        user_info.append(s)
        user_info.append(username)
        user_info.append(currentSemester)
        user_info.append(engineCertificate)

        return user_info


    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['chart_data'] =  self.Make_chart_data()
        context['percent'] = self.rank_statistic()
        context['user_info'] = self.user_info()
        return context

from django.views.generic import *
from dataParser.models import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
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


class GradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/grades_list.html'
    context_object_name = 'grades_list'

    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효')
        scorelist = scorelist.exclude(grade__contains='P').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    def get_avgGrade(self):
        s = self.request.user.hukbun
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D')| Q(grade='F'))
        for i in range(0, gradelist.count()):
            print(gradelist[i].subject+","+gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            print(temp)
            sum = sum + temp
        score_sum = self.get_score_sum()
        print(score_sum)
        avg = sum/score_sum
        #avg = round(avg, 3)
        return avg

    def get_queryset(self):
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).order_by('yearNsemester', 'subject')

    def get_fake_grade_sum(self):
        s = self.request.user.hukbun
        fake_grade_sum = StudentGrade.objects.filter(hukbun=s).values_list('score', flat=True)
        sum = 0
        for i in fake_grade_sum:
            sum = sum + float(i)

        return sum

    def get_design_grade_sum(self):
        s = self.request.user.hukbun
        design_gradelist = StudentGrade.objects.filter(hukbun=s).values_list('grade_design', flat=True)
        sum = 0.0
        for i in design_gradelist:
            sum = sum + float(i)

        return sum


    def get_context_data(self,**kwargs):
        context = super(GradeLV, self).get_context_data(**kwargs)
        context['grade_list'] = self.get_queryset()
        context['grade_sum'] = self.get_score_sum()
        context['avgGrade'] = self.get_avgGrade()
        context['fake_grade_sum'] = self.get_fake_grade_sum()
        context['design_grade_sum'] = self.get_design_grade_sum()
        return context


class MajorGradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/major_subject_list.html'
    context_object_name = 'major_list'

    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).filter(valid ='유효').exclude(grade__contains='F').values_list('score', flat=True)
        scorelist = scorelist.exclude(grade__contains='P')
        for i in scorelist:
            sum = sum + float(i)

        return sum

    def get_avgGrade(self):
        s = self.request.user.hukbun
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(valid='유효').filter(Q(eisu='컴과')|Q(eisu='전필')).filter(
            Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') |
            Q(grade='C') | Q(grade='D+') | Q(grade='D') | Q(grade='F'))
        gradelist = gradelist.exclude(grade__contains='P')
        print(gradelist)

        for i in range(0, gradelist.count()):
            print(gradelist[i].subject+","+gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            sum = sum + temp
        score_sum = self.get_score_sum()
        avg = sum/score_sum
        return avg

    def get_fake_grade_sum(self):
        s = self.request.user.hukbun
        fake_grade_sum = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필')).values_list('score', flat=True)
        sum = 0
        for i in fake_grade_sum:
            sum = sum + float(i)

        return sum

    def get_queryset(self):
        # 학번과 이수로 filter를 사용해서 리스트를 가져와야 한다.
        s = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='컴과') | Q(eisu='전필'))

    def get_context_data(self,**kwargs):
        context = super(MajorGradeLV, self).get_context_data(**kwargs)
        context['major_list'] = self.get_queryset()
        context['grade_sum'] = self.get_score_sum()
        context['avgGrade'] = self.get_avgGrade()
        context['fake_grade_sum'] = self.get_fake_grade_sum()
        return context


class GeGradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/ge_subject_list.html'
    context_object_name = 'ge_list'

    def get_queryset(self):
        test = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=test).filter(
            Q(eisu='M자') |Q(eisu='수리')| Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회')
            |Q(eisu='과기')|Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') | Q(eisu='언문'))

    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(
            Q(eisu='M자') | Q(eisu='수리')| Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회')
            |Q(eisu='과기')|Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') | Q(eisu='언문')).filter(valid = '유효').values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    def get_avgGrade(self):
        s = self.request.user.hukbun
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(
            Q(eisu='M자')|Q(eisu='수리')| Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') |
            Q(eisu='사회') | Q(eisu='과기') | Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') |
            Q(eisu='언문')).filter(valid='유효').filter(Q(grade='A+') | Q(grade='A') | Q(grade='B+') |
            Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D') | Q(grade='F'))

        for i in range(0, gradelist.count()):
            print(gradelist[i].subject+","+gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            sum = sum + temp

        score_sum = self.get_score_sum()
        avg = sum/score_sum
        return avg

    def get_fake_grade_sum(self):
        s = self.request.user.hukbun
        fake_grade_sum = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자') | Q(eisu='필수') | Q(eisu='역철') | Q(eisu='경사') | Q(eisu='체기') | Q(eisu='사회') | Q(eisu='과기') | Q(eisu='자협') | Q(eisu='미래') | Q(eisu='직필') | Q(eisu='문예') | Q(eisu='언문')).values_list('score', flat=True)
        sum = 0
        for i in fake_grade_sum:
            sum = sum + float(i)

        return sum

    def get_context_data(self,**kwargs):
        context = super(GeGradeLV, self).get_context_data(**kwargs)
        context['ge_list'] = self.get_queryset()
        context['grade_sum'] = self.get_score_sum()
        context['avgGrade'] = self.get_avgGrade()
        context['fake_grade_sum'] = self.get_fake_grade_sum()
        return context


class MscGradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/msc_subject_list.html'
    context_object_name = 'msc_list'

    def get_queryset(self):
        test = self.request.user.hukbun
        return StudentGrade.objects.filter(hukbun=test).filter(Q(eisu='M자') | Q(eisu='수리'))

    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        scorelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자') | Q(eisu='수리')).values_list('score', flat=True)
        for i in scorelist:
            sum = sum + float(i)

        return sum

    def get_avgGrade(self):
        s = self.request.user.hukbun
        avg = 0.0
        sum = 0.0
        gradelist = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자')|Q(eisu='수리')).filter(Q(grade='A+') |
                Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D') | Q(grade='F'))

        for i in range(0, gradelist.count()):
            print(gradelist[i].subject + "," + gradelist[i].grade)
            temp = getIntScore(gradelist[i].grade) * int(gradelist[i].score)
            sum = sum + temp

        score_sum = self.get_score_sum()
        avg = sum / score_sum
        return avg

    # def get_avgGrade(self):
    #     s = self.request.user.hukbun
    #     avg = 0.0
    #     sum = 0.0
    #     gradelist = StudentGrade.objects.filter(hukbun=s).filter(eisu='M자').filter(Q(grade='A+') |
    # Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D') | Q(grade='F')).values_list('grade', flat=True)
    #     count = len(gradelist)
    #     for g in gradelist:
    #         s = getIntScore(g)
    #         if s == None:
    #             continue
    #         else:
    #             sum = sum + s
    #     avg = sum / count
    #     return avg

    def get_fake_grade_sum(self):
        s = self.request.user.hukbun
        fake_grade_sum = StudentGrade.objects.filter(hukbun=s).filter(Q(eisu='M자') | Q(eisu='수리')).values_list('score', flat=True)
        sum = 0
        for i in fake_grade_sum:
            sum = sum + float(i)

        return sum

    def get_context_data(self, **kwargs):
        context = super(MscGradeLV, self).get_context_data(**kwargs)
        context['msc_list'] = self.get_queryset()
        context['grade_sum'] = self.get_score_sum()
        context['avgGrade'] = self.get_avgGrade()
        context['fake_grade_sum'] = self.get_fake_grade_sum()
        return context


class SemesterGradeLV(LoginRequiredMixin,ListView):
    model = StudentGrade
    template_name = 'grades/grade_semester_list.html'
    context_object_name = 'semestergradelist'

    def get_semester_list(self):
        s = self.request.user.hukbun
        semesterlist = self.get_queryset()
        semestergradelist = []
        for i in range(0, len(semesterlist)):
            semestergradelist.append(StudentGrade.objects.filter(hukbun=s).filter(yearNsemester=semesterlist[i]).order_by('yearNsemester'))

        return semestergradelist

    def get_queryset(self):
        s = self.request.user.hukbun
        semesterlist = StudentGrade.objects.filter(hukbun=s).values_list('yearNsemester', flat=True).distinct().order_by('yearNsemester')
        return semesterlist

    ##평점 산출 학점##
    def get_score_sum(self):
        s = self.request.user.hukbun
        sum = 0
        semesterlist = self.get_queryset()
        scorelist = []
        for i in range(0, len(semesterlist)):
            temp = StudentGrade.objects.filter(hukbun=s)\
                .filter(yearNsemester=semesterlist[i])\
                .filter(valid='유효')
            temp = temp.exclude(grade__contains='P')
            scorelist.append(temp.values_list('score', flat=True))
        print(scorelist)
        sumlist = []
        for i in scorelist:
            for j in i:
                sum = sum + float(j)
            sumlist.append(sum)
            sum = 0

        return sumlist

    ##평점 평균##
    def get_avgGrade(self):
        s = self.request.user.hukbun
        avg = 0.0
        sum = 0.0
        semesterlist = self.get_queryset()
        gradelist = []
        avglist = []
        for i in range(0, len(semesterlist)):
            gradelist.append(StudentGrade.objects.filter(hukbun=s).filter(yearNsemester=semesterlist[i]).filter(valid='유효').filter(
                Q(grade='A+') | Q(grade='A') | Q(grade='B+') | Q(grade='B') | Q(grade='C+') | Q(grade='C') | Q(grade='D+') | Q(grade='D')| Q(grade='F')))
        print(gradelist)
        score_sumlist = self.get_score_sum() #list
        print(score_sumlist)
        for i in range(0, len(gradelist)):
            for g in gradelist[i]:
                s = getIntScore(g.grade) * int(g.score)
                sum = sum + s
            print(sum)
            avg = sum/score_sumlist[i]
            avglist.append(avg)
            sum = 0

        return avglist

    ##취득 학점##
    def get_fake_grade_sum(self):
        s = self.request.user.hukbun
        sum = 0
        semesterlist = self.get_queryset()
        scorelist = []
        for i in range(0, len(semesterlist)):
            temp = StudentGrade.objects.filter(hukbun=s).filter(yearNsemester=semesterlist[i])
            #temp = temp.exclude(grade='P')
            scorelist.append(temp.values_list('score', flat=True))
        print(scorelist)
        total_sumlist = []
        for i in scorelist:
            for j in i:
                sum = sum + float(j)
            total_sumlist.append(sum)
            sum = 0

        return total_sumlist

    ##취득 설계 학점##
    def get_design_grade_sum(self):
        s = self.request.user.hukbun
        sum = 0
        semesterlist = self.get_queryset()
        design_scorelist = []
        for i in range(0, len(semesterlist)):
            temp = StudentGrade.objects.filter(hukbun=s).filter(yearNsemester=semesterlist[i])
            # temp = temp.exclude(grade='P')
            design_scorelist.append(temp.values_list('grade_design', flat=True))
        print(design_scorelist)
        design_sumlist = []
        for i in design_scorelist:
            for j in i:
                sum = sum + float(j)
            design_sumlist.append(sum)
            sum = 0

        return design_sumlist

    def get_context_data(self,**kwargs):
        context = super(SemesterGradeLV, self).get_context_data(**kwargs)
        context['semesterlist'] = self.get_queryset()
        context['semestergradelist'] = self.get_semester_list()
        context['sumlist'] = self.get_score_sum()
        context['avglist'] = self.get_avgGrade()
        context['total_sumlist'] = self.get_fake_grade_sum()
        context['design_sumlist'] = self.get_design_grade_sum()
        return context

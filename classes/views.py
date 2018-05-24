from django.shortcuts import render
from dataParser.models import StudentInfo, Course
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.
class majorLV(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'classes/majorAll.html'
    context_object_name = 'subjects'
    paginate_by = 2

class majorDV(LoginRequiredMixin, DetailView):
    model = Course

class recommand(LoginRequiredMixin, View):
    def get(self, request):
        student = StudentInfo.objects.get(hukbun=request.user.hukbun)
        print(student)
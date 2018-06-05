from django.db import models
from dataParser.models import Course

class necessaryCourse(models.Model):
    childCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='necessary_child')
    parentCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='necessary_parent')
class promotedCourse(models.Model):
    childCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='promoted_child')
    parentCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='promoted_parent')
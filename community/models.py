from django.db import models
from django.urls import reverse
from tagging.fields import TagField
from dataParser.models import StudentInfo
from django.utils.text import slugify


class Post(models.Model):
    title =  models.CharField('제목', max_length=50)
    slug = models.SlugField('슬러그', unique=True, allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('요약 설명', max_length=100, blank=True,
                                   help_text='simple description text.')
    content = models.TextField('내용')
    tag = TagField('태그')
    create_date = models.DateTimeField('생성 날짜', auto_now_add=True)
    modify_date = models.DateTimeField('수정 날짜', auto_now=True)
    owner = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    hits = models.IntegerField('조회수',null=True, blank=True)
#tagField는 CharField를 상속받아서 디폴트로 amx_length=255,Blank=True로 정의하고 있어서 따로 내용을 안채워도됨


    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'my_post'
        ordering = ('-modify_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('community:post_detail', args=(self.slug,))

    def get_previous_post(self):
        return self.get_previous_by_modify_date()

    def get_next_post(self):
        return self.get_next_by_modify_date()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)
# Create your models here.

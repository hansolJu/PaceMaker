from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from tagging.views import TaggedObjectList

from django.contrib.auth.mixins import LoginRequiredMixin
from community.models import Post
from dataParser.models import StudentInfo

# --- TemplateView
class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'

# --- ListView
class PostLV(ListView):
    model = Post
    template_name =  'community/post_all.html'
    context_object_name = 'posts'

    count_hit =True

    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostLV, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class PostTOL(TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'

# --- DeatilView
class PostDV(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'community/post_detail.html'

    def pageCounter(self, pk):
        post = Post.objects.get(id=pk)
        post.hits += 1
        post.save()
        return render('blog/post_detail.hmtl', {'post': post})



# --- CRUD View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug': 'auto-filling-do-not-input'}
    # slug 필드를 처리하는 또 다른 방법은 fields속성에서 제외해 폼에 나타나지 않도록 하는 방법입니다. \
    # 폼에는 보이지 않지만, Post 모델의 save()함수에 의해 테리블의 레코드에는 자동으로 채워집니다.
    # fields = ['title', 'description', 'content', 'tag']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('community:index')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('community:index')
# Create your views here.

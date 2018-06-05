from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from tagging.views import TaggedObjectList

from django.contrib.auth.mixins import LoginRequiredMixin
from community.models import PostIF,PostOB
from dataParser.models import StudentInfo

from django.views.generic.edit import FormView
from community.forms import PostSearchForm,DocumentForm
from django.db.models import Q
from django.shortcuts import render

# --- TemplateView
class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'

# --- ListView
class OldbookLV(ListView):
    model = PostOB
    template_name = 'community/post_oldbook.html'
    context_object_name = 'posts'

    paginate_by = 5  # Display 5 objects per page

    def get_context_data(self, **kwargs):
        context = super(OldbookLV, self).get_context_data(**kwargs)
        paginator = context['paginator']
        context['totalCnt'] = PostOB.objects.all().count()
        page_numbers_range = 5  # Display only 5 page numbers
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

    def get_filter(self, **kwargs):
        sort = self.request.GET.get('sort','')

        if sort == 'mypost':
            sortfilter = PostOB.objects.filter(user=self.request.user).order_by('pk')
            return sortfilter
        elif sort == 'new':
            sortfilter = PostOB.objects.order_by('modify_date')
            return sortfilter

class InfoLV(ListView):
    model = PostIF
    template_name = 'community/post_Info.html'
    context_object_name = 'posts'

    paginate_by = 5 # Display 5 objects per page

    def get_context_data(self, **kwargs):
        context = super(InfoLV, self).get_context_data(**kwargs)
        paginator = context['paginator']
        context['totalCnt'] = PostIF.objects.all().count()
        page_numbers_range = 5 # Display only 5 page numbers
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
    model = PostIF
    template_name = 'tagging/tagging_post_list.html'

# --- DeatilView
class PostDV(LoginRequiredMixin,DetailView):
    model = PostIF
    template_name = 'community/Information_detail.html'

    def get_queryset(self):
        return PostIF.objects.all()    #filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(PostDV, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.hits = obj.hits + 1
        obj.save()
        return context


    # def count(self, **kwargs):
    #     context = super(PostDV, self).get_context_data(**kwargs)
    #     hit = context['hit']

    # def pageCounter(self,request):
    #     pk = request.GET['title']
    #     post = Post.objects.get(id=pk)
    #
    #     # 조회수를 늘린다.
    #     Post.objects.filter(id=pk).update(hits=Post.hits + 1)
    #
    #     return render('community/post_Info.html', {'post':post})

        # post = Post.objects.get(id=pk)
        # post.hits += 1
        # post.save()
        # return redirect('community/Information_detail.hmtl', {'post': post})

class OBPostDV(LoginRequiredMixin,DetailView):
    model = PostOB
    template_name = 'community/Oldbook_detail.html'

    def get_queryset(self):
        return PostOB.objects.all()    #filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(OBPostDV, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.hits = obj.hits + 1
        obj.save()
        return context

class SearchFormView(InfoLV,FormView):
    form_class = PostSearchForm
    template_name = 'community/post_Info.html'

    def form_valid(self, form):
        schWord = '%s' %self.request.POST['search_word']
        post_info_list = PostIF.objects.filter(Q(title__icontains=schWord)|Q(description__icontains=schWord)
                                        |Q(content__icontains=schWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_info_list

        return render(self.request, self.template_name, context)

class OBSearchFormView(OldbookLV,FormView):
    form_class = PostSearchForm
    template_name = 'community/post_oldbook.html'

    def form_valid(self, form):
        schWord = '%s' %self.request.POST['search_word']
        post_oldbook_list = PostOB.objects.filter(Q(title__icontains=schWord)|Q(description__icontains=schWord)
                                        |Q(content__icontains=schWord)).distinct()
        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_oldbook_list

        return render(self.request, self.template_name, context)

# --- CRUD View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = PostIF

    fields = ['title',  'description', 'content', 'file']
    initial = {'slug': 'auto-filling-do-not-input'}
    # slug 필드를 처리하는 또 다른 방법은 fields속성에서 제외해 폼에 나타나지 않도록 하는 방법입니다. \
    # 폼에는 보이지 않지만, Post 모델의 save()함수에 의해 테리블의 레코드에는 자동으로 채워집니다.
    # fields = ['title', 'description', 'content', 'tag']
    success_url = reverse_lazy('community:Info_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)

class OBPostCreateView(LoginRequiredMixin, CreateView):
    model = PostOB

    fields = ['buysell', 'title',  'description', 'content', 'file']
    initial = {'slug': 'auto-filling-do-not-input'}
    # slug 필드를 처리하는 또 다른 방법은 fields속성에서 제외해 폼에 나타나지 않도록 하는 방법입니다. \
    # 폼에는 보이지 않지만, Post 모델의 save()함수에 의해 테리블의 레코드에는 자동으로 채워집니다.
    # fields = ['title', 'description', 'content', 'tag']
    success_url = reverse_lazy('community:ob_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OBPostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = PostIF
    fields = ['title', 'description', 'content', 'file']
    success_url = reverse_lazy('community:Info_list')

    def get_queryset(self):
        return PostIF.objects.filter(owner=self.request.user)

class OBPostUpdateView(LoginRequiredMixin, UpdateView):
    model = PostOB
    fields = ['title', 'description', 'content','file']
    success_url = reverse_lazy('community:ob_list')

    def get_queryset(self):
        return PostOB.objects.filter(owner=self.request.user)



class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = PostIF
    success_url = reverse_lazy('community:Info_list')

    def get_queryset(self):
        return PostIF.objects.filter(owner=self.request.user)

class OBPostDeleteView(LoginRequiredMixin, DeleteView):
    model = PostOB
    success_url = reverse_lazy('community:ob_list')

    def get_queryset(self):
        return PostOB.objects.filter(owner=self.request.user)

# Create your views here.


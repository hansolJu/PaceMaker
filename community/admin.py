from django.contrib import admin

from community.models import PostIF,PostOB

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'modify_date')
    list_filter = ('modify_date',)
    search_fields =  ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(PostIF, PostAdmin)
admin.site.register(PostOB, PostAdmin)
# Register your models here.

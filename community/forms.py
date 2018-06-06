from django import forms

# 커뮤니티 검색 forms
class PostSearchForm(forms.Form):
    search_word = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'form-control', 'placeholder': 'Search...'
                   }),
        label=False)

# 파일 업로드 forms
class DocumentForm(forms.Form):
    files =  forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


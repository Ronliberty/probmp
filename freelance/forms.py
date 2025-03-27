from django import forms
from .models import Post, News, Tool, Skill


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'country', 'link', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter description'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter valid URL'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("A post with this title already exists.")
        return title

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link and not link.startswith(('http://', 'https://')):
            raise forms.ValidationError("Enter a valid URL starting with http:// or https://")
        return link


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['headline', 'content', 'country']

    def clean_headline(self):
        headline = self.cleaned_data.get('headline')
        if News.objects.filter(headline=headline).exists():
            raise forms.ValidationError("A news article with this headline already exists.")
        return headline


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description', 'link', 'country', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Tool.objects.filter(name=name).exists():
            raise forms.ValidationError("A tool with this name already exists.")
        return name

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link and not link.startswith(('http://', 'https://')):
            raise forms.ValidationError("Enter a valid URL starting with http:// or https://")
        return link


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description', 'country']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Skill.objects.filter(name=name).exists():
            raise forms.ValidationError("A skill with this name already exists.")
        return name

from django import forms
from .models import Tag, Comment, Reply
from .fields import SimpleCaptchaField

'''------------------------------------タグ関連------------------------------------
'''
class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


'''------------------------------------コメント関連------------------------------------
'''
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('target', 'data_created')
        widgets = {
            'text':forms.Textarea(
                attrs={'placeholder': 'コメント記入欄'}
                )
        }
    captcha = SimpleCaptchaField()

class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('target', 'data_created')
        widgets = {
            'text':forms.Textarea(
                attrs={'placeholder': '返信記入欄'}
                )
        }
    captcha = SimpleCaptchaField()

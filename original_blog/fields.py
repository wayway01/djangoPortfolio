from django import forms

class SimpleCaptchaField(forms.CharField):

    def __init__(self, label='Captcha', **kwargs):
        super().__init__(label=label, required=True, **kwargs)
        self.widget.attrs['placeholder'] = '投稿するためには、1+1の答えを入力してください。'

    def clean(self, value):
        value = super().clean(value)
        if value == "2":
            return value
        else:
            raise forms.ValidationError('答えが違います。')
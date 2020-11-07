from django import forms
from captcha.fields import CaptchaField


class captchaForm(forms.Form):
    captcha = CaptchaField(label='验证码')

#coding=utf-8
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

class RegForm(forms.ModelForm):
    username=forms.EmailField(label=u'注册邮箱',help_text='激活帐号和登录时用')
    password1=forms.CharField(label=u'登录密码',help_text='不少于6位',
            widget=forms.PasswordInput,min_length=6)
    password2=forms.CharField(label=u'确认密码',widget=forms.PasswordInput,min_length=6)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(RegForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #用户处于未激活状态
        user.is_active=0;
        user.email = user.username
        if commit:
            user.save()
        return user

__author__ = 'jingyuan'
__date__ = '2020/5/16 9:50'

import re

from django import forms
from apps.operations.models import UserAsk

# class AddAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     mobile = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=2, max_length=20)

class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[358]\d{9}|^146\d{8}$|^176\d{8}$"

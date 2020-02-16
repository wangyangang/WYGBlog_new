from django import forms


class PostAdminForm(forms.ModelForm):
    """更改后台管理的Form界面"""
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
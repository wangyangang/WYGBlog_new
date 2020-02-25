from django import forms
from .models import Category, Tag, Post
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from mdeditor.fields import MDTextField
from mdeditor.widgets import MDEditorWidget


class PostAdminForm(forms.ModelForm):
    """更改后台管理的Form界面"""
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows': 11, 'cols': 109}), label='摘要', required=False)
    # category = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                   widget=autocomplete.ModelSelect2(url='category-autocomplete'),
    #                                   label='分类')
    # tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
    #                                      widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
    #                                      label='标签')
    # content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)
    # content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True) 上传图片用这个
    #content_md = forms.CharField(widget=forms.Textarea(
                                # attrs={'rows': 30, 'cols': 120, 'class': 'form-control'}
                                # ),
                                #  label='content_md正文',
                                #  required=False)
    content = forms.CharField(widget=MDEditorWidget(), label='正文', required=True)
    # content = forms.CharField(widget=forms.HiddenInput(), required=False, label='content正文')

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc',
                  'content', 'status')

    # def __init__(self, *args, **kwargs):
        # initial = initial or {}
        # if instance:
        #     if instance.is_md:
        #         initial['content_md'] = instance.content
        #     else:
        #         initial['content_ck'] = instance.content
        # print('----------------------')
        # super().__init__(instance=instance, initial=initial, **kwargs)

        # initial = kwargs.get('initial') or {}
        # instance = kwargs.get('instance')
        # if instance:
        #     if instance:
        #         initial['content_md'] = instance.content
        #     else:
        #         initial['content_ck'] = instance.content
        # kwargs.update({'instance': instance, 'initial': initial})
        # super(PostAdminForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     is_md = self.cleaned_data.get('is_md')
    #     if is_md:
    #         content_field_name = 'content_md'
    #     else:
    #         content_field_name = 'content_ck'
    #     content = self.cleaned_data.get(content_field_name)
    #     if not content:
    #         self.add_error(content_field_name, '必须填')
    #         return
    #     self.cleaned_data['content'] = content
    #     return super().clean()

    class Media:
        js = ('js/jquery.js', 'js/post_editor.js',)



from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView

from .forms import CommentForm


class AddCommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        post_id = request.POST.get('post')
        blog_name = request.POST.get('blog_name')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.post_id = post_id
            instance.save()
            succeed = True
            return redirect(reverse('blog:post', args=(blog_name, post_id)))
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'post': post_id
        }
        return self.render_to_response(context)


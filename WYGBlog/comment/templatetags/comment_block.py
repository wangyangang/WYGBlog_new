from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(post, blog_name):
    return {
        'post': post,
        'blog_name': blog_name,
        'comment_form': CommentForm(),
        'comments': post.comment_set.all()
    }

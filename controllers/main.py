from django.shortcuts import render_to_response
from models.busline import Busline
from django.template import RequestContext
# from controllers.utils import modal_message
from models.post import Post


def main():
    """Load main page."""
    busline = Busline.filter_by_line_equals(line_number)
    posts = Post.objects.filter(busline__id=busline.id)
    posts = sorted(posts, key=lambda post: (post.time), reverse=True)
    return render_to_response("main.html",
                              {'busline': busline,
                                  'posts': posts, },
                              context_instance=RequestContext(request))

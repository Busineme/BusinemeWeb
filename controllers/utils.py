from django.shortcuts import render_to_response
from django.template import RequestContext
from models.post import Post
from models.favorite import Favorite


def modal_message(alert_title, error_lead, error_message_in, html, request):
    r"""
    Populate a htmlvars with the error message and generates the\
    response.
    """
    htmlvars = {}
    htmlvars["alert_title"] = alert_title
    htmlvars["error_lead"] = error_lead
    htmlvars["modal_message"] = error_message_in
    response = response_htmlvars(htmlvars, html, request)
    return response


def generic_htmlvars(html, request, **kvargs):
    """Populate a htmlvars with generic inputs"""
    return response_htmlvars(kvargs, html, request)


def call_feed_page(request, **kvargs):
    posts = Post.all()
    posts = sorted(
        posts, key=lambda post: (post.time), reverse=True)
    posts = posts[:10]
    favorites = Favorite.objects.filter(
        user_id=request.user)
    if favorites == []:
        favorites = None
    return generic_htmlvars(
        'feed_page.html', request, posts=posts, favorites=favorites, **kvargs)


def response_htmlvars(htmlvars, html, request):
    """Generate a response with a already populated htmlvars."""
    response = render_to_response(html, htmlvars,
                                  context_instance=RequestContext(request))
    return response

from django.shortcuts import render_to_response
from django.template import RequestContext
from controllers.utils import call_feed_page


def feed_page(request):
    """Load feed page."""
    return call_feed_page(request)


def about_page(request):
    """Load about page."""
    return render_to_response('about_page.html',
                              context_instance=RequestContext(request))

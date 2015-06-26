# -*- coding: utf-8 -*-
"""Busline controller docstring"""
from django.shortcuts import render_to_response
from models.busline import Busline
from django.template import RequestContext
from controllers.utils import modal_message
from models.post import Post


def search_line(request):
    r"""
    Perform a search for bus lines that contain the input value entered\
    by the user then returns the result page and the list of results.
    """
    line_number = request.GET['busline']
    buslines = Busline.filter_by_line_number(line_number)
    count_busline = len(buslines)
    response = render_to_response("search_result_page.html",
                                  {'buslines': buslines,
                                   'count_busline': count_busline,
                                   'searched_number': line_number},
                                  context_instance=RequestContext(request))
    return response


def advanced_search_busline(request):
    r"""
    Perform an advanced search for bus lines which contain the input values\
    entered by the user then returns the result page and the list of results.
    """
    if ((len(request.GET['busline_advanced']) < 2) and
            (len(request.GET['description']) < 2)):
        response = modal_message(
            "Erro :(",
            "Entrada inválida.",
            "Os campos preenchidos da busca avançada devem possuir \
            no mínimo 2 dígitos.",
            "search_result_page.html", request)
    else:
        buslines = Busline.filter_by_multiple(
            line_number=request.GET['busline_advanced'],
            description=request.GET['description'],
            terminal__description=''
        )
        count_busline = len(buslines)
        line_number = request.GET['busline_advanced']
        response = render_to_response(
            "search_result_page.html",
            {'buslines': buslines,
             'count_busline': count_busline,
             'searched_number': line_number,
             'description': request.GET['description']},
            context_instance=RequestContext(request))

    return response


def advanced_search_busline_page(request):
    """Return the advanced search page when requested."""
    return render_to_response("advanced_search_busline_page.html",
                              context_instance=RequestContext(request))


def busline_profile(request, line_number):
    """Return the profle page from a line number when requested."""
    busline = Busline.get_by_line_equals(line_number)
    posts = Post.objects.filter(busline__id=busline.id)
    posts = sorted(posts, key=lambda post: (post.time), reverse=True)
    return render_to_response("busline_profile.html",
                              {'busline': busline,
                                  'posts': posts, },
                              context_instance=RequestContext(request))

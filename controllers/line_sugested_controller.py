
from django.template import RequestContext
from controllers.utils import modal_message
from models.terminal import Terminal
from models.line_sugested import LineSugested
from django.shortcuts import render_to_response


def sugesting_line(request):
    r"""
    Call method to sugest_line  depending on the request \
    method (GET or POST).
    """
    if request.method == 'GET':
        response = sugesting_line_page(request)
    elif request.method == 'POST':
        response = sugesting_line_action(request)
    return response


def sugesting_line_page(request):
    terminals = Terminal.all()
    response = render_to_response('line_sugested_page.html', {'terminals': terminals}, context_instance=RequestContext(request))
    return response


def sugesting_line_action(request):
    """save data on db page when requested. """
    line_sugest = LineSugested()
    line_sugest.busline = int(request.POST['busline'])
    line_sugest.description = request.POST['description']
    line_sugest.justify = request.POST['justify']
    line_sugest.via = request.POST['via']
    line_sugest.terminal_id = request.POST['terminal']
    # line_sugest.terminal = request.POST['terminal']
    line_sugest.save()

    response = modal_message('Sucesso', 'linha sugerida com sucesso', 'Lnha sugerida \
            com sucesso!', 'feed_page.html', request)
    return response

# -*- coding: utf-8 -*-
"""Post controller docstring"""
from django.shortcuts import render_to_response
from models.post import Post
from models.busline import Busline
from django.template import RequestContext
from controllers.utils import modal_message, call_feed_page
from django.contrib.auth.decorators import login_required
from exception.line_without_post import LineWithoutPostError
from exception.api import ApiException


def make_post_page(request):
    """Return the post page when requested. """
    line_number = request.GET['line_number']
    busline = Busline.get_by_line_equals(line_number)
    busline_id = busline.id
    terminals = busline.terminals
    try:
        last_post = Post.last(busline_id)
    except LineWithoutPostError:
        last_post = None
    if request.user.is_authenticated():
        return render_to_response("make_post_page.html",
                                  {'line_number': line_number,
                                   'last_post': last_post,
                                   'terminals': terminals},
                                  context_instance=RequestContext(request))
    else:
        return modal_message(
            "Erro :(",
            "Usuário não logado.",
            "Para realizar esta ação.\
             você deve estar logado.",
            "login_page.html", request)


@login_required
def make_post_action(request):
    """Perform the action of saving the post. """

    post = Post()
    post.capacity = request.POST['capacity']
    post.traffic = request.POST['traffic']
    post.comment = request.POST['description']
    post.latitude = request.POST['codigo_latitude']
    post.longitude = request.POST['codigo_longitude']
    post.user_id = request.user.id
    try:
        post.terminal_id = request.POST["terminal"]
    except:
        return call_feed_page(request,
                              alert_title='Erro :(',
                              error_lead='Campo não preenchido.',
                              modal_message='O campo de terminal deve ser \
                              preenchido para realizar uma businada.'
                              )
    pontuation = 0

    if request.POST['review'] == '':
        pontuation = 0
    else:
        pontuation = int(request.POST['review'])
    try:
        busline = Busline.get_by_line_equals(request.POST['line_number'])
        post.busline_id = busline.id
        try:
            last_post = Post.last(post.busline_id)
            last_post.user.pontuation = last_post.user.pontuation + \
                pontuation
            last_post.user.save()
        except LineWithoutPostError:
            pass
        if post.latitude == "" or post.longitude == "":
            return call_feed_page(request,
                                  alert_title='Erro :(',
                                  error_lead='Serviço não disponível',
                                  modal_message='Não conseguimos obter sua\
                                       geolocalização.'
                                  )
        post.save()
        response = call_feed_page(request,
                                  alert_title='Sucesso',
                                  error_lead='Post realizado',
                                  modal_message='Post realizado com sucesso!'
                                  )
    except ApiException:
        response = call_feed_page(request,
                                  alert_title='Erro :(',
                                  error_lead='Servidor não disponível',
                                  modal_message='O acesso ao servidor está \
                                  indisponível no momento, verifique sua \
                                  conexão.'
                                  )

    if post.latitude == "" or post.longitude == "":
        return call_feed_page(request,
                              alert_title='Erro :(',
                              error_lead='Servidor não disponível',
                              modal_message='Não conseguimos obter sua \
                              geolocalização'
                              )
    post.save()
    return response


def make_post(request):
    r"""
    Call method to make the post depending on the request \
    method (GET or POST).
    """
    if request.method == 'GET':
        response = make_post_page(request)
    elif request.method == 'POST':
        response = make_post_action(request)
    return response

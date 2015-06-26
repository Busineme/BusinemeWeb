# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from models.user import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from controllers.utils import modal_message


def register_user_page(request):
    r"""
    Load the register user page. If a user is authenticated, it will be \
    redirected to the main page instead.
    """
    if request.user.is_authenticated():
        response = redirect("/",
                            context_instance=RequestContext(request))
    else:
        response = render_to_response('register_user_page.html',
                                      context_instance=RequestContext(request))
    return response


def register_user(request):
    r"""
    Register the user if all the data inserted in the forms are valid. The \
    email has to be unique, and with "@" and a "." (dot). The username has to \
    be unique. Finally, no fields can be blank.
    """
    user = User()
    user.first_name = request.POST["name"]
    user.email = request.POST["email"]
    user.username = request.POST["username"]
    user.set_password(request.POST["password"])
    try:
        if not user.validate_unique_email():
            response = modal_message(
                "Erro :(",
                "Email ja cadastrado.", "O e-mail inserido já \
                está em uso. Utilize um e-mail diferente para realizar o \
                cadastro.",
                "register_user_page.html", request)
            return response
        response = redirect("/login/",
                            context_instance=RequestContext(request))
        if not user.validate_email():
            response = modal_message(
                "Erro :(",
                "E-mail inválido.",
                "Verifique o e-mail inserido. Ele deve conter os caracteres \
                '@' e '.' (ponto).",
                "register_user_page.html", request)
        if not user.validate_user_password(request.POST["password"]):
            response = modal_message(
                "Erro :(",
                "Campo de senha vazio.",
                "Não é possível realizar o cadastro com a senha vazia, insira\
                 uma por favor.",
                "register_user_page.html", request)

        if user.validate_email() and user.validate_unique_email() and \
                user.validate_user_password(request.POST["password"]):
            user.save()

    except IntegrityError:
        if not user.validate_user_name():
            response = modal_message(
                "Erro :(",
                "Usuário já cadastrado.",
                "O nome de usuário inserido já está em uso.",
                "register_user_page.html", request)

    return response


def log_user(request):
    r"""
    Call method to log the user depending on the request \
    method (GET or POST).
    """
    if request.method == 'GET':
        response = log_user_get(request)
    elif request.method == 'POST':
        response = log_user_post(request)
    return response


def log_user_get(request):
    """Log the user with GET method, (load page)."""
    if request.user.is_authenticated():
        response = redirect("/",
                            context_instance=RequestContext(request))
    else:
        response = render_to_response('login_page.html',
                                      context_instance=RequestContext(request))
    return response


def log_user_post(request):
    r"""
    Log the user with POST method (action). Checks if user is deactivated \
    0and if username or password are incorrect.
    """
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            response = redirect('/', context_instance=RequestContext(request))
        else:
            response = modal_message(
                "Erro :(",
                "Usuário desativado.",
                "Esta usuário foi desativado.\
            Entre em contato com o suporte Busine.me para solicitar a\
             reativação.",
                "login_page.html", request)
    else:
        response = modal_message(
            "Erro :(",
            "Usuário não encontrado.",
            "Verifique se o nome de usuário e a senha informados estão\
             corretos.",
            "login_page.html", request)
    return response


@login_required
def logout_user(request):
    """Log user out."""
    logout(request)
    return redirect('/login/', context_instance=RequestContext(request))


@login_required
def user_account_page(request):
    """Load the account managment page, that lets the user change his data."""
    if request.user.is_authenticated():
        user = request.user
    return render_to_response('account_page.html', {'user': user},
                              context_instance=RequestContext(request))


@login_required
def change_password_page(request):
    r"""
    Load the password managment page, that lets the user change his \
    password.
    """
    if request.user.is_authenticated():
        user = request.user
    return render_to_response('change_password_page.html', {'user': user},
                              context_instance=RequestContext(request))


@login_required
def change_password_action(request):
    """Change user password checking for his current password."""
    if request.user.is_authenticated():
        user = request.user

    old_password = request.POST["old_password"]
    new_password1 = request.POST["new_password1"]
    new_password2 = request.POST["new_password2"]

    if not user.check_password(old_password):
        response = modal_message(
            "Erro :(",
            "Senha atual incorreta.",
            "Verifique a escrita da senha informada.",
            "change_password_page.html", request)
    else:
        if not (new_password1 == new_password2):
            response = modal_message(
                "Erro :(",
                "Os campos de nova senha não conferem.",
                "Verifique a escrita das senhas informadas.",
                "change_password_page.html", request)
        else:
            user.set_password(new_password1)
            user.save()
            response = redirect("/login/",
                                context_instance=RequestContext(request))
            logout(request)
    return response


@login_required
def change_userdata(request):
    """Change user data."""
    if request.user.is_authenticated():
        user = request.user
        user.first_name = request.POST["name"]
        user.email = request.POST["email"]
        user.save()
    return redirect("/",
                    context_instance=RequestContext(request))


@login_required
def deactivate_account_page(request):
    """Load user account deactivation page."""
    if request.user.is_authenticated():
        user = request.user
    return render_to_response('deactivate_account_page.html', {'user': user},
                              context_instance=RequestContext(request))


@login_required
def deactivate_account_action(request):
    """Deactivate user account checking for his current password."""
    user = request.user

    password = request.POST["password"]

    if not user.check_password(password):
        response = modal_message(
            "Erro :(",
            "Senha incorreta.",
            "Verifique a escrita da senha informada.",
            "deactivate_account_page.html", request)
    else:
        user.is_active = False
        user.save()
        logout(request)
        response = modal_message(
            "Sucesso!",
            "Usuário desativado com sucesso.",
            "Esperamos o seu retorno, até logo! :)",
            "login_page.html", request)
    return response


@login_required
def deactivate_account(request):
    """Call method to deactivate the user depending on the request method."""
    if request.method == 'GET':
        response = deactivate_account_page(request)
    elif request.method == 'POST':
        response = deactivate_account_action(request)
    return response


@login_required
def change_password(request):
    """Call method to user password depending on the request method."""
    if request.method == 'GET':
        response = change_password_page(request)
    if request.method == 'POST':
        response = change_password_action(request)
    return response

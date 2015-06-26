from models.favorite import Favorite
from models.busline import Busline
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect
from django.shortcuts import render_to_response


@login_required
def favorite_busline(request, line_number):
    """ Favorite a busline and check if the busline is already favorited. \
    If so, the method will unfavorite the busline """
    busline = Busline.get_by_line_equals(line_number)
    busline_id = busline.id
    user_id = request.user.id
    if not Favorite.is_favorite(user_id, busline_id):
        favorite = Favorite()
        favorite.user_id = user_id
        favorite.busline_id = busline.id
        favorite.save()
        return redirect(
            "/fav_page/",
            context_instance=RequestContext(request))
    else:
        Favorite.delete_favorite(user_id, busline_id)
        return redirect(
            "/fav_page/",
            context_instance=RequestContext(request))


@login_required
def unfavorite_busline(request, line_number):
    """ Unfavorite a busline """
    busline = Busline.get_by_line_equals(line_number)
    busline_id = busline.id
    user_id = request.user.id
    Favorite.delete_favorite(user_id, busline_id)
    return redirect(
        "/fav_page/",
        context_instance=RequestContext(request))


@login_required
def favorite_busline_page(request):
    """ Load the Favorites buslines page """
    favorites = Favorite.objects.filter(
        user_id=request.user).order_by("busline_id")

    return render_to_response("fav_page.html",
                              {'favorites': favorites},
                              context_instance=RequestContext(request))

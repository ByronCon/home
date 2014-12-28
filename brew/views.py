from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from brew.models import Recipe


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def wip(request):
    return HttpResponse("Hello, world. You're at a WIP page.")


# ## Recipe
# Index page
def recipe_index(request):
    recipe_list = Recipe.objects.all()
    context = {'recipe_list': recipe_list}
    return render(request, 'brew/recipe_index.html', context)

# Detail view of recipe
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'brew/recipe_detail.html', {'recipe': recipe})


def recipe_update(request, recipe_id):
    r = Recipe.objects.get(pk=1)
    return HttpResponse("You're trying to change " + r.name)


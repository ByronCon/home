from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse ,Http404
from django.contrib import messages
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.base import TemplateView

# Brew Models
from brew.models import Recipe, Batch, Bottling, BatchForm




# ## Generic Views
class HomePageView(TemplateView):
    template_name = "brew/index.html"


def wip(request):
    return HttpResponse("Hello, world. You're at a WIP page.")


def wip2(request, recipe_id):
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

# Recipe update -- doesn't exist?
def recipe_update(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'brew/recipe_detail.html', {
            'recipe': recipe,
            'error_message': "You are trying to change " + recipe.name,
        })


# ## Batch
# Index page
class BatchIndexView(generic.ListView):
    #template_name = 'brew/batch_index.html'
    #context_object_name = 'batch_list'

    def get_queryset(self):
        """Return all batches."""
        return Batch.objects.all()


# Batch Detail
class BatchDetailView(generic.DetailView):
    model = Batch


# Batch Update
def batch_create(request):
    # If POST, process data
    if request.method == 'POST':
        form = BatchForm(request.POST)
        # If valid data, process it
        if form.is_valid():
            form.save()
        messages.add_message(request, messages.INFO, 'Created new batch: ' + request.POST['name`'])
        return redirect('brew:batch_index')
    # If GET, display blank form
    else:
        form = BatchForm()

    return render(request, 'brew/batch_create.html', {'form': form})


# Testing update of existing
def batch_update(request, pk):
    # If POST, process data
    if request.method == 'POST':
        # Identify which Batch we're updating, then process
        b = Batch.objects.get(pk=pk)
        form = BatchForm(request.POST, instance=b)
        # If valid data, process it
        if form.is_valid():
            form.save()
            return HttpResponse("Trying to update. " + pk)
    # If GET, display blank form
    else:
        b = Batch.objects.get(pk=pk)
        form = BatchForm(instance=b)

    return render(request, 'brew/batch_update.html', {'form': form})


# Batch delete
def batch_delete(request, pk):
    Batch.objects.get(pk=pk).delete()
    messages.add_message(request, messages.INFO, 'Deleted ' + pk)
    return redirect('brew:batch_index')

# ## Bottling
class BottlingIndexView(generic.ListView):
    def get_queryset(self):
        """Return all bottlings."""
        return Bottling.objects.all()


class BottlingDetailView(generic.DetailView):
    model = Bottling


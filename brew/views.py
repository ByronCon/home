from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse ,Http404
from django.contrib import messages
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy   # need lazy as views imported before urls - ie; url reference doesn't yet exist

# Brew Models
from brew.models import Recipe, Batch, Bottling, BatchForm, MeasurementForm, GravityType, RecipeForm, BottlingForm



# ## Generic Views
@login_required
def home_page(request):
    """ Default home page - redirect if not logged in """
    if request.user.is_authenticated():
        return HttpResponse("Logged in as " + (request.user.username ))
    else:
        return HttpResponse("Not logged in: " + request.user.username)


class HomePageView(TemplateView):
    template_name = "brew/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomePageView, self).dispatch(*args, **kwargs)

def wip(request):
    return HttpResponse("Hello, world. You're at a WIP page.")


def wip2(request, recipe_id):
    return HttpResponse("Hello, world. You're at a WIP page.")


# ## Recipe
# Index page
class RecipeIndexView(generic.ListView):
    #template_name = 'brew/batch_index.html'
    #context_object_name = 'batch_list'

    def get_queryset(self):
        """Return all batches."""
        return Recipe.objects.all()


class RecipeDetailView(generic.DetailView):
    model = Batch


# Detail view of recipe
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'brew/recipe_detail.html', {'recipe': recipe})


# Create Recipe
class RecipeCreate(generic.CreateView):
    form_class = RecipeForm
    model = Recipe


# Update recipe
class RecipeUpdate(generic.UpdateView):
    form_class = RecipeForm
    model = Recipe


# Delete recipe
class RecipeDelete(generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy('brew:recipe_index')

# Recipe update -- doesn't exist?
#def recipe_update(request, recipe_id):
#    recipe = get_object_or_404(Recipe, pk=recipe_id)
#    return render(request, 'brew/recipe_detail.html', {
#            'recipe': recipe,
#            'error_message': "You are trying to change " + recipe.name,
#        })


# ## Batch
# Index page
class BatchIndexView(generic.ListView):
    model = Batch
    # Get Batches which are bottled
    #queryset = Batch.objects.filter(is_bottled)

    def get_context_data(self, **kwargs):
        context = super(BatchIndexView, self).get_context_data(**kwargs)
        # Get Batches which are not bottled
        #context['inactive_list'] = Batch.objects.filter(is_bottled)
        return context



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
            messages.add_message(request, messages.INFO, 'Created new batch: ' + request.POST['name'])
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
            messages.add_message(request, messages.INFO, 'Updated Batch: ' + request.POST['name'])
            return redirect('brew:batch_index')
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


### Measurements
# Create
def measure_create(request):
    # If POST, process data
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        # If valid data, process it
        if form.is_valid():
            form.save()
            batch = Batch.objects.get(pk=request.POST['batch'])
            gravity_type = str(GravityType.objects.get(pk=request.POST['gravity_type']))
            messages.add_message(request, messages.INFO, 'Created new ' + gravity_type + ' measurement for ' + str(batch) + ' it is ' + batch.state)
            return redirect('brew:batch_detail', batch.pk)
    # If GET, display blank form
    else:
        form = MeasurementForm()

    return render(request, 'brew/measure_create.html', {'form': form})


# ## Bottling
class BottlingIndexView(generic.ListView):
    model = Bottling

    def get_context_data(self, **kwargs):
        context = super(BottlingIndexView, self).get_context_data(**kwargs)
        context['available_list'] = Bottling.objects.filter(num_remaining=0)
        return context


class BottlingDetailView(generic.DetailView):
    model = Bottling


class BottlingCreateView(generic.CreateView):
    model = Bottling
    form_class = BottlingForm

### Drink
class DrinkIndexView(generic.ListView):
    model = Bottling
    queryset = Bottling.objects.filter(num_remaining__gt=0)
    template_name = "brew/drink_list.html"

    def get_context_data(self, **kwargs):
        context = super(DrinkIndexView, self).get_context_data(**kwargs)
        context['available_list'] = Bottling.objects.filter(num_remaining=0)
        return context


class DrinkDetailView(generic.DetailView):
    model = Bottling
    template_name = "brew/drink_detail.html"

# Update recipe
class DrinkUpdate(generic.UpdateView):
    #form_class = DrinkForm
    model = Bottling
    template_name = "brew/drink_form.html"


# recipes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Recipe, Ingredient, Step, Comment, Rating
from .forms import RecipeForm, IngredientForm, StepForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'comment':
            Comment.objects.create(
                recipe=recipe,
                author=request.POST.get('author', 'Anonymous'),
                text=request.POST.get('text', '')
            )
            return redirect('recipe_detail', pk=pk)

        if form_type == 'rating':
            score = int(request.POST.get('rating', 0))
            if 1 <= score <= 5:
                Rating.objects.create(recipe=recipe, score=score)
                scores = [r.score for r in recipe.ratings.all()]
                recipe.rating_avg = sum(scores) / len(scores)
                recipe.save()
            return redirect('recipe_detail', pk=pk)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': recipe.ingredients.all(),
        'steps': recipe.steps.all(),
        'comments': recipe.comments.order_by('-created_at'),
    })

def recipe_create(request):
    # Allow unlimited add via JS, start with 1 blank
    IngredientFormSet = modelformset_factory(Ingredient, form=IngredientForm, extra=1)
    StepFormSet       = modelformset_factory(Step, form=StepForm, extra=1)

    if request.method == 'POST':
        form     = RecipeForm(request.POST, request.FILES)
        ing_set  = IngredientFormSet(request.POST, queryset=Ingredient.objects.none(), prefix='ing')
        step_set = StepFormSet(request.POST, queryset=Step.objects.none(), prefix='step')

        if form.is_valid() and ing_set.is_valid() and step_set.is_valid():
            recipe = form.save()

            for f in ing_set:
                if f.cleaned_data:
                    obj = f.save(commit=False)
                    obj.recipe = recipe
                    obj.save()

            for f in step_set:
                if f.cleaned_data:
                    obj = f.save(commit=False)
                    obj.recipe = recipe
                    obj.save()

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form     = RecipeForm()
        ing_set  = IngredientFormSet(queryset=Ingredient.objects.none(), prefix='ing')
        step_set = StepFormSet(queryset=Step.objects.none(), prefix='step')

    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'ing_set': ing_set,
        'step_set': step_set,
        'ing_empty': ing_set.empty_form,
        'step_empty': step_set.empty_form,
    })

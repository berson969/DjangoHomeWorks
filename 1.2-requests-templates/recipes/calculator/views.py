from django.shortcuts import render
from django.urls import reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, kг': 0.3,
        'сыр, kг': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def start_page(request):
    context = {
        'recipes': DATA.keys()
    }
    return render(request, 'calculator/home.html', context)


def select_recipe(request, name_dish):
    servings = int(request.GET.get('servings', 1))
    calc_dish = {key: '%.2f' % (value*servings) for key, value in DATA[name_dish].items()}
    context = {
        'name': name_dish,
        'servings': servings,
        'recipe': calc_dish,
        'to_home': reverse('home')
    }
    return render(request, 'calculator/index.html', context)

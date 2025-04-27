from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import CarModel, News, CarSeries
from django.contrib.auth.decorators import login_required


def index(request):
    latest_news = News.objects.order_by('-date_published')[:3]
    featured_models = CarModel.objects.order_by('?')[:3]
    return render(request, 'cars/index.html', {
        'latest_news': latest_news,
        'featured_models': featured_models
    })


def model_list(request):
    series = CarSeries.objects.prefetch_related('carmodel_set').all()
    all_series = CarSeries.objects.all()
    selected_series = request.GET.get('series')

    if selected_series and selected_series != 'all':
        series = series.filter(id=int(selected_series))

    return render(request, 'cars/models.html', {
        'series': series,
        'all_series': all_series
    })


def model_detail(request, model_id):
    car_model = get_object_or_404(CarModel, pk=model_id)
    related_models = CarModel.objects.filter(
        series=car_model.series
    ).exclude(id=model_id)[:4]

    return render(request, 'cars/detail.html', {
        'model': car_model,
        'related_models': related_models
    })


def news_list(request):
    news = News.objects.order_by('-date_published')
    return render(request, 'cars/news.html', {'news': news})


@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'cars/register.html', {'form': form})
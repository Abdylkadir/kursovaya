from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

import csv

from .models import Location, Genre


def export_to_csv(request):
    locations = Location.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=locations_export.csv; encoding="cp1251"; newline="";'
    writer = csv.writer(response)
    writer.writerow(['Название', 'Описание',
                    'Изображение' 'Ссылка'])
    locations_fields = locations.values_list('title', 'description',
                                             'imageLocation', 'url')
    for location in locations_fields:
        writer.writerow(location)
    return response


class GenreCount:

    def get_genres(self):
        return Genre.objects.all()

    def get_counts(self):
        return Location.objects.filter(draft=False).values('count')


class LocationsView(GenreCount, ListView):

    model = Location
    queryset = Location.objects.filter(draft=False)
    paginate_by = 1
    # template_name = 'locations/locations.html'

    # def get_context_data(self, *args, ** kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

    # def get(self, request):
    #     locations = Location.objects.all()
    #     return render(request, "locations/locations.html", {"location_list": locations})


class LocationDetailView(GenreCount, DetailView):

    model = Location
    slug_field = 'url'

    # def get(self, request, slug):
    #     locations = Location.objects.get(url=slug)
    #     return render(request, "locations/location_detail.html", {"location": locations})


class FilterLocationView(GenreCount, ListView):
    """Фильтр локаций"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Location.objects.filter(
            Q(count__in=self.request.GET.getlist('count')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = ''.join(
            [f'count={x}&' for x in self.request.GET.getlist('count')])
        context["genre"] = ''.join(
            [f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return context


class Search(ListView):
    """Поиск Локаций"""
    paginate_by = 2

    def get_queryset(self):
        return Location.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	GeoNamesPlace,
)


class GeoNamesPlaceCreateView(CreateView):

    model = GeoNamesPlace


class GeoNamesPlaceDeleteView(DeleteView):

    model = GeoNamesPlace


class GeoNamesPlaceDetailView(DetailView):

    model = GeoNamesPlace


class GeoNamesPlaceUpdateView(UpdateView):

    model = GeoNamesPlace


class GeoNamesPlaceListView(ListView):

    model = GeoNamesPlace


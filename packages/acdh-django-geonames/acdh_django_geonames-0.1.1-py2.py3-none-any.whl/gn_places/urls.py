# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'gn_places'
urlpatterns = [
    url(
        regex="^GeoNamesPlace/~create/$",
        view=views.GeoNamesPlaceCreateView.as_view(),
        name='GeoNamesPlace_create',
    ),
    url(
        regex="^GeoNamesPlace/(?P<pk>\d+)/~delete/$",
        view=views.GeoNamesPlaceDeleteView.as_view(),
        name='GeoNamesPlace_delete',
    ),
    url(
        regex="^GeoNamesPlace/(?P<pk>\d+)/$",
        view=views.GeoNamesPlaceDetailView.as_view(),
        name='GeoNamesPlace_detail',
    ),
    url(
        regex="^GeoNamesPlace/(?P<pk>\d+)/~update/$",
        view=views.GeoNamesPlaceUpdateView.as_view(),
        name='GeoNamesPlace_update',
    ),
    url(
        regex="^GeoNamesPlace/$",
        view=views.GeoNamesPlaceListView.as_view(),
        name='GeoNamesPlace_list',
    ),
	]

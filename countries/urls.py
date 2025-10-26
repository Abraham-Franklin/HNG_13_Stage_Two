# from django.urls import path
# from .views import RefreshCountryView, CountryListView, CountryDetailView, StatusView, SummaryImageView

# urlpatterns = [
#     path('countries/refresh', RefreshCountryView.as_view(), name='refresh-countries'),
#     path('countries', CountryListView.as_view(), name='list-countries'),
#     path('countries/<str:name>', CountryDetailView.as_view(), name='country-detail'),
#     path('status', StatusView.as_view(), name='status'),
#     path('countries/image', SummaryImageView.as_view(), name='summary-image'),
# ]


from django.urls import path
from .views import (
    RefreshCountryView,
    CountryListView,
    CountryDetailView,
    StatusView,
    SummaryImageView,
)

urlpatterns = [
    path('countries/refresh/', RefreshCountryView.as_view(), name='refresh-countries'),
    path('countries/refresh', RefreshCountryView.as_view(), name='refresh-countries'),

    path('countries/', CountryListView.as_view(), name='list-countries'),
    path('countries', CountryListView.as_view(), name='list-countries'),

    path('countries/<str:name>/', CountryDetailView.as_view(), name='country-detail'),
    path('countries/<str:name>', CountryDetailView.as_view(), name='country-detail'),

    path('status/', StatusView.as_view(), name='status'),
    path('status', StatusView.as_view(), name='status'),

    path('countries/image/', SummaryImageView.as_view(), name='summary-image'),
    path('countries/image', SummaryImageView.as_view(), name='summary-image'),
]

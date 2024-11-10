from django.urls import path
from .views import scrape_data_view

urlpatterns = [
    path('', scrape_data_view, name='home'),  # Home page with default size
    path('products/size/<int:size>/', scrape_data_view, name='product_size')  # Route for specific size
]

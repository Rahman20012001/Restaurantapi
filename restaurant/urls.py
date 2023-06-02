from django.urls import include, path
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.MenuItemsView.as_view()),
    path('booking/', views.BookingViewSet.as_view()),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    path('message/', views.msg),
    path('api-token-auth/', obtain_auth_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

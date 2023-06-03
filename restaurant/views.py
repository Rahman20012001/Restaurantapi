from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Menu, Booking
from rest_framework import generics
from .serializers import MenuSerializer, BookingSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.throttling import UserRateThrottle

# Create your views here.

def home(request):
    return render(request, 'home.html')


class MenuItemsPagination(PageNumberPagination):
    page_size = 10


class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = MenuItemsPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'price']
    search_fields = ['title']  # Adjust the fields according to your model

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply filters based on query parameters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
@throttle_classes([UserRateThrottle])  # Add throttling to this view
def msg(request):
    return Response({"message": "This view is protected"})

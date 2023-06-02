from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Menu, Booking
from rest_framework import generics
from .serializers import MenuSerializer, BookingSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination

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
    
def get_queryset(self):
    queryset = super().get_queryset()
    search_term = self.request.query_params.get('search', None)
    if search_term:
        queryset = queryset.filter(name__icontains=search_term)
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
def msg(request):
    return Response({"message": "This view is protected"})
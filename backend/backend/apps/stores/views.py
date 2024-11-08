# backend/apps/store/views.py
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework import viewsets
from rest_framework import generics # type: ignore
from .models import Store
from .serializers import StoreSerializer
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.permissions import AllowAny

from backend.apps.users.models import User
from backend.apps.users.serializers import UserSerializer
from django.utils.text import slugify

import uuid


# for multiple store view
class MyStoresDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # user_id = User.objects.get(email=user)
        store = Store.objects.filter(user=user.id)
        mystore = StoreSerializer(store, many=True)
        return Response({'mystore':mystore.data}, status=status.HTTP_200_OK)

# for single store view
class MyStoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def is_valid_uuid(self, uuid_string):
        try:
            uuid_obj = uuid.UUID(uuid_string, version=4)  # You can specify the version you want
        except ValueError:
            return False
        return str(uuid_obj) == uuid_string

    def get(self, request):
        try:
            store_id = request.GET.get('store_id')
            if store_id and self.is_valid_uuid(store_id):
                user = request.user
                # user_id = User.objects.get(email=user)
                store = Store.objects.filter(user=user.id, id=store_id)
                mystore = StoreSerializer(store, many=True)
                return Response({'mystore':mystore.data}, status=status.HTTP_200_OK)
            
            return Response({'error':'store_id is required or value error'}, status=status.HTTP_400_BAD_REQUEST)
        except Store.DoesNotExist:
            return Response({'error':'Something went wrong or there is no store created'}, status=status.HTTP_400_BAD_REQUEST)



class StoreCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can create a store
    # permission_classes = [AllowAny]
    def post(self, request):
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        stores_with_products = Store.objects.prefetch_related('product_store').all()
        serializer = StoreSerializer(stores_with_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    # def list(self, request, *args, **kwargs):
    #     return Response({"message":"this is get method"}, status = status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            if Store.objects.filter(owner=request.user).exists():
                return Response({"message":"You Can't Create Store More Than One"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


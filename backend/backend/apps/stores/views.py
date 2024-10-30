# backend/apps/store/views.py
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.views import APIView # type: ignore

from rest_framework import generics # type: ignore
from .models import Store
from .serializers import StoreSerializer
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.permissions import AllowAny

from backend.apps.users.models import User
from backend.apps.users.serializers import UserSerializer


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
        store = Store.objects.all()

        serializer = StoreSerializer(store, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# class StoreCreateView(APIView):
#     # permission_classes = [IsAuthenticated]  # Only authenticated users can create a store
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = StoreSerializer(data=request.data)
#         user = User.objects.filter(id="d9b9962e-50e1-428a-b68a-198124ee9ddb")
#         # userSerializer = UserSerializer(user, many=True)
#         if serializer.is_valid():
#             serializer.save(owner=user)  # Set the owner to the authenticated user
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(vendor=self.request.user.vendor)  # Assumes user has a related vendor

from django.shortcuts import render
from rest_framework import viewsets, mixins
from django.views.generic import View
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import * 

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class RestoransViewSet(viewsets.ModelViewSet):
    queryset = Restoran.objects.all()
    serializer_class = RestoranSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class ClientViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = ClientSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id, 'status': user.status}, status=200)

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        logout(request)
        return Response(status=204)


# {
#     'table', number_table
# }
class TableControlViewSet(APIView):
    def post(self, request, r_id):
        restoran = Restoran.objects.filter(id=r_id).first()
        unit_table = int(data['table'])
        tables = Table.objects.filter(restoran=restoran).last()
        for i in range(0, unit_table):
            table = Table(restoran=restoran, number=tables.number+i+1)
            table.save()
        restoran.tables += unit_table
        restoran.save()
        return Response({'status':'success add tables'})

    def delete(self, request, r_id):
        restoran = Restoran.objects.filter(id=r_id).first()
        table = Table.objects.filter(restoran=restoran).last()
        table.delete()
        restoran.tables -= 1
        restoran.save()
        return Response({'status':'success delete table'})


# Detail Product

class RestoranProductDetailViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        p_id = self.kwargs['p_id']
        r_id = self.kwargs['r_id']
        return Product.objects.filter(id=p_id, category__restoran__id=r_id)
    

# lists Product

class RestoranProductsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        r_id = self.kwargs['r_id']
        return Product.objects.filter(category__restoran__id=r_id)


class RsCtgProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        c_id = self.kwargs['c_id']
        return Product.objects.filter(category__id=c_id)


# lists Workers

class WorkerListsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        r_id = self.kwargs['r_id']
        return UserProfile.objects.filter(restoran=r_id)

# lists Category

class CategoryListsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        r_id = self.kwargs['r_id']
        return Category.objects.filter(restoran__id=r_id)


# Worker Get Post Methods

class WorkerControlViewSet(APIView):
    def get(self, request, w_id, r_id):
        w = UserProfile.objects.filter(restoran=r_id ,id=w_id, status=1).first()
        if w is None:
            return Response({'status': 'Error :('})
        w_json = {
            'username': w.username,
            'email': w.email,
            'phone': w.mobile,
            'avatar': w.avatar.url,
            'duty': w.duty,
            'last_name': w.last_name,
            'restoran': w.restoran,
            'wage': w.wage,
            'wage_type': w.wage_type
        }
        return Response(w_json)


    def put(self, request, w_id, r_id):
        data = request.data
        w = UserProfile.objects.filter(restoran=r_id, id=w_id).first()
        if w is None:
            return Response({'status':'Error.   :('})
        username = data['username']
        email = data['email']
        phone = data['phone']
        last_name = data['last_name']
        wage_type = data['wage_type']
        wage = data['wage']
        duty = data['duty']
        w_test = UserProfile.objects.filter(username=username).first()
        if w_test:
            if w_test != w:
                return Response({'status':'Error. This is username is corrected'})
        w.username = username
        w.email = email
        w.mobile = phone
        w.last_name = last_name
        w.wage_type = wage_type
        w.wage = wage
        w.duty = duty
        w.save()
        return Response({"status": 'Success!!! :)'})


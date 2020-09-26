from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from app.serializers import CategorySerializer, ProductSerializer
from app.models import Category, Product, Table, UserProfile
from .models import TableProducts
from .serializers import TableProductsSerializer
from django.utils import timezone
# Create your views here.


class RestoranTablesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        r_id = self.kwargs['restoran_id']
        return Category.objects.filter(restoran__id=r_id)

class ProductListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        c_id = self.kwargs['c_id']
        return Product.objects.filter(category__id=c_id)

class ProductDetailViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        p_id = self.kwargs['p_id']
        return Product.objects.filter(id=p_id)

class DeleteTableProduct(APIView):
    def delete(self, request, t_p_id):
        t_p = Table.objects.filter(id=t_p_id, recd=1, display=1).first()
        if t_p is not None:
            if t_p.unit == 1:
                t_p.delete()
                return Response({'msg': 'deleted'})
            elif t_p.unit > 1:
                t_p.unit -= 1
                t_p.save()
                return Response({'msg': 'subtruction'})
        else:
            return Response({'msg':'this is object do not live'})
























class NewRestoranTableDetailViewSet(APIView):
    def get(self, request, r_id, t_n):
        # data = request.data
        # client = UserProfile.objects.filter(id=int(data['client_id'])).first()
        table = Table.objects.filter(restoran__id=int(r_id), number=int(t_n)).first()
        output_json = []
        products = []
        for j in TableProducts.objects.filter(table=table.id, status=1, display=1, recd=2):
            try:
                a = j.product.image.url
            except:
                a = 'default'
            products.append({
                "name": j.product.name,
                "price": j.product.price,
                "unit" : j.unit,
                "image" : a
            })
        output_json.append({
            'table': table.number,
            'status': table.color,
            'products': products
        })
        return Response(output_json)



class NewRestoranTablesViewSet(APIView):
    def get(self, request, r_id):
        # data = request.data
        # client = UserProfile.objects.filter(id=int(data['client_id'])).first()
        tables = Table.objects.filter(restoran__id=int(r_id))
        output_json = []
        item_json = {}
        for i in tables:
            item_json['table'] = i.number
            item_json['status'] = i.color
            products = []
            for j in TableProducts.objects.filter(table=i.id, status=1, display=1, recd=2):
                try:
                    a = j.product.image.url
                except:
                    a = 'default'
                products.append({
                    "name": j.product.name,
                    "price": j.product.price,
                    "unit" : j.unit,
                    "image" : a
                })
            item_json['products'] = products
            output_json.append({
                'table': i.number,
                'status': i.color,
                'products': products
            })
        return Response(output_json)

    def put(self, request, r_id):
        data = request.data
        client = UserProfile.objects.filter(id=int(data['client_id'])).first()
        table = Table.objects.filter(restoran__id=int(r_id), number=data['table']).first()
        sts = data['status']
        if table.color == 'empty':
            if sts == 'scanned':
                now = timezone.localtime(timezone.now())
                table.user = client.id
                table.color = sts
                table.date = now
                table.save()
                return Response({'status': 'success'})
            else:
                return Response({'status': 'error'})
        else:
            if sts == 'scanned':
                return Response({'status': 'success', 'msg': 'read'})
            if table.user != client.id:
                return Response({'status': 'error'})
            if sts == 'ordered':
                table.color = sts
                table.save()
                return Response({'status': 'success'})
            if sts == 'reordered':
                table.color = sts
                table.save()
                return Response({'status': 'success'})
            if sts == 'bill_requested':
                table.color = sts
                table.save()
                return Response({'status': 'success'})
            if sts == 'empty':
                if table.color == 'order_cancelled':
                    table.color = sts
                    table.save()
            return Response({'status': 'error'})


class ListTableProductsViewSet(APIView):
    # def get_queryset(self):
    #     r_id = self.kwargs['r_id']
    #     t_n = self.kwargs['t_n']
    #     table = Table.objects.filter(restoran__id=int(r_id), number=int(t_n)).first()
    #     return TableProducts.objects.filter(table=table.id, display=1)
    def get(self, request, r_id, t_n):
        table = Table.objects.filter(restoran__id=int(r_id), number=int(t_n)).first()
        objs = TableProducts.objects.filter(table=table.id, display=1, recd=1)
        u_json = []
        for i in objs:
            a = {
                'id': i.id,
                'table': i.table,
                'product': {
                    'id': i.product.id,
                    'name': i.product.name,
                    'price': i.product.price
                },
                'unit': i.unit,
                'status': i.status
            }
            u_json.append(a)
        return Response(u_json)
    
    def post(self, request, r_id, t_n):
        table = Table.objects.filter(restoran__id=r_id, number=t_n).first()
        if table is None:
            return Response({'status': 'error', 'msg':'This is table not'})
        data = request.data
        client = int(data['client'])
        c = UserProfile.objects.filter(id=client).first()
        if table.user is not None:
            if table.user != c.id:
                return Response({'status': 'error'})
        objs = TableProducts.objects.filter(table=table.id, display=1, recd=1)
        for i in data['products']:
            p = Product.objects.filter(id=i['product']).first()
            if p is not None:
                a=0
                for j in objs:
                    if p.id == j.product.id:
                        j.unit += int(i['unit'])
                        j.save()
                        a=1
                    if a==1:
                        break
                if a == 0:
                    code = (str(table.date.year)[2:]+str(table.date.month)+str(table.date.day)+str(table.date.hour)+str(table.date.minute)+str(table.date.second)+str(table.date.microsecond))
                    t_p = TableProducts(table=table.id, product=p, unit=i['unit'], client=c, recd=1, code_order=code)
                    t_p.save()
        return Response({'msg':'success'}, status=200)


class HistoryesTableProductsViewSet(APIView):
    # def get_queryset(self):
    #     c_id = self.kwargs['client_id']
    #     client = UserProfile.objects.filter(id=c_id).first()
    #     return TableProducts.objects.filter(client=client, display=2)

    def get(self, request, client_id):
        client = UserProfile.objects.filter(id=client_id).first()
        objs = TableProducts.objects.filter(client=client, display=2)
        lists = set(TableProducts.objects.values_list('code_order', flat=True))
        u_json = []
        print(lists)
        for j in lists:
            products = []
            p_ls = objs.filter(code_order=j)
            t_s = 0
            for i in p_ls:
                a = {
                    'id': i.product.id,
                    'name': i.product.name,
                    'price': i.product.price,
                    'unit': i.unit,
                    'date': i.data
                }
                t_s += int(i.product.price)*float(i.unit)
                products.append(a)
            u_json.append({
                'code': j,
                'restaurant_name': p_ls[0].product.category.restoran.name,
                'total_sum': t_s,
                'products': products
            })
        return Response(u_json)

class HistoryDetailTableProductsViewSet(APIView):
    # def get_queryset(self):
    #     c_id = self.kwargs['client_id']
    #     client = UserProfile.objects.filter(id=c_id).first()
    #     return TableProducts.objects.filter(client=client, display=2)

    def get(self, request, client_id, h_code):
        client = UserProfile.objects.filter(id=client_id).first()
        objs = TableProducts.objects.filter(client=client, display=2)
        products = []
        p_ls = objs.filter(code_order=h_code)
        t_s = 0
        for i in p_ls:
            a = {
                'id': i.product.id,
                'name': i.product.name,
                'price': i.product.price,
                'unit': i.unit,
                'date': i.data
            }
            t_s += int(i.product.price)*float(i.unit)
            products.append(a)
        u_json = {
            'code': h_code,
            'restaurant_name': p_ls[0].product.category.restoran.name,
            'total_sum': t_s,
            'products': products
        }
        return Response(u_json)




































        



# Profile 

class ClientProfileViewSet(APIView):
    def get(self, request, u_id):
        u = UserProfile.objects.filter(id=u_id).first()
        u_json = {
            'username': u.username,
            'email': u.email,
            'phone': u.mobile,
            'avatar': u.avatar.url,
            # 'status': u.status,
            'last_name': u.last_name,
        }
        return Response(u_json)
    
    def put(self, request, u_id):
        data = request.data
        u = UserProfile.objects.filter(id=u_id).first()
        username = data['username']
        email = data['email']
        phone = data['phone']
        last_name = data['last_name']
        u_test = UserProfile.objects.filter(username=username).first()
        if u_test:
            if u_test != u:
                return Response({'status':'error'})
        u.username = username
        u.email = email
        u.mobile = phone
        u.last_name = last_name
        u.save()
        return Response({"status": 'success'})

# {
#     "password":"passwordtext"
#     'new_password':"passwordtext",
#     "new_password2":"passwordtextsecond",
# }
class ClientEditPassword(APIView):
    def post(self, request, u_id):
        data = request.data
        u = UserProfile.objects.filter(id=u_id).first()
        password = data['password']
        user = authenticate(username=u.username, password=password)
        if user is None:
            return Response({"status": 'error'})
        new_password = data['new_password']
        new_password2 = data['new_password2']
        if new_password != new_password2:
            return Response({"status": 'error'})
        u.set_password(new_password)
        u.save()
        return Response({"status": 'success'})
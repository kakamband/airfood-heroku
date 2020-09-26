from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Table, UserProfile
from client_app.models import TableProducts
from app.serializers import TableSerializers
# Create your views here.



class TableViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TableSerializers
    
    def get_queryset(self):
        r_id = self.kwargs['r_id']
        return Table.objects.filter(restoran__id=r_id)
    


class New_RestoranTableDetailViewSet(APIView):
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

class New_RestoranTablesViewSet(APIView):
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
        waiter = UserProfile.objects.filter(id=int(data['waiter_id'])).first()
        table = Table.objects.filter(restoran__id=int(r_id), number=data['table']).first()
        sts = data['status']
        if table.color == 'ordered':
            t_prds = TableProducts.objects.filter(table=table.id, status=1, display=1, recd=1)
            if sts == 'order_accepted':
                for i in t_prds:
                    i.recd = 2
                    i.save()
                table.waiter = waiter.id
                table.color = sts
                table.save()
                return Response({'status': 'success'})
            elif sts == 'order_cancelled':
                for i in t_prds:
                    i.delete()
                table.color = sts
                table.save()
                return Response({'status': 'error'})
        elif table.color == 'reordered':
            if table.waiter != waiter.id:
                return Response({'status': 'error'})
            t_prds = TableProducts.objects.filter(table=table.id, status=1, display=1, recd=1)
            if sts == 'reorder_accepted':
                for i in t_prds:
                    i.recd = 2
                    i.save()
                table.waiter = waiter.id
                table.color = sts
                table.save()
                return Response({'status': 'success'})
            elif sts == 'reorder_cancelled':
                for i in t_prds:
                    i.delete()
                table.color = sts
                table.save()
                return Response({'status': 'error'})
        # elif table.color == 'bill_requested':
        if table.waiter != waiter.id:
            return Response({'status': 'error'})
        if sts == 'bill_closed':
            t_prds = TableProducts.objects.filter(table=table.id, status=1, display=1, recd=2)
            for i in t_prds:
                i.display = 2
                i.save()
            table.user = None
            table.waiter = None
            table.color = 'empty'
            table.save()
            return Response({'status': 'success'})
        return Response({'status': 'error'})

            
                


































# cook
# {
#     "t_product_id": t_product.id
# }

class CookViewSet(APIView):
    def post(self, request, r_id, t_n):
        data = request.data
        table = Table.objects.filter(restoran__id=r_id, number=t_n).first()
        t_product = TableProducts.objects.filter(table=table.id, id=int(data['waiter_id']))
        if t_product.status == 1:
            t_product.status = 2
            t_product.save()
            return Response({'status':'success'})
        else:
            return Response({'status':'error'})



# Profile

class WorkerProfileViewSet(APIView):
    def get(self, request, w_id):
        w = UserProfile.objects.filter(id=w_id, status=1).first()
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


    def put(self, request, w_id):
        data = request.data
        w = UserProfile.objects.filter(id=w_id).first()
        username = data['username']
        email = data['email']
        phone = data['phone']
        last_name = data['last_name']
        w_test = UserProfile.objects.filter(username=username).first()
        if w_test:
            if w_test != w:
                return Response({'status':'Error. This is username is corrected'})
        w.username = username
        w.email = email
        w.mobile = phone
        w.last_name = last_name
        w.save()
        return Response({"status": 'Success!!! :)'})


# {
#     "password":"passwordtext"
#     'new_password':"passwordtext",
#     "new_password2":"passwordtextsecond",
# }
class WorkerEditPassword(APIView):
    def post(self, request, w_id):
        data = request.data
        w = UserProfile.objects.filter(id=w_id).first()
        password = data['password']
        worker = authenticate(username=w.username, password=password)
        if worker is None:
            return Response({"status": ' :|  Error. :( '})
        new_password = data['new_password']
        new_password2 = data['new_password2']
        if new_password != new_password2:
            return Response({"status": ' :|  Error.(1 != 2) :( '})
        w.set_password(new_password)
        w.save()
        return Response({"status": 'Success!!! :)'})
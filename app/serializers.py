from rest_framework import serializers

from .models import Category, Restoran, Product, Table, UserProfile, WorkTimes
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions



UserProfile = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserProfile(
            username=validated_data['username'],
            email = validated_data['email'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile'],
            avatar=validated_data['avatar'],
            wage_type=validated_data['wage_type'],
            wage=validated_data['wage'],
            duty=validated_data['duty'],
            status=1,
            restoran=validated_data['restoran'],
        )
        user.set_password(validated_data['password'])
        user.save()
        for i in range(1, 8):
            a = WorkTimes(worker=user, week=i)
            a.save()
        return user

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'last_name', 'password', 'mobile', 'avatar', 'wage_type', 'wage', 'duty', 'status', 'restoran')

class ClientSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserProfile(
            username=validated_data['username'],
            email = validated_data['email'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile'],
            avatar=validated_data['avatar'],
            status=2,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'last_name', 'password', 'mobile', 'avatar', )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated. "
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials. "
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both. "
            raise exceptions.ValidationError(msg)
        return data





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'restoran', )




class RestoranSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        restoran = Restoran(name=validated_data['name'], image=validated_data['image'], tables=validated_data['tables'])
        restoran.save()
        for i in range(0,restoran.tables):
            t = Table(number=i+1, restoran=restoran)
            t.save()
        return restoran
        
    class Meta:
        model = Restoran
        fields = ('id', 'name', 'image', 'tables', )




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'body', 'status', 'unit', 'price', 'image', 'category', )


class TableSerializers(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'number', 'restoran', 'color', 'user', )
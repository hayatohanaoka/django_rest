from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib import auth

from second_rest_api.models import Item, Product

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.get_user_model()
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        """
        Django の UserManager が持っている保存メソッドを使用する
        利点： パスワード暗号化保存が使える
        詳しくはドキュメントを参照
        https://docs.djangoproject.com/en/5.0/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
        """
        user = auth.get_user_model()
        return user.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


def min_price_for_discounted(value):
    if value <= 100:
        raise serializers.ValidationError('割引後の価格は100円以下にはなりません')


# Model serializers を使ってみる
class ItemModelSerializer(serializers.ModelSerializer):
    """
    ModelSerializerを継承すると、デフォルトで createメソッド と updateメソッド が定義された状態になる
    ModelSerializer は、 Serializer のサブクラス！
    """
    discounted_price = serializers.IntegerField(
        min_value=0, validators=[min_price_for_discounted])
    class Meta:
        model = Item  # Item をもとに serializer を定義
        # fields = '__all__'
        fields = ['id', 'name', 'price',    'discounted_price']
        # read_only_fields = ['price'] # ここに必須項目を設定すると、POSTでの登録時にエラーになる
        extra_kwargs = {  # 各引数への追加オプション
            'name': {
                'write_only': True,  # 書き込み専用（読み込み時には値が表示されない）
                'required': False
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=['name', 'price'],
                message='name と price の両方の値が同じアイテムを登録しないでください'
            )
        ]
    
    # バリデーションメソッド
    def validate_price(self, value):
        if self.partial and value is None:
            return value
        if value % 10 != 0:
            raise serializers.ValidationError('1桁目は0にしてください')
        return value
    
    def validate_names(self, value):
        if self.partial and value is None:
            return value
        if value[0].is_lower == 'a':
            raise serializers.ValidationError('1文字目はa以外にして下さい')
        return value
    
    def validate(self, data):
        price = data['price'] if 'price' in data.keys() else self.instance.price
        discounted_price = data['discounted_price'] \
            if 'discounted_price' in data.keys() else self.instance.discounted_price
        
        if price < discounted_price:
            raise serializers.ValidationError('割引価格は低kがよりも低い値に設定してください')
        return data
    
    # def create(self, validated_data):
    #     return Item.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     if 'name' in validated_data.keys():
    #         instance.name = validated_data['name']
    
    #     if 'price' in validated_data.keys():
    #         instance.price = validated_data['price']
    
    #     if 'discounted_price' in validated_data.keys():
    #         instance.discounted_price = validated_data['discounted_price']
    
    #     instance.save()
    #     return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, data):
        data_keys = data.keys()
        if 'username' not in data_keys or 'password' not in data_keys:
            raise serializers.ValidationError('ログイン情報が不足しています')
        return data

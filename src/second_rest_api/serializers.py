from rest_framework import serializers
from .models import Item

def min_price_for_discounted(value):
    if value <= 100:
        raise serializers.ValidationError('割引後の価格は100円以下にはなりません')


class ItemSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    price = serializers.IntegerField(min_value=0)
    discounted_price = serializers.IntegerField(min_value=0, validators=[min_price_for_discounted])
    
    # バリデーションメソッド
    def validate_price(self, value):
        if value % 10 != 0:
            raise serializers.ValidationError('1桁目は0にしてください')
        return value
    
    def validate_names(self, value):
        if value[0].is_lower == 'a':
            raise serializers.ValidationError('1文字目はa以外にして下さい')
        return value
    
    def validate(self, data):
        price = data['price']
        discounted_price = data['discounted_price']
        if price < discounted_price:
            raise serializers.ValidationError('割引価格は低kがよりも低い値に設定してください')
        return data
    
    # CRUD メソッド
    def create(self, validated_data):
        print('create is running')
        print(validated_data)
        return Item.objects.create(**validated_data)

    def update(self, validated_data):
        print('update is running')

    def delete(self, validated_data):
        print('delete is running')

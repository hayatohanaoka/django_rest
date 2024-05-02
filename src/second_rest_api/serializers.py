from rest_framework import serializers
from .models import Item

def min_price_for_discounted(value):
    if value <= 100:
        raise serializers.ValidationError('割引後の価格は100円以下にはなりません')


class ItemSerializers(serializers.Serializer):
    # id = serializers.ReadOnlyField()
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=20)
    price = serializers.IntegerField(min_value=0)
    discounted_price = serializers.IntegerField(min_value=0, validators=[min_price_for_discounted])
    
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
    
    # CRUD メソッド（D はなし）
    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data.keys():
            instance.name = validated_data['name']
        
        if 'price' in validated_data.keys():
            instance.price = validated_data['price']
        
        if 'discounted_price' in validated_data.keys():
            instance.discounted_price = validated_data['discounted_price']
        
        instance.save()
        return instance

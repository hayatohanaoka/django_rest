from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from second_rest_api.models import Item

def min_price_for_discounted(value):
    if value <= 100:
        raise serializers.ValidationError('割引後の価格は100円以下にはなりません')


# Model serializers を使ってみる
class ItemModelSerializers(serializers.ModelSerializer):
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

from django.db.models import Avg
from rest_framework import serializers
from applications.product.models import Product, Comment, Like, Rating, Image


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        files_data = request.FILES
        post = Product.objects.create(**validated_data)

        for image in files_data.getlist('images'):
            Image.objects.create(post=post, image=image)
        return post

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.filter(like=True).count()
        rep['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return rep



    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(rep)
        if not instance.parent:
            rep.pop('parent')
        return rep


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField()
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['rating']


class OrderSerializer(serializers.ModelSerializer):
    pass


class ProductSerializer(serializers.ModelSerializer):
    image = ser
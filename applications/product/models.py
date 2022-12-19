from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Post')
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

    # def save(self):
    #     pass


class Image(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comment', null=True)
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.username} {self.post.title}"


class Like(models.Model):
    """
    likes model
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')  # Post.objects.likes
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} -> {self.like}'


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], blank=True, null=True
    )

    def __str__(self):
        return f'{self.owner} -> {self.rating}'


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product_obj = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    amount = models.PositiveIntegerField(default=1)
    order = models.BooleanField(default=False)
    order_code = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f'{self.owner} - {self.product_obj}'

    def create_order_code(self):
        import uuid
        self.order_code = str(uuid.uuid4())

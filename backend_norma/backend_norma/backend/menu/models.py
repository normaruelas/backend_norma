from django.db import models

class Category(models.Model):
    key = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Variant(models.Model):
    key = models.SlugField(unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Size(models.Model):
    key = models.SlugField(unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class MenuItem(models.Model):
    public_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category.key})"

class Price(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='prices')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('item', 'size', 'variant')

    def __str__(self):
        return f"{self.item.name} - {self.size.key}/{self.variant.key}: {self.amount}"

class Settings(models.Model):
    addon_meat = models.DecimalField(max_digits=6, decimal_places=2, default=3)
    meat_variants = models.ManyToManyField(Variant, blank=True)

    def __str__(self):
        return "Ajustes"

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="recipes"
    )
    description = models.TextField()
    publish_date = models.DateField()

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=25, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        # related_name='users'
        null=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user"
        verbose_name = "Api_User"

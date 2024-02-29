from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    phone_number = models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )

    avatar = models.ImageField(
        upload_to=f"user/avatar/",
        max_length=255,
        null=True,
        blank=True,
    )

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return 'https://static.vecteezy.com/system/resources/previews/016/916/479/original/placeholder-icon-design-free-vector.jpg'

    @property
    def is_service_provider(self):
        service_provider = ServiceProvider.objects.filter(user=self).first()
        return service_provider is not None


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    value = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.value


class ServiceProvider(models.Model):

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    work = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )


    TOWNS = [
        ("ouagadougou", "Ouagadougou"),
        ("bobodioulasso", "Bobo-Dioulasso"),
        ("koudougou", "Koudougou"),
        ("ouahigouya", "Ouahigouya"),
        ("banfora", "Banfora"),
        ("dedougou", "Dédougou"),
        ("kaya", "Kaya"),
        ("tenkodogo", "Tenkodogo"),
        ("fada_ngourma", "Fada N'gourma"),
        ("dori", "Dori"),
        ("koupela", "Koupéla"),
        ("reo", "Réo"),
        ("ouargaye", "Ouargaye"),
        ("manga", "Manga"),
        ("ziniare", "Ziniaré"),
        ("kombissiri", "Kombissiri"),
        ("gaoua", "Gaoua"),
        ("houet", "Houet"),
        ("yako", "Yako"),
        ("kongoussi", "Kongoussi"),
        ("marchi", "Marchi"),
        ("mohembo", "Mohembo"),
        ("nouna", "Nouna"),
        ("pama", "Pama"),
        ("po", "Pô"),
        ("sapone", "Saponé"),
        ("seytenga", "Seytenga"),
        ("sindou", "Sindou"),
        ("solenzo", "Solénzo"),
        ("sondrio", "Sondrio"),
        ("tenado", "Tenado"),
        ("titao", "Titao"),
        ("tougan", "Tougan"),
        ("yako", "Yako"),
        ("zinga", "Zinga"),
        ("zorgho", "Zorgho"),
    ]
    town = models.CharField(
        max_length=255,
        choices=TOWNS,
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    LEVEL_OF_EDUCATION = [
        ("BEPC", "BEPC"),
        ("BAC", "BAC"),
        ("BAC+1", "BAC+1"),
        ("BAC+2", "BAC+2"),
        ("BAC+3", "Licence"),
        ("BAC+4", "BAC+4"),
        ("BAC+5", "MASTER"),
    ]
    level_of_education = models.CharField(
        max_length=255,
        choices=LEVEL_OF_EDUCATION,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

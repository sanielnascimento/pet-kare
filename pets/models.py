from django.db import models


class AnimalGenre(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    sex = models.CharField(
        max_length=20,
        choices=AnimalGenre.choices,
        default=AnimalGenre.NOT_INFORMED
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.PROTECT,
        related_name="pets"
    )
    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="pets"
    )

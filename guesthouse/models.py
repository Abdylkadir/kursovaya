from django.db import models

from django.urls import reverse

from simple_history.models import HistoricalRecords


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name                    # Ак вернет строковое представление о модели

    class Meta:                             # Ак контейнер класса с некоторыми опциями,прикрепленными к модели
        verbose_name = "Категория"          # Имя для объета в ед числе
        verbose_name_plural = "Категории"   # Имя для объета во мн числе


class Guide(models.Model):
    """Гиды и повары"""
    name = models.CharField("Имя", max_length=100)
    # age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="guides/")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('guide_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Гиды и повара"
        verbose_name_plural = "Гиды и повара"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Location(models.Model):
    """Локация"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    imageLocation = models.ImageField(
        "Изображение", upload_to="locations/", default='')
    count = models.PositiveSmallIntegerField("Количество людей", default=1)
    guides = models.ManyToManyField(
        Guide, verbose_name="гид", related_name="location_guide")  # Ак verbose_name - имя для поля, related_name - имя,используемое для отношения от связываемого объекта
    cookers = models.ManyToManyField(
        Guide, verbose_name="повар", related_name="location_cooker")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    price = models.PositiveIntegerField("Цена", default=0,
                                        help_text="указывать сумму в рублях")
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class LocationsShots(models.Model):
    """Кадры из локации"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(
        Location, verbose_name="Локация", on_delete=models.CASCADE)  # Ак CASCADE - при удалении Локации все кадры тоже удалятся

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из локации"
        verbose_name_plural = "Кадры из локации"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.location}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    location = models.ForeignKey(
        Location, verbose_name="локация", on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

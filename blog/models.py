from django.db import models

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Заголовок", help_text="Введите заголовок статьи"
    )

    content = models.TextField(
        verbose_name="Содержимое статьи", help_text="Введите содержимое статьи"
    )

    preview = models.ImageField(
        upload_to="blog/photo",
        verbose_name="Превью",
        help_text="Загрузите превью статьи",
        **NULLABLE
    )

    number_views = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

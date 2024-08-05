from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(max_length=50, verbose_name='email', unique=True)
    comment = models.TextField(verbose_name='комментарии', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема сообщения")
    text = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey(User, verbose_name='Пользователь', **NULLABLE, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.subject}: {self.text}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class MailingSettings(models.Model):
    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]
    start_time = models.DateTimeField(verbose_name='время начала рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания рассылки')
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED, verbose_name='статус')

    title = models.CharField(max_length=50, verbose_name='тема')
    text = models.TextField(verbose_name='письмо')

    massage = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.CASCADE)

    client = models.ManyToManyField(Client, verbose_name='клиент')
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.title} time: {self.start_time} - {self.end_time}, periodicity: {self.periodicity}, status: {self.status}'

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылок'
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class Log(models.Model):
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_ERROR = 'ERROR'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_ERROR, 'Ошибка'),
    ]

    time = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, verbose_name='статус попытки',
                              default=STATUS_SUCCESS)
    server_response = models.TextField(default=False, verbose_name='ответ почтового сервера')

    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент', **NULLABLE)

    def __str__(self):
        return f'{self.time} {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

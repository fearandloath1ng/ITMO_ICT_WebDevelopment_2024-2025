## Лабораторная работа №2

# Функции

- Приложение Hotels может регистрировать новых пользователей и позволяет им заходить в свой аккаунт. 
- Пользователь имеет доступ к списку отелей, комнатам этих отелей и отзывам на них. 
- Пользователь имеет возможность смотреть свои бронирования, создавать новые, изменять и удалять их.
- Пользователь может оставлять отзывы о проживании.

# Модели

- Hotel: *name, owner, address, description*
- Room: *hotel (fk), room type, price, capacity, description*
- Reservation: *user (fk), room (fk), start date, end date*
- Review: *reservation (fk), review, rate*

```python
class Hotel(models.Model):
    name = models.CharField(max_length=50, null=False)
    owner = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, null=False)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=30, null=False)
    price = models.PositiveIntegerField()
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    description = models.CharField(max_length=100, blank=True, null=True)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Review(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
```

# Начало работы

- Команда запуска сервера: `python manage.py runserver`
- Ссылка на регистрацию: <http://127.0.0.1:8000/signup/>
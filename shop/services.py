from django.utils import timezone


def is_birthday_today(birthday):
    
    if birthday:
        today = timezone.now().date()
        return birthday.month == today.month and birthday.day == today.day
    return False


def price_with_birthday_discount(birthday, price, discount=10):
    
    if is_birthday_today(birthday):
        return int(price * (1 - discount / 100))
    return price

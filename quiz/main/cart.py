from decimal import Decimal
from django.conf import settings
from .models import Book

class Cart:
    def __init__(self, request):
        """
        Инициализация корзины.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity=1, update_quantity=False):
        """
        Добавление книги в корзину или обновление её количества.
        """
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}
        if update_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Сохраняем корзину в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, book):
        """
        Удаление книги из корзины.
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        """
        Итерация по книгам в корзине и получение объектов Book.
        """
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчёт всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчёт общей стоимости книг в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Очистка корзины.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
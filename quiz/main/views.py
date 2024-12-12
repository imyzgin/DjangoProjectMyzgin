from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .forms import ContactForm
from django.contrib import messages

# class CustomLogin(AuthenticationForm):
#    name = forms.CharField(label="Your name", max_length=100)

# class ContactForm(forms.Form):
#    name = forms.CharField(label="Your name", max_length=100)


def render_main(request): 
    # популярные книги с id 1 и 3
    popular_books = Book.objects.filter(id__in=[5, 3])
    
    # новинки с id 2 и 4
    new_books = Book.objects.filter(id__in=[6, 4])
    
    data = {
        'popular_books': popular_books,  
        'new_books': new_books,          
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
    }
    
    return render(request, 'index.html', data)

# def contacts(request):
#    form = CustomLogin()
#    return render(request, 'contacts.html', {"form": form})

def contacts(request):
   return render(request, 'contacts.html')



def books_list(request):
   data = {}
   data["books"] = Book.objects.all()
   print(data['books'])
   return render(request, 
                 'bookslist.html',
                 data
                 )


def add_to_cart(request, book_id):
    # Проверяем, есть ли корзина в сессии
    if 'cart' not in request.session:
        request.session['cart'] = []

    # Добавляем книгу в корзину
    request.session['cart'].append(book_id)
    request.session.modified = True  # Сохраняем изменения в сессии

    messages.success(request, 'Книга добавлена в корзину!')
    return redirect('catalog')

def remove_from_cart(request, book_id):
    # Удаляем книгу из корзины
    if 'cart' in request.session:
        request.session['cart'].remove(book_id)
        request.session.modified = True  # Сохраняем изменения в сессии

    messages.success(request, 'Книга удалена из корзины!')
    return redirect('cart')  # Перенаправляем на страницу корзины

def cart(request):
    # Получаем корзину из сессии
    cart_items = request.session.get('cart', [])

    # Получаем объекты книг из корзины
    books = Book.objects.filter(id__in=cart_items)

    return render(request, 'cart.html', {'books': books})



class BooksList(ListView):
   queryset = Book.objects.all()
   template_name = 'bookslist.html'
   context_object_name = "books"
   # paginate_by = 4  ПАГИНАЦИЯ
   

class BookDetail(DetailView):
   model = Book
   template_name = 'book_detail.html'
   context_object_name = "book"

class AuthorList(ListView):
   queryset = Author.objects.all()
   template_name = 'tests/author_list.html'
   context_object_name = "authors"
   
class GenreList(ListView):
   queryset = Genre.objects.all()
   template_name = 'genre_list.html'
   context_object_name = "genres"

class ReviewList(ListView):
   queryset = Review.objects.all()
   template_name = 'review_list.html'
   context_object_name = "reviews"

class PublisherList(ListView):
   queryset = Publisher.objects.all()
   template_name = 'publisher_list.html'
   context_object_name = "publishers"
   
def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            return render(request, 'contacts_success.html')  
    else:
        form = ContactForm()
    return render(request, 'contacts.html', {'form': form})

def catalog(request):
    genres = Genre.objects.all()
    selected_genre_id = request.GET.get('genre')
    
    if selected_genre_id:
        books = Book.objects.filter(genre__id=selected_genre_id)
    else:
        books = Book.objects.all()
    
    return render(request, 'catalog.html', {'genres': genres, 'books': books})




# __eq = 
# __gt >
# __ge >=
#__le <=
# __lq <
# question = Question.filter(pk__eq=pk)
# SELECT * FROM Question WHERE pk=$pk;
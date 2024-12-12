from django.urls import path
from . import views



urlpatterns = [
    path('', views.render_main, name ='index'),
    # path('books/', views.books_list),
    path("books/", views.BooksList.as_view()),
    path("books/<int:pk>", views.BookDetail.as_view(), name = "book_detail"),
    path("authors/", views.AuthorList.as_view()),
    path("genres/", views.GenreList.as_view(), name="genres"),
    path("review/", views.ReviewList.as_view(), name="reviews"),
    path("publisher/", views.PublisherList.as_view(), name="publishers"),
    path('contacts/', views.contacts, name="contacts"),
    path('catalog/', views.catalog, name='catalog'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart')
    #  path("test/", views.hello, name="test")

    
]
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book, Author, Genre

def home(request):
    #django ORM object
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'home.html', context)

def book(request, book_id):
    #here we are using the book_id that we passed in in order to search in the db Book table built-in id field
    book = Book.objects.get(id=book_id)
    context = {
        'book': book
    }
    return render(request, 'book.html', context)



########################################WORK ON ME LATER################################################
#TODO: author views
    #path('author/<int:author_id>/', views.author_stories, name='author_stories')
def author_stories(request, author_id):
    author = Author.objects.get(id=author_id)
    context = {
        'author': author
    }
    return render(request, 'author.html', context)


#TODO: genre views
    #path('genre/<int:genre_id>/', views.genre_stories, name='genre_stories')
def genre_stories(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    context = {
        'genre': genre
    }
    return render(request, 'genre.html', context)

from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from books.models import Book, Author, Genre, Word
from books.parser import create_book_contents_object

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

def book_info(request, book_id):
    book = Book.objects.get(id=book_id)
    book_words = list(Word.objects.filter(book=book))
    if not book_words:
        create_book_contents_object(book)
    context = {
        #for this to work, Book model must have content_lines attribute as an array with [line1, line2, ...]
        "book_words": book_words,
        'book': book
    }
    return render(request, 'book_info.html', context)


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

#this will update all definitions, not a specific one
#this is the logic of what the endpoint should do
#TODO: this endpoint results in an error, stopping at a different word every time
def update_definitions(request):
    words = Word.objects.all()
    #update defitions for each book we have in the database one at a time
    for word in words:
        print(word.book_form, " is about to be updated")
        word.update_definition() #from models.py
    
    return render(request, 'update_defs.html')

#TODO: would the following need a new view? would it work on its own?
    #path('genre/<int:genre_id>/<int:book_id>/', views.book_info, name='genre_book_info')

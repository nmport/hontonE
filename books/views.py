from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
import time, re
from books.models import Book, Author, Genre, Word, BookWord, BookLine
from hontone.models import UserWord, WordDeck
from books.parser import create_book_contents_object

from rest_framework import viewsets
from books.serializers import BookSerializer

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
    update = request.GET.get('update', False) if request.method == 'GET' else False
    book_words = list(BookWord.objects.filter(book=book))
    if not book_words:
        create_book_contents_object(book)
    context = {
        #book_info is a BookContents object, so we are also create BookWord, BookLine objects within it
        #for this to work, Book model must have content_lines attribute as an array with [line1, line2, ...]
        "book_words": book_words,
        "book_lines": list(book.book_lines.all()),
        'book': book
    }
    return render(request, 'book_info.html', context)

@login_required(login_url='/login')
def add_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user_words = []
    user = request.user
    for book_word in book.book_words.all():
        #NOTE: if request.user.user_words.filter(word=book_word.word).exists()
        user_word = UserWord.objects.filter(user=request.user, word=book_word.word).first()
        if not user_word:
            user_word = UserWord.objects.create(
                user=user,
                word=book_word.word
            )
        user_words.append(user_word)
    
    # This part we are checking if an existing word deck exists with a book name, 
    # we might have cases where users have previously created a word deck for the book but removed 
    # The word, in this case we want to preserve that word deck and create a new one for them instead. 
    # If one already exists with all the same words, we don't need to make a WordDeck
    book_name = "{} - {}".format(
        book.name_romaji if not book.name_japanese else book.name_japanese, 
        ", ".join([author.name for author in book.authors.all()])
    )
    existing_book_word_decks = WordDeck.objects.filter(user=user, name__startswith=book_name)
    if not existing_book_word_decks.filter(user_words__in=user_words, book=book).exists():
        # Checking what other names exist so as to give the created WordDeck a unique name ie. book_name (2)
        max_index = -1
        print(existing_book_word_decks)
        for word_deck in existing_book_word_decks:
            if re.match(book_name + '( \([1-9][0-9]*\)$|$)', word_deck.name):
                index_str = word_deck.name.split(book_name, maxsplit=1)[-1].strip(' ()')
                index = int(index_str) if index_str.isnumeric() else 0
                max_index = max(max_index, index)
            
        name_suffix = f" ({max_index+1})" if max_index != -1 else ""
        print(name_suffix)
        WordDeck.objects.create(user=user, name=book_name+name_suffix, book=book).user_words.set(user_words)
    return redirect('show_words')

@login_required(login_url='/login')
def add_line(request, book_line_id):
    book_line = BookLine.objects.get(id=book_line_id)
    for word in book_line.words.all():
        if not UserWord.objects.filter(user=request.user, word=word).exists():
            UserWord.objects.create(
                user=request.user,
                word=word
            )
    return redirect('show_words')

@login_required(login_url='/login')
def add_word(request, word_id):
    word = Word.objects.get(id=word_id)
    if not UserWord.objects.filter(user=request.user, word=word).exists():
        UserWord.objects.create(
            user=request.user,
            word=word
        )
    return redirect('show_words')
    
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

#DRF
def list_books(request):
    books = Person.objects.all()

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
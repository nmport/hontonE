"""hontone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from books import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet) #creates books endpoint + books/id 


urlpatterns = [
    #the name variable corresponds to the html file (??) or what exactly is it doing?
    path('', views.home, name='home'),
    path('books/<int:book_id>', views.book, name='book'),
    path('books/<int:book_id>/info', views.book_info, name='book_info'),
    path('books/<int:book_id>/add', views.add_book, name='add_book'), #not implemented
    path('book-lines/<int:book_line_id>/add', views.add_line, name='add_line'),
    path('book-words/<int:word_id>/add', views.add_word, name='add_word'),
    #TODO: use author path
    path('authors/<int:author_id>', views.author_stories, name='author_stories'),

    # #TODO: use authors path -- need to implement a page just to see all the available authors, can later be used to search
    # path('authors', views.author_stories, name='author_stories'),

    #TODO: use genre path
    path('genres/<int:genre_id>', views.genre_stories, name='genre_stories'),

    #this is an endpoint that does something
    path('update_definitions', views.update_definitions, name='update_defs'),
    
    path('', include(router.urls))
]
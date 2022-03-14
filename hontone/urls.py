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
from django.contrib import admin
from django.urls import path, include
from hontone import views

# we will probably need to reevaluate our urls, which will be the home page and how we want to layout
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('users', views.show_users, name='user'), # NOTE: temporary, will only be used to see the users we make
    path('word-decks', views.show_word_decks, name='show_word_decks'),
    path('word-decks/delete-all', views.clear_word_decks, name='clear_word_decks'),
    path('word-decks/<int:word_deck_id>/delete', views.remove_word_deck, name='remove_word_deck'),
    path('word-decks/<int:word_deck_id>', views.show_word_deck, name='show_word_deck'),
    path('word-decks/<int:word_deck_id>/delete-all', views.clear_word_deck_words, name='clear_word_deck_words'),
    path('word-decks/<int:word_deck_id>/<int:word_id>/delete', views.remove_word_deck_word, name='remove_word_deck_word'),
    path('user-words', views.show_words, name='show_words'),
    path('user-words/delete-all', views.clear_words, name='clear_words'),
    path('user-words/<int:user_word_id>/delete', views.remove_word, name='remove_word'),
    path('', include('books.urls'))
]

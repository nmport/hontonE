from django.db import models
from django.utils.functional import cached_property

POEM = 'POEM'
SHORT = 'SHORT'
OTHER = 'OTHER'
STORY_CHOICES = [(POEM, 'Poem'), (SHORT, 'Short Story'), (OTHER, 'Other')]

#note: there is a many to many relationship with Author
class Book(models.Model):
    # 'id' is the built in unique Primary Key for all models unless overridden
    name_romaji = models.CharField(max_length=30, verbose_name='Name (Romaji)', null=True, blank=True, default=None)
    name_japanese = models.CharField(max_length=30, verbose_name='Name (Japanese)', null=True, blank=True, default=None)
    contents_romaji = models.TextField(verbose_name='Contents (Romaji)', null=True, blank=True, default=None)
    contents_japanese = models.TextField(verbose_name='Contents (Japanese)', null=True, blank=True, default=None)
    JLPT_level = models.IntegerField(null=True, blank=True, default=None)

    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    @property
    def name(self):
        if self.name_japanese:
            return self.name_japanese
        elif self.name_romaji:
            return self.name_romaji
        else:
            #raise exception here later
            print("Name not recognized as Japanese or Romaji, ID: {}".format(self.id)) 

    @property
    def content_lines(self):
        #splits a string into a list using \n as the delimiter
        if self.contents_japanese:
            return [line.strip() for line in str(self.contents_japanese).split('\n') if line.strip()]
        elif self.contents_romaji:
            return [line.strip() for line in str(self.contents_romaji).split('\n') if line.strip()]
        else:
            #raise exception here later
            print("Contents not recognized as Japanese or Romaji, ID: {}".format(self.id))

    @property
    def author_names(self):
        author_names = [author.name for author in self.authors.all()]
        return ", ".join(author_names) if len(author_names) > 0 else "Unknown"
    #could/should this be a thing?
    @property
    def to_romaji(self):
        pass

class Author(models.Model):
    name = models.CharField(max_length=20)
    books = models.ManyToManyField('Book', related_name='authors') #author can have many books, books can have many authors. this allows us to do bookOBJ.authors to get a list of authors for a book and authorOBJ.books to get a list of books for an author
    genres = models.ManyToManyField('Genre', related_name='authors') #author can have many genre, genre can have many authors

#note: there is a many to many relationship with Author
#lots of genres have a bunch of wacky alternate names, but we can deal with that later
class Genre(models.Model):
    name_romaji = models.CharField(max_length=70, verbose_name='Name (Romaji)', null=True, blank=True, default=None)
    name_japanese = models.CharField(max_length=50, verbose_name='Name (Japanese)', null=True, blank=True, default=None)

    @property
    def name(self):
        if self.name_japanese:
            return self.name_japanese
        elif self.name_romaji:
            return self.name_romaji
        else:
            #raise exception here later
            print("Genre not recognized as Japanese or Romaji, ID: {}".format(self.id))

    
class Story(models.Model):
    genre = models.ForeignKey('Genre', related_name='stories', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    book = models.ForeignKey('Book', related_name='stories', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    name = models.CharField(max_length=100) # STORY NAME
    story = models.CharField(max_length=25, choices=STORY_CHOICES, null=True, blank=True, default=None)
from django.db import models
from django.utils.functional import cached_property
from books.search import JishoSearch
# from search import JishoSearch

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

class BookLine(models.Model):
    indices = models.CharField(max_length=100) #this needs to be optimized for being a list
    line_romaji = models.CharField(max_length=200, null=True, default=None)
    line_japanese = models.CharField(max_length=200)
    words = models.ManyToManyField('Word', related_name='book_lines')
    book = models.ForeignKey('Book', related_name='book_lines', on_delete=models.CASCADE)

    @cached_property
    def book_words(self):
        return [word.book_words.get(book=self.book) for word in self.words.all()]

    def add_index(self, index):
        indices = self.get_indices()
        
        if int(index) not in indices:
            self.indices = ';'.join(map(str, indices + [index]))
            self.save()

    def get_indices(self):
        return list(map(int, self.indices.split(';'))) if self.indices else []

    @property
    def occurences(self):
        return len(self.get_indices())

class BookWord(models.Model):
    indices = models.CharField(max_length=1000, default="")
    word = models.ForeignKey('Word', related_name='book_words', null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey('Book', related_name='book_words', on_delete=models.CASCADE)

    def add_index(self, index):
        indices = self.get_indices()
        
        if int(index) not in indices:
            self.indices = ';'.join(map(str, indices + [index]))
            self.save()

    def get_indices(self):
        return list(map(int, self.indices.split(';'))) if self.indices else []

    @property
    def occurences(self):
        return len(self.get_indices())

    #using django's "create" method for models, we can create Word models in parser and pass in book_, reading_, dict_, and pos_array
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        
class Word(models.Model):
    book_form = models.CharField(max_length=35)
    reading_form = models.CharField(max_length=35)
    dict_form = models.CharField(max_length=35)
    part_of_speech_array = models.CharField(max_length=200) #in the save method, this is converted to an easy to use string vs sudachipy raw POS array (ex: ['動詞', '一般', '*', '*', '五段-ラ行', '連用形-促音便'])
    #word = models.ForeignKey(Word, related_name='definitions', on_delete=models.CASCADE) is the line in Definition model where we get self.definit
    @cached_property
    def word_definitions(self):
        return [def_obj for def_obj in self.definitions.all()] 

    @cached_property
    def is_particle(self):
        return self.part_of_speech_array.split(';')[0] == "助詞"
    
    def is_defined(self):
        #HACK: len(self.definitions.all()) > 0
        return (self.definitions.all()).count() > 0
    
    #NOTE: currently only setting definitions for NON particle words, not yet taking into account not found or related words
    def update_definition(self):
        if not self.is_particle:
            dict_search = JishoSearch(self) #we can create objects here in the models.py
            dict_search.define() #this should populate dict_search.definitions list
            for definition in dict_search.definitions:
                joined_definition = ", ".join(definition)
                #HACK: not sure where these objects are created/stored - in the DB I suppose. need help understanding this line because it's a for loop
                if not Definition.objects.filter(definition=joined_definition, word=self).exists():
                    Definition.objects.create(definition=joined_definition, word=self)
    
    #Here we are overwritting a built-in django method "save" that exists for all models. overwrite "if you want something to happen whenever you save an object" 
    # What happens when you save?:
    #1. Emit a pre-save signal. 2. Preprocess the data. 3. Prepare the data for the database., 4. Insert the data into the database. 5. Emit a post-save signal. 
    def save(self, *args, **kwargs):
        #HACK: when exactly would this conversion of the pos array happen? what args are going through here?
        if isinstance(self.part_of_speech_array, list):
            self.part_of_speech_array = ";".join(self.part_of_speech_array)
        super().save(*args, **kwargs) #call the "real" save method that does the 5 steps above
        if not self.definitions.exists() or self.is_particle:
            self.update_definition()

    def __str__(self):
        return self.dict_form
    

class Definition(models.Model):
    definition = models.TextField()
    word = models.ForeignKey(Word, related_name='definitions', on_delete=models.CASCADE)
    
    #we aren't using this property anywhere, yet, but may in the future
    @property 
    def definition_list(self):
        return str(self.definition).split(", ")

    def __str__(self):
        return str(self.definition)

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
    story_type = models.CharField(max_length=25, choices=STORY_CHOICES, null=True, blank=True, default=None)
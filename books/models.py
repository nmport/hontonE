from django.db import models

#note: there is a many to many relationship with Author
class Book(models.Model):
    # 'id' is the built in unique Primary Key for all models unless overridden
    name = models.CharField(max_length=30, verbose_name='Name', null=True, blank=True, default=None)
    contents = models.TextField(verbose_name='Contents', null=True, blank=True, default=None)

    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    @property
    def content_lines(self):
        #splits a string into a list using \n as the delimiter
        return [line.strip() for line in str(self.contents_japanese).split('\n') if line.strip()]


#lots of genres have a bunch of wacky alternate names, but we can deal with that later
class Genre(models.Model):
    name = models.CharField(max_length=70, verbose_name='Name', null=True, blank=True, default=None)
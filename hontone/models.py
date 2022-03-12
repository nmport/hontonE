from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db import models
from django.db.models.fields import related
from books import models as content_models

UNKNOWN = 'UNKNOWN'
LEARNING = 'LEARNING'
KNOWN = 'KNOWN'
STATUS_CHOICES = [(choice, choice) for choice in [UNKNOWN, LEARNING, KNOWN]]

class HontoneUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("Users must have a valid username")
        if not password:
            # TODO: Add validation for password here?
            raise ValueError("Users must have a valid password")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class HontoneUser(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = HontoneUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def word_bank(self):
        return UserWord.objects.filter(user=self)

class UserWord(models.Model):
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UNKNOWN)
    level = models.CharField(max_length=20, default=None, null=True)
    last_updated = models.DateTimeField(default=None, null=True)
    next_review = models.DateTimeField(default=None, null=True)
    user = models.ForeignKey(HontoneUser, related_name='user_words', on_delete=models.CASCADE)
    word = models.ForeignKey(content_models.Word, related_name='user_word', on_delete=models.CASCADE)

class WordDeck(models.Model):
    name = models.CharField(max_length=30)
    user_words = models.ManyToManyField(UserWord, related_name='word_decks')
    user = models.ForeignKey(HontoneUser, related_name='word_decks', on_delete=models.CASCADE)
    books = models.ForeignKey(content_models.Book, related_name='word_decks', null=True, on_delete=models.PROTECT)
from django.db import models
from django.urls import reverse
import uuid


class Author(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name='Primeiro nome'
    )
    
    last_name = models.CharField(
        max_length=255,
        verbose_name='Último nome'
    )

    date_of_birth = models.DateField(
        verbose_name='Data de nascimento',
        blank=False,
        null=False
    )

    date_of_death = models.DateField(
        verbose_name='Data do falecimento',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Gênero',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Linguagem',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Titulo',
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE
    )

    summary = models.TextField(
        max_length=1000,
        verbose_name='Sumário',
        blank=False,
        null=False
    )

    imprint = models.CharField(
        max_length=255,
        verbose_name='Imprint',
        blank=False,
        null=False
    )

    isbn = models.CharField(
        max_length=13,
        verbose_name='ISBN',
        blank=False,
        null=False
    )

    genre = models.ManyToManyField(
        Genre, 
    )

    language = models.ForeignKey(
        Language, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}'


    def get_absolute_url(self):
        return reverse('book-detail-view', args=[str(self.id)])

    class Meta:
        ordering = ['title']



class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library'
    )
    
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True
    )
    
    imprint = models.CharField(
        max_length=200
    )

    due_back = models.DateField(
        null=True,
        blank=True
    )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

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
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Gênero',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'


class Language(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Linguagem',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Linguagem'
        verbose_name_plural = 'Linguagens'


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Título',
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        Author, 
        verbose_name='Autor',
        on_delete=models.CASCADE
    )

    summary = models.TextField(
        max_length=1500,
        verbose_name='Sumário',
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
        verbose_name='Gênero'
    )

    language = models.ForeignKey(
        Language,
        verbose_name='Linguagem',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}'

    def display_genre(self):
        """Create a string for the Genre. This is required to display_genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Gênero'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        ordering = ['title']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'


class BookInstance(models.Model):
    """Model representing a specific copy of a book."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='ID unica do livro, que representa ele na livraria'
    )
    
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        verbose_name='Título do Livro',
        null=True
    )
    
    imprint = models.CharField(
        max_length=255,
        verbose_name='Versão impressa',
        blank=False,
        null=False
    )

    due_back = models.DateField(
        verbose_name='Data de devolução',
        null=True,
        blank=True
    )

    LOAN_STATUS = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponivel'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade',
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    class Meta:
        ordering = ['due_back']
        verbose_name = 'Instância de um livro'
        verbose_name_plural = 'Todas as instâncias'

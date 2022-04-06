from django.contrib import admin
from catalog.models import Author, Book, Genre, BookInstance, Language


admin.site.register(Genre)
admin.site.register(Language)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]
    ordering = ('first_name', )


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    ordering = ('title', )
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstaceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Informações do livro', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Disponibilidade', {
            'fields': ('status', 'due_back')
        })
    )

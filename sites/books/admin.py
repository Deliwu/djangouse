from django.contrib import admin
from django.utils import timezone
from .models import Author, Book, Publisher


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['first_name']
    list_display = ['first_name', 'last_name']


def book_authors_display(obj):
    return ','.join([author.last_name for author in obj.authors.all()])


book_authors_display.short_description = 'Authors'


def make_book_pub_date_to_now(modeladmin, request, queryset):
    queryset.update(publication_date=timezone.now())


make_book_pub_date_to_now.short_description = 'Mark selected book pub_date as now'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ['title', 'publisher', book_authors_display, 'publication_date']
    actions = [make_book_pub_date_to_now]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

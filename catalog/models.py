from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
    name=models.CharField(max_length=100, help_text="Genre of book")
    def __str__(self):

        return self.name
# Create your models here.


class Book(models.Model):
    title=models.CharField('Title', max_length=100)
    author=models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character')
    genre=models.ManyToManyField(Genre)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])


class BookInstance(models.Model):
    """
      Model representing a specific copy of a book (i.e. that can be borrowed from the library).
      """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.id, self.book.title)

class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
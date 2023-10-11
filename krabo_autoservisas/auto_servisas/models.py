from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid

class Genre(models.Model):
    name = models.CharField(_("name"), max_length=50, db_index=True)
    
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Genre_detail", kwargs={"pk": self.pk})

class Author(models.Model):
    first_name = models.CharField(_("first name"), max_length=100, db_index=True)
    last_name = models.CharField(_("last name"), max_length=100, db_index=True)

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Book(models.Model):
    title = models.CharField(_("title"), max_length=250, db_index=True)
    author = models.ForeignKey(
        Author, 
        verbose_name=_(""), 
        on_delete=models.CASCADE,
        related_name="books",
    )
    genre = models.ForeignKey(
        Genre, 
        verbose_name=_("genres"), 
        on_delete=models.CASCADE,
        related_name="books",
    )
    summary = models.TextField(_("summary"))

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        ordering = ["title"]

    def __str__(self):
        return f"{self.author} - {self.title}"

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
    
LOAN_STATUS = (
    (0, _("available")),
    (1, _("reserved")),
    (2, _("taken")),
    (3, _("unavailable")),
)

class BookInstance(models.Model):
    unique_id = models.UUIDField(_("unique ID"), db_index=True, unique=True)
    book = models.ForeignKey(
        Book, 
        verbose_name=_("book"), 
        on_delete=models.CASCADE,
        related_name="instances",
    )
    due_back = models.DateField(_("due back"), null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _("status"), choices=LOAN_STATUS, default=0
    )

    class Meta:
        verbose_name = _("book_instance")
        verbose_name_plural = _("book_instances")
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.book} UUID:{self.unique_id}"

    def get_absolute_url(self):
        return reverse("bookinstance_detail", kwargs={"pk": self.pk})

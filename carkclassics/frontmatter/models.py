from django.db import models
from django.urls import reverse


class Text(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, help_text="Or 'Traditionally attributed to ...'")
    slug = models.SlugField(unique=True)
    tradition = models.CharField(max_length=100, blank=True)  # e.g. Confucian, Daoist, Hindu
    summary = models.TextField(help_text="Two or three sentences on why it is worth reading.")
    suggested_pace = models.CharField(max_length=100, blank=True, help_text="e.g. 'Six sessions, about 4 books each'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Edition(models.Model):
    text = models.ForeignKey(Text, related_name="editions", on_delete=models.CASCADE)
    translator = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField("ISBN", max_length=17, blank=True)  # fill in from the book itself
    cover = models.ImageField(upload_to="editions/", blank=True, help_text="Use your own photo of your copy.")
    cover_alt = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True, help_text="Why choose it: introduction, notes, readability.")
    is_group_edition = models.BooleanField(default=False, help_text="The edition the group uses.")
    public_domain = models.BooleanField(default=False)
    link = models.URLField(blank=True, help_text="Publisher page or a library catalog entry.")

    class Meta:
        ordering = ["-is_group_edition", "translator"]

    def __str__(self):
        return f"{self.text} ({self.translator})"


class Cycle(models.Model):
    title = models.CharField(max_length=200)
    text = models.ForeignKey(Text, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True)
    start_date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class Session(models.Model):
    cycle = models.ForeignKey(Cycle, related_name="sessions", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=300, blank=True)
    passage = models.CharField(max_length=200, help_text="e.g. 'Analects 1-2'")
    assignment_for_next = models.CharField(max_length=200, blank=True)

    # Filled in after the meeting. Anonymous: no participant names.
    published = models.BooleanField(default=False)
    headcount = models.PositiveIntegerField(null=True, blank=True)
    opening_question = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    unresolved = models.TextField(blank=True, help_text="One open question per line.")
    facilitator_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]
        unique_together = [("cycle", "number")]

    def __str__(self):
        return f"{self.cycle} - session {self.number}"

    def get_absolute_url(self):
        return reverse("seminar:session_detail", args=[self.cycle.slug, self.number])

    def unresolved_list(self):
        return [line for line in self.unresolved.splitlines() if line.strip()]

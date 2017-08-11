from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()


# Create your models here.
class QuestionCategory(models.Model):
    cat_title = models.CharField(max_length=200,verbose_name='Category title',unique=True)
    cat_class = models.CharField(max_length=200,verbose_name='Category class name')
    cat_help = models.CharField(max_length=200,verbose_name='category help')
    cat_create_date = models.DateField(default=timezone.now)
    order = models.PositiveIntegerField()

    def __str__(self):
        return str(self.order) + '-' + self.cat_title


class Question(models.Model):
    category = models.ForeignKey(QuestionCategory, related_name='question_category')
    question_title = models.CharField(max_length=200)
    question_class = models.CharField(max_length=200)
    question_help = models.CharField(max_length=200)
    question_create_date = models.DateField(default=timezone.now)
    slug = models.SlugField(unique=True, max_length=140, null=True, blank=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.question_title + ' ' + str(self.order) + ' - ' + str(self.category)

    def _get_unique_slug(self):
        slug = slugify(self.question_class)
        unique_slug = slug
        num = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}_{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug and self.question_class:
            self.slug = self._get_unique_slug()
        super(Question, self).save(*args, **kwargs)


class Semester(models.Model):
    TERM_CHOICES = [
        ('first','First'),
        ('second','Second'),
        ('third','Third')
    ]
    sem_year = models.IntegerField(default=datetime.date.today().year, verbose_name='Semester Year')
    sem_month = models.CharField(max_length=50,choices=TERM_CHOICES, verbose_name='Semester Month')
    sem_is_active = models.BooleanField(verbose_name='Active')
    questions = models.ManyToManyField(Question, through='QuestionSemester', related_name='semester')
    users = models.ManyToManyField(User, through='UserSemester', related_name='semester')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sem_year) + ' (' + str(self.sem_month) + ')'

    def count_question(self):
        return self.questions.count()


class QuestionSemester(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    question_deadline = models.DateTimeField(null=False,blank=False)
    question_visibility = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.semester) + ' - question(' + str(self.question) + ')'

    class Meta:
        unique_together = ('question', 'semester')


class UserSemester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_registered_for_semester = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ' - semester(' + str(self.semester) + ')'

    class Meta:
        unique_together = ('user', 'semester')

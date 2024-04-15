from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


SUBSCRIPTION = (
    ('F', 'FREE'),
    ('M', 'Monthly'),
    ('Y', 'Yearly'))


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(
        max_length=100, choices=SUBSCRIPTION, default="FREE")

    def __str__(self):
        return self.user.username


class Course(models.Model):
    course_name = models.CharField(max_length=40)
    course_decription = RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to='course')
    slug = models.SlugField(blank=True)

    def save(self, *agrs, **kwargs):
        self.slug = slugify(self.course_name)  # for slug
        super(Course, self).save(*agrs, **kwargs)  # to save nnicely

    def __str__(self):
        return self.course_name


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_module_name = models.CharField(max_length=40)
    course_description = RichTextField()
    video = models.FileField(upload_to="video/%y")
    # from module you can watch 2 out of 100 video for free
    can_view = models.BooleanField(default=False)

    def __str__(self):
        return self.course_module_name

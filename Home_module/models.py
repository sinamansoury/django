from django.db import models

# Create your models here.


class Sliders(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(verbose_name='لینک')
    url_title = models.CharField(max_length=100, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/sliders/', verbose_name='عکس', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title
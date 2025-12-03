# Django Module
from django.db import models

# Third Party
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

# Local Module
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel

class Blog(AbstractDateTimeModel, AbstractBaseSeoModel):
    title= models.CharField(
        max_length= 225,
        verbose_name= 'موضوع'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='blog/%y/%m/%d/',
        verbose_name='تصویر',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 60}
    )
    alt = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='تگ آلت',
    )
    banner_description = models.TextField(
        verbose_name= 'توضیحات بنر'
    )
    full_description = RichTextField(
        verbose_name= 'محتوا'
    )
    newest_blog = models.ManyToManyField(
        'self',
        verbose_name= 'جدیدترین مطالب',
        symmetrical=False,
        related_name= 'related_to',
        blank= True
    )

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    @property
    def default_search_engine_title(self):
        return self.title

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

    @property
    def get_image(self):

        if self.image and self.image_thumbnail:
            image = self.image_thumbnail.url
            return image
        return None

class BlogComment(AbstractDateTimeModel):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='بلاگ'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='نام'
    )
    email = models.EmailField(
        verbose_name='ایمیل'
    )
    content = models.TextField(
        verbose_name='نظر'
    )
    is_visible = models.BooleanField(
        default=False,
        verbose_name='نمایش در صفحه'
    )

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه‌ها'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name} - {self.blog.title}"
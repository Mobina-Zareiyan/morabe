# Django Module
from django.db import models


# Local Module
from utils.models import AbstractDateTimeModel


# Third-party
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ckeditor.fields import RichTextField


class Contractor(AbstractDateTimeModel):
    name = models.CharField(
        max_length= 150,
        verbose_name= 'نام شرکت',
    )
    image = models.ImageField(
        upload_to= 'contractors/%y/%m/%d/',
        verbose_name= 'عکس برند'
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
    successful_project = models.PositiveIntegerField(
        default= 0,
        verbose_name= 'پروژه های موفق'
    )
    work_experience = models.PositiveIntegerField(
        default= 0,
        help_text= 'سال',
        verbose_name= 'سابقه کار'
    )
    subtitle = models.TextField(
        blank= True,
        verbose_name= 'توضیحات برای بنر'
    )
    description = RichTextField(
        blank= True,
        verbose_name= 'درباره کمپانی'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="نمایش در صفحه اصلی؟"
    )


    class Meta:
        verbose_name = 'سازنده'
        verbose_name_plural = 'سازنده ها'


    def __str__(self):
        return self.name


    @property
    def get_image(self):
        if self.image and self.image_thumbnail:
            image = self.image_thumbnail.url
            return image
        return None



class Gallery(AbstractDateTimeModel):
    contractor = models.ForeignKey(
        Contractor,
        related_name='galleries',
        on_delete=models.CASCADE,
        verbose_name= '' ,
    )
    image = models.ImageField(
        max_length=255,
        upload_to='projects/gallery/%Y/%m/%d/',
        verbose_name= 'تصویر',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(960, 540)],
        format='JPEG',
        options={'quality': 80}
    )
    alt = models.CharField(
        max_length=255,
        blank=True,
        null= True,
        verbose_name= 'تگ آلت',
    )
    title = models.CharField(
        max_length= 255,
        null= True,
        blank= True,
        verbose_name= 'موضوع',
    )
    subtitle = models.CharField(
        max_length= 255,
        blank= True,
        null= True,
        verbose_name= 'توضیحات کوتاه',
    )


    @property
    def get_image(self):
        if self.image:
            try:
                return self.image_thumbnail.url
            except:
                return self.image.url
        return None

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالری ها'

    def __str__(self):
        return self.contractor.name





class RegistrationContractor(AbstractDateTimeModel):
    full_name = models.CharField(
        max_length= 150,
        verbose_name='نام شرکت',
        null= True,
        blank= True,
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name='شماره تماس',
        blank=True,
        null=True,
    )
    contractor_type  = models.TextField(
        verbose_name='نوع سازنده',
    )
    is_checked = models.BooleanField(
        default=False,
        verbose_name='بررسی شده؟',
    )

    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = "درخواست ها"
        ordering = ('-created',)

    def __str__(self):
        return f'{self.contractor_type} - {self.phone}'





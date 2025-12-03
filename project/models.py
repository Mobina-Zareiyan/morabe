# Django Module
from django.db import models
from django.apps import apps
from django.core.validators import FileExtensionValidator, ValidationError

# Local Module
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel
from areas.models import Province, City


# Third-party
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ckeditor.fields import RichTextField


class UsageType(models.TextChoices):
    RESIDENTIAL = "residential", "مسکونی"
    COMMERCIAL = "commercial", "تجاری"
    OFFICE = "office", "اداری"
    MIXED = "mixed", "ترکیبی"

class Project(AbstractDateTimeModel, AbstractBaseSeoModel):
    title = models.CharField(
        max_length= 255,
        verbose_name= 'نام پروژه',

    )
    province = models.ForeignKey(
        Province,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='استان',
    )
    city = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='شهر',
    )
    usage_type = models.CharField(
        choices= UsageType.choices,
        max_length= 50,
        verbose_name='نوع کاربری'
    )
    profit_to_date = models.CharField(
        max_length= 50,
        verbose_name='سود محقق شده',
    )
    invest_start_from = models.PositiveIntegerField(
        help_text= 'تومان',
        verbose_name='مبلغ شروع سرمایه گذاری'
    )
    contractor = models.ForeignKey(
        'contractor.Contractor',
        related_name= 'projects',
        on_delete = models.CASCADE,
        verbose_name='سازنده'
    )
    floor_count = models.PositiveIntegerField(
        null= True,
        blank= True,
        verbose_name= 'تعداد طبقه',
    )
    unit_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= 'تعداد واحد',
    )
    usable_area = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        verbose_name= 'متراژ مفید',
    )
    status = models.ForeignKey(
        'ProjectStatus',
        related_name = 'projects',
        null=True,
        blank=True,
        on_delete= models.SET_NULL,
        verbose_name = 'وضعیت پروژه',
    )
    estimated_completion_date = models.DateField(
        verbose_name= 'تاریخ پیش بینی شده'
    )
    start_date = models.DateField(
        verbose_name= 'تاریخ شروع'
    )
    project_details = RichTextField(
        null=True,
        blank=True,
        verbose_name= 'اطلاعات پروژه'
    )
    address = models.TextField(
        verbose_name= 'آدرس'
    )
    map = models.TextField(
        null=True,
        blank=True,
        verbose_name= 'نقشه',
        help_text= 'کد embed گوگل مپ',
    )
    price_per_meter = models.PositiveIntegerField(
        help_text='تومان',
        verbose_name= 'قیمت هر متر'
    )
    total_area = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        verbose_name= 'متراژ کل'
    )
    complete_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name= 'متراژ تکمیل شده'
    )
    bedroom_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= 'تعداد خواب'
    )
    parking_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= 'تعداد پارکینگ'
    )
    warehouse_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= 'تعداد انباری'
    )



    def clean(self):
        if self.complete_area and self.total_area:
            if self.complete_area > self.total_area:
                raise ValidationError("متراژ تکمیل شده نمی‌تواند از متراژ کل بیشتر باشد")

        if self.start_date and self.estimated_completion_date:
            if self.estimated_completion_date <= self.start_date:
                raise ValidationError( "تاریخ پایان باید بعد از تاریخ شروع باشد" )


    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه ها'


    def __str__(self):
        return self.title



class ProjectStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name= 'وضعیت پروژه')

    class Meta:
        verbose_name = 'وضعیت پروژه'
        verbose_name_plural = 'وضعیت پروژه ها'

    def __str__(self):
        return self.name



class Gallery(AbstractDateTimeModel):
    project = models.ForeignKey(
        Project,
        related_name='gallery',
        on_delete=models.CASCADE,
        verbose_name= '' ,
    )
    image = models.ImageField(
        max_length=255,
        upload_to='projects/gallery/%y/%m/%d/',
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
        return self.project.title


class ProjectProgressReport(AbstractDateTimeModel):
    def validate_file_size(value):
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError('حجم فایل نباید بیشتر از 10 مگابایت باشد')

    project = models.ForeignKey(
        Project,
        related_name="progress_reports",
        on_delete= models.CASCADE,
        verbose_name= 'پروژه'
    )
    pdf = models.FileField(
        validators=[
            FileExtensionValidator(['pdf']),
            validate_file_size
        ],
        upload_to='projects/docs/%Y/%m/%d/',
        verbose_name= 'گزارش پیشرفت'
    )


    class Meta:
        verbose_name = 'گزارش پیشرفت'
        verbose_name_plural = 'گزارش پیشرفت'

    def __str__(self):
        return self.project.title


class ProjectDocuments(AbstractDateTimeModel):
    def validate_file_size(value):
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError('حجم فایل نباید بیشتر از 10 مگابایت باشد')

    project = models.ForeignKey(
        Project,
        related_name="documents",
        on_delete= models.CASCADE,
        verbose_name= 'پروژه'
    )
    pdf = models.FileField(
        validators=[
            FileExtensionValidator(['pdf']),
            validate_file_size
        ],
        upload_to='projects/documents/%Y/%m/%d/',
        verbose_name= 'اسناد پروژه'
    )


    class Meta:
        verbose_name = 'سند پروژه'
        verbose_name_plural = 'اسناد پروژه'

    def __str__(self):
        return self.project.title



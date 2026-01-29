# Django Built-in Modules
from django.db import models
from django.core.validators import FileExtensionValidator, ValidationError
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel
from areas.models import Province, City


# Third Party Packages
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from decimal import Decimal
from ckeditor.fields import RichTextField


class UsageType(models.TextChoices):
    RESIDENTIAL = "residential", _("مسکونی")
    COMMERCIAL = "commercial", _("تجاری")
    OFFICE = "office", _("اداری")
    MIXED = "mixed", _("ترکیبی")

class Project(AbstractDateTimeModel, AbstractBaseSeoModel):
    title = models.CharField(
        max_length= 255,
        verbose_name= _('نام پروژه'),

    )
    province = models.ForeignKey(
        Province,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('استان'),
    )
    city = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name= _('شهر'),
    )
    usage_type = models.CharField(
        choices= UsageType.choices,
        max_length= 50,
        verbose_name= _('نوع کاربری')
    )
    profit_to_date = models.CharField(
        max_length= 50,
        verbose_name= _('سود محقق شده'),
    )
    invest_start_from = models.PositiveIntegerField(
        help_text= _('تومان'),
        verbose_name= _('مبلغ شروع سرمایه گذاری')
    )
    contractors = models.ManyToManyField(
        'contractor.Contractor',
        related_name= 'projects',
        verbose_name= _('سازنده')
    )
    floor_count = models.PositiveIntegerField(
        null= True,
        blank= True,
        verbose_name= _('تعداد طبقه'),
    )
    unit_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= _('تعداد واحد'),
    )
    usable_area = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        verbose_name= _('متراژ مفید'),
    )
    status = models.ForeignKey(
        'ProjectStatus',
        related_name = 'projects',
        null=True,
        blank=True,
        on_delete= models.SET_NULL,
        verbose_name = _('وضعیت پروژه'),
    )
    estimated_completion_date = models.DateField(
        verbose_name= _('تاریخ پیش بینی شده')
    )
    start_date = models.DateField(
        verbose_name= _('تاریخ شروع')
    )
    project_details = RichTextField(
        null=True,
        blank=True,
        verbose_name= _('اطلاعات پروژه')
    )
    address = models.TextField(
        verbose_name= _('آدرس')
    )
    map = models.TextField(
        null=True,
        blank=True,
        verbose_name= _('نقشه'),
        help_text= _('کد embed گوگل مپ'),
    )
    price_per_meter = models.PositiveIntegerField(
        help_text= _('تومان'),
        verbose_name= _('قیمت هر متر')
    )
    total_area = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        verbose_name= _('متراژ کل')
    )
    complete_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name= _('متراژ تکمیل شده')
    )
    bedroom_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= _('تعداد خواب')
    )
    parking_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= _('تعداد پارکینگ')
    )
    warehouse_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= _('تعداد انباری')
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name= _("نمایش در صفحه اصلی؟")
    )
    total_budget = models.PositiveIntegerField(
        verbose_name= _("بودجه کل پروژه"),
        help_text= _("حداکثر سرمایه مورد نیاز برای پروژه (تومان)")
    )
    current_funding = models.PositiveIntegerField(
        default=0,
        verbose_name= _("سرمایه فعلی جمع‌آوری شده"),
        help_text= _("مقدار سرمایه‌ای که تاکنون جمع شده")
    )
    investable_area = models.DecimalField(
        max_digits=14,
        decimal_places=6,
        verbose_name= _("متراژ قابل سرمایه‌گذاری")
    )
    # multiplier = models.PositiveIntegerField(
    #     default= 0,
    #     verbose_name= 'ماکزیمم قیمت فروش',
    # )

    @property
    def sold_area(self):
        result = self.investments.filter(
            status="paid"
        ).aggregate(total=Sum("area"))["total"]
        return result or Decimal("0")

    @property
    def remaining_area(self):
        return self.investable_area - self.sold_area



    def clean(self):
        if self.complete_area and self.total_area:
            if self.complete_area > self.total_area:
                raise ValidationError(_("متراژ تکمیل شده نمی‌تواند از متراژ کل بیشتر باشد"))

        if self.start_date and self.estimated_completion_date:
            if self.estimated_completion_date <= self.start_date:
                raise ValidationError( _("تاریخ پایان باید بعد از تاریخ شروع باشد") )


    class Meta:
        verbose_name = _('پروژه')
        verbose_name_plural = _('پروژه ها')


    def __str__(self):
        return self.title





class ProjectStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name= _('وضعیت پروژه'))

    class Meta:
        verbose_name = _('وضعیت پروژه')
        verbose_name_plural = _('وضعیت پروژه ها')

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
        upload_to='projects/gallery/%Y/%m/%d/',
        verbose_name= _('تصویر'),
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
        verbose_name= _('تگ آلت'),
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
        verbose_name = _('گالری')
        verbose_name_plural = _('گالری ها')

    def __str__(self):
        return self.project.title


class ProjectProgressReport(AbstractDateTimeModel):
    def validate_file_size(value):
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError(_('حجم فایل نباید بیشتر از 10 مگابایت باشد'))

    project = models.ForeignKey(
        Project,
        related_name="progress_reports",
        on_delete= models.CASCADE,
        verbose_name= _('پروژه')
    )
    pdf = models.FileField(
        validators=[
            FileExtensionValidator(['pdf']),
            validate_file_size
        ],
        upload_to='projects/docs/%Y/%m/%d/',
        verbose_name= _('گزارش پیشرفت')
    )


    class Meta:
        verbose_name = _('گزارش پیشرفت')
        verbose_name_plural = _('گزارش پیشرفت')

    def __str__(self):
        return self.project.title


class ProjectDocuments(AbstractDateTimeModel):
    def validate_file_size(value):
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError(_('حجم فایل نباید بیشتر از 10 مگابایت باشد'))

    project = models.ForeignKey(
        Project,
        related_name="documents",
        on_delete= models.CASCADE,
        verbose_name= _('پروژه')
    )
    pdf = models.FileField(
        validators=[
            FileExtensionValidator(['pdf']),
            validate_file_size
        ],
        upload_to='projects/documents/%Y/%m/%d/',
        verbose_name= _('اسناد پروژه')
    )


    class Meta:
        verbose_name = _('سند پروژه')
        verbose_name_plural = _('اسناد پروژه')

    def __str__(self):
        return self.project.title



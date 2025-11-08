# Django Built-in modules
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Local Apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from ckeditor_uploader.fields import RichTextUploadingField


class BaseSeoModelQueryset(models.QuerySet):
    def published(self):
        return self.filter(page_display_status=AbstractBaseSeoModel.PUBLISH)


class AbstractBaseSeoModel(models.Model):
    DRAFT = 0
    PUBLISH = 1
    PAGE_DISPLAY_STATUS_CHOICES = (
        (DRAFT, 'پیش‌نویس'),
        (PUBLISH, 'انتشار'),
    )

    slug = models.SlugField(
        max_length=255,
        allow_unicode=True,
        unique=True,
        verbose_name='اسلاگ',
    )

    page_display_status = models.SmallIntegerField(
        choices=PAGE_DISPLAY_STATUS_CHOICES,
        default=DRAFT,
        verbose_name='وضعیت نمایش صفحه',
    )

    search_engine_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name='عنوان موتور جستجو',
        help_text='اگر خالی باشد، پیش‌نمایش آنچه به‌صورت خودکار تولید می‌شود نمایش داده می‌شود.',
    )

    search_engine_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات موتور جستجو',
        help_text='اگر خالی باشد، پیش‌نمایش آنچه به‌صورت خودکار تولید می‌شود نمایش داده می‌شود.',
    )

    search_engine_keywords = models.TextField(
        null=True,
        blank=True,
        verbose_name='کلیدواژه‌های موتور جستجو',
        help_text='اگر خالی باشد، پیش‌نمایش آنچه به‌صورت خودکار تولید می‌شود نمایش داده می‌شود.',
    )

    canonical_link = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینک کنونیکال',
        help_text='تگ کنونیکال به جلوگیری از محتوای تکراری کمک می‌کند.',
    )

    objects = BaseSeoModelQueryset.as_manager()

    class Meta:
        abstract = True

    def meta_tags(self):
        content_type = ContentType.objects.get_for_model(self)
        return MetadataModel.objects.filter(
            content_type=content_type.pk,
            object_id=self.pk
        ).values('field', 'value')

    @property
    def page_title(self):
        if self.search_engine_title:
            return self.search_engine_title
        if hasattr(self, 'default_search_engine_title'):
            if self.default_search_engine_title:
                return self.default_search_engine_title
        return ''

    def get_absolute_url_if_published(self):
        if self.page_display_status == self.PUBLISH:
            return self.get_absolute_url()
        return '#'

    @property
    def page_description(self):
        if self.search_engine_description:
            return self.search_engine_description
        if hasattr(self, 'default_search_engine_description'):
            if self.default_search_engine_description:
                return self.default_search_engine_description
        return ''

    @property
    def page_keywords(self):
        if self.search_engine_keywords:
            return self.search_engine_keywords
        if hasattr(self, 'default_search_engine_keywords'):
            if self.default_search_engine_keywords:
                return self.default_search_engine_keywords
        return ''


class AbstractContentModel(models.Model):
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات'
    )
    content = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name='محتوا',
    )

    class Meta:
        abstract = True


class MetadataModel(AbstractDateTimeModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='نوع محتوا',
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name='شی مرتبط',
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    field = models.CharField(
        max_length=255,
        verbose_name='فیلد',
    )
    value = models.TextField(
        verbose_name='مقدار',
    )

    class Meta:
        verbose_name = 'تگ متا'
        verbose_name_plural = 'تگ‌های متا'

    def __str__(self):
        return str(self.id)

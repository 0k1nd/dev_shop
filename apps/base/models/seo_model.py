from django.db import models
from django.utils.text import slugify


class BaseSeoModel(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        abstract = True

    def get_seo_source_title(self) -> str:
        return getattr(self, "name", "") or getattr(self, "title", "")

    def get_seo_source_description(self) -> str:
        return getattr(self, "description", "")

    def prepare_seo_fields(self):
        if not self.slug and self.get_seo_source_title():
            self.slug = slugify(self.get_seo_source_title())
        if not self.meta_title:
            self.meta_title = self.get_seo_source_title()[:255]
        if not self.meta_description:
            self.meta_description = self.get_seo_source_description()[:300]

    def save(self, *args, **kwargs):
        self.prepare_seo_fields()
        super().save(*args, **kwargs)
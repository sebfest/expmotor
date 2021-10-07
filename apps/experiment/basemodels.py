from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class AbstractBaseModel(models.Model):
    """Abstract base model for all models."""
    slug = models.SlugField(
        _('slug'),
        max_length=128,
        blank=True,
        db_index=False,
        help_text=_('Slug for URL.')
    )
    created_date = models.DateTimeField(
        _('created at'),
        auto_now=False,
        auto_now_add=True,
        editable=False,
        help_text=_('Date of creation'),
    )
    modified_date = models.DateTimeField(
        _('modified at'),
        auto_now=True,
        auto_now_add=False,
        help_text=_('Date of last modification'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Is active'),
    )
    activation_date = models.DateTimeField(
        _('activated at'),
        blank=True,
        null=True,
        help_text=_('Date of activation'),
    )

    def clean(self):
        """Custom model validation."""
        if self.is_active and self.activation_date is None:
            self.activation_date = timezone.now()
        elif not self.is_active and self.activation_date is not None:
            self.activation_date = None
        if not self.slug:
            self.slug = slugify(self.__str__())

    def save(self, *args, **kwargs):
        self.clean()
        super(AbstractBaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-activation_date', '-created_date']
        get_latest_by = 'activation_date'

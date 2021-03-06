import django
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey, DO_NOTHING, UniqueConstraint, CheckConstraint, Q, IntegerField
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_empty_or_0_10(value):
    if value is not None:
        if value > 10 or value < 0:
            raise ValidationError(
                _('%(value)s is not between 0 and 10'),
                params={'value': value},
            )


def validate_no_slash(value):
    if '/' in value:
        raise ValidationError(
            _('%(value)s must not contain /'),
            params={'value': value},
        )


class Whisky(models.Model):
    name = models.CharField(max_length=128, primary_key=True, validators=[validate_no_slash])

    class Meta:
        verbose_name_plural = "Whiskies"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('whisky-detail', args=[str(self.pk)])


class Evening(models.Model):
    date = models.DateField(primary_key=True,
                            # default=datetime.date.today(),
                            default=django.utils.timezone.now
                            )
    whiskies = models.ManyToManyField(Whisky, through='EveningWhisky')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('evening-detail', args=[str(self.pk)])


class EveningWhisky(models.Model):
    evening = ForeignKey(Evening, on_delete=DO_NOTHING)
    whisky = ForeignKey(Whisky, on_delete=DO_NOTHING)
    order = IntegerField(verbose_name='order of the day', null=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "EveningWhiskies"
        constraints = [UniqueConstraint(fields=['evening', 'whisky'], name='evening_whisky')]

    def __str__(self):
        return f'{self.evening_id} {self.whisky_id} {self.order}'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('eveningwhisky-detail', args=[str(self.id)])


class Tasting(models.Model):
    evening_whisky = ForeignKey(EveningWhisky, on_delete=DO_NOTHING)
    nose = models.DecimalField("nose/Geruch (0-10) best whisky ever=10", max_digits=3, decimal_places=1,
                               validators=[validate_empty_or_0_10], null=True, blank=True)
    taste = models.DecimalField("taste/Geschmack (0-10) best whisky ever=10", max_digits=3, decimal_places=1,
                                validators=[validate_empty_or_0_10], null=True, blank=True)
    color = models.DecimalField("color/Farbe (0-10) like water=0, Cola=10", max_digits=3, decimal_places=1,
                                validators=[validate_empty_or_0_10], null=True, blank=True)
    smokiness = models.DecimalField("smokiness/Rauchigkeit (0-10) in the middle of the chimney=10", max_digits=3,
                                    decimal_places=1, validators=[validate_empty_or_0_10], null=True, blank=True)
    user = ForeignKey(User, on_delete=DO_NOTHING)

    class Meta:
        constraints = [UniqueConstraint(fields=['evening_whisky', 'user'], name='evening_whisky_user'),
                       CheckConstraint(check=Q(nose__gte=0) & Q(nose__lte=10), name='nose_between_0_10'),
                       CheckConstraint(check=Q(taste__gte=0) & Q(taste__lte=10), name='taste_between_0_10')]

    def __str__(self):
        return f'{self.evening_whisky} {self.user} {self.nose} {self.taste}'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('tasting-detail', args=[str(self.id)])

import datetime
import random

from django.utils import timezone
from django.utils.text import slugify
from factory import LazyAttribute, SubFactory, Faker, RelatedFactoryList, Iterator
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

from experiment.models import Experiment, Session, Registration
from settings import base


class UserFactory(DjangoModelFactory):
    class Meta:
        model = base.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    first_name = Faker(
        'first_name'
    )
    last_name = Faker(
        'last_name'
    )
    username = LazyAttribute(
        lambda obj: slugify(obj.first_name + '_' + obj.last_name)
    )
    email = Faker(
        'email'
    )
    password = Faker(
        'password'
    )
    is_staff = Faker(
        'boolean',
        chance_of_getting_true=0
    )
    is_superuser = Faker(
        'boolean',
        chance_of_getting_true=0
    )
    is_active = Faker(
        'boolean', chance_of_getting_true=100
    )
    date_joined = LazyAttribute(
        lambda obj: timezone.now() - datetime.timedelta(days=random.randint(5, 50))
    )
    last_login = LazyAttribute(
        lambda obj: obj.date_joined + datetime.timedelta(days=4)
    )


class RegistrationFactory(DjangoModelFactory):
    class Meta:
        model = Registration
        django_get_or_create = ('first_name', 'last_name')

    first_name = Faker(
        'first_name',
        locale='no_NO'
    )
    last_name = Faker(
        'last_name',
        locale='no_NO'
    )
    phone = Faker(
        'phone_number',
        locale='no_NO'
    )
    email = Faker(
        'email',
        locale='no_NO'
    )
    confirmed_email = Faker(
        'boolean',
        chance_of_getting_true=95
    )
    created_date = FuzzyDateTime(
        timezone.now() - datetime.timedelta(days=random.randint(5, 356))
    )
    modified_date = LazyAttribute(
        lambda obj: obj.created_date + datetime.timedelta(days=random.randint(1, 4))
    )
    is_active = Faker(
        'boolean',
        chance_of_getting_true=99
    )


class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session

    experiment = Iterator(
        Experiment.objects.all()
    )
    date = FuzzyDateTime(
        timezone.now(),
        timezone.now() + datetime.timedelta(days=random.randint(5, 30))
    )
    time = LazyAttribute(
        lambda obj: obj.date.replace(microsecond=0, second=0, minute=0)
    )
    place = Faker(
        'address',
        locale='no_NO'
    )
    max_subjects = Faker(
        'random_int',
        min=15,
        max=30
    )
    created_date = LazyAttribute(
        lambda obj: obj.experiment.created_date
    )
    modified_date = LazyAttribute(
        lambda obj: obj.created_date + datetime.timedelta(days=random.randint(1, 4))
    )
    is_active = Faker(
        'boolean', chance_of_getting_true=99
    )
    participants = RelatedFactoryList(
        RegistrationFactory,
        factory_related_name='session',
        size=lambda: random.randint(1, 10),
    )


class ExperimentFactory(DjangoModelFactory):
    class Meta:
        model = Experiment
        django_get_or_create = ('name',)

    manager = SubFactory(
        UserFactory
    )
    name = LazyAttribute(
        lambda obj: slugify(obj.title)
    )
    title = Faker(
        'sentence',
        nb_words=3,
    )
    email = Faker(
        'email',
        locale='no_NO'
    )
    phone = Faker(
        'random_number',
        digits=8,
    )
    created_date = FuzzyDateTime(
        timezone.now() - datetime.timedelta(days=random.randint(5, 356))
    )
    modified_date = LazyAttribute(
        lambda obj: obj.created_date + datetime.timedelta(days=random.randint(1, 4))
    )
    is_active = Faker(
        'boolean',
        chance_of_getting_true=99
    )
    session = RelatedFactoryList(
        SessionFactory,
        factory_related_name='experiment',
        size=10
    )

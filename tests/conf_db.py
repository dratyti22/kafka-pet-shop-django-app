import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Автоматическое создание БД и применение миграций"""
    with django_db_blocker.unblock():
        # Создаем тестовую БД и применяем миграции
        call_command('migrate', verbosity=0)

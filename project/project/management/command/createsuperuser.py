from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        database = options.get('database')

        # Prompt for age field
        age = input("Age: ")
        if age:
            options['age'] = age
        else:
            raise CommandError("Invalid age")

        try:
            return super().handle(*args, **options)
        except Exception as e:
            raise CommandError(e)

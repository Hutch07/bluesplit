from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import Group

        def create_default_groups(sender, **kwargs):
            if kwargs.get('app_config') and kwargs['app_config'].name != self.name:
                return
            for group_name in ['Customer', 'Pilot', 'Admin', 'General']:
                Group.objects.get_or_create(name=group_name)

        post_migrate.connect(create_default_groups, sender=self, dispatch_uid='core_create_default_groups')

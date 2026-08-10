from django.apps import AppConfig


class ExperimentConfig(AppConfig):
    name = 'experiment'
    verbose = 'Experiment'

    def ready(self):
        from . import signals  # noqa: F401

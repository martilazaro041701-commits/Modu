from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Job, JobHistory


@receiver(pre_save, sender=Job)
def cache_previous_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status_id = None
        return
    instance._previous_status_id = (
        sender.objects.filter(pk=instance.pk).values_list("current_status_id", flat=True).first()
    )


@receiver(post_save, sender=Job)
def log_job_status_change(sender, instance, created, **kwargs):
    previous_status_id = getattr(instance, "_previous_status_id", None)
    current_status_id = instance.current_status_id

    if created and current_status_id:
        JobHistory.objects.create(job=instance, status_id=current_status_id)
        return

    if previous_status_id != current_status_id and current_status_id:
        JobHistory.objects.create(job=instance, status_id=current_status_id)

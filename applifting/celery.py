from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "applifting.settings")
app = Celery("applifting")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,
        snapshot_offer_pricestamps.s(),
        name="get_offer_pricestamps_for_all_products",
    )


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task
def snapshot_offer_pricestamps():
    from catalog.tasks import get_offer_pricestamps_for_all_products

    return get_offer_pricestamps_for_all_products()

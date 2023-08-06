import urllib

from django.conf import settings
from django.shortcuts import reverse

from .base import BaseBackend


class DebugWebBackend(BaseBackend):
    """
    This backend aids debugging in concert with the 'debug-run' view.

    Instead of actually running a job, it prints the url to the debug-run view
    for the local Django instance which can be used to run the task for
    debugging.

    See the docstring of that view for information (and limitations) about it.
    """

    def enqueue(self, job, queue):
        path = reverse('django-lightweight-queue:debug-run')
        query_string = urllib.parse.urlencode({'job': job.to_json()})
        url = "{}{}?{}".format(settings.SITE_URL, path, query_string)
        print(url)

    def dequeue(self, queue, worker_num, timeout):
        pass

    def length(self, queue):
        return 0

from django.utils.functional import cached_property

from .utils import get_queue_counts
from .cron_scheduler import CRON_QUEUE_NAME


class Machine:
    """
    Dummy machine class to contain documentation.

    Implementations may extend this class if desired, though this
    is not required.
    """

    @property
    def run_cron(self):
        """
        Returns a `bool` for whether or not a runner on this machine should
        run the cron queue.
        """
        raise NotImplementedError()

    @property
    def worker_names(self):
        """
        Returns a sequence of tuples of (queue_name, worker_num) for the workers
        which should run on this machine. Worker numbers start at 1.

        Implemetations should be efficient even if this is called several times.
        """
        raise NotImplementedError()


class PooledMachine(Machine):
    """
    A machine which behaves as part of a pool.

    It relies on being given information about the pool which it uses to
    determine its position within the pool and thus which queues to run.
    """

    def __init__(self, machine_number, machine_count, only_queue):
        self.machine_number = machine_number
        self.machine_count = machine_count
        self.only_queue = only_queue

    @property
    def run_cron(self):
        return self.machine_number == 1 and (
            not self.only_queue or self.only_queue == CRON_QUEUE_NAME
        )

    @property
    def configure_cron(self):
        return True

    @cached_property
    def worker_names(self):
        """
        Determine the workers to run on a given machine in a pool of a known size.
        """

        worker_names = []

        # Iterate over all the possible workers which will be run in the pool,
        # choosing only those which should be run on this machine.
        job_number = 1

        for queue, num_workers in sorted(get_queue_counts().items()):
            if self.only_queue and self.only_queue != queue:
                continue

            for worker_num in range(1, num_workers + 1):
                if (job_number % self.machine_count) + 1 == self.machine_number:  # noqa: S001
                    worker_names.append((queue, worker_num))

                job_number += 1

        return worker_names


class DirectlyConfiguredMachine(Machine):
    """
    A machine which is configured by an explicitly passed in configuration file.

    This class assumes that the loading of the settings from that configuration
    file has already been handled.
    """
    @property
    def run_cron(self):
        return False

    @property
    def configure_cron(self):
        return False

    @cached_property
    def worker_names(self):
        return tuple(
            (queue, worker_number)
            for queue, num_workers in sorted(get_queue_counts().items())
            for worker_number in range(num_workers)
        )

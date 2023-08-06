from dataclasses import dataclass, field
from pathlib import Path
import json
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import stringcase
import toolz
from toolz.dicttoolz import keymap


class Capacity(BaseModel):
    # note: values are always in megaBytes
    memory_mb: int
    vcores_nb: int


class Queue(BaseModel):
    """queues object for a Leaf Yarn queue"""

    queue_name: str
    # Configured queue capacity in percentage relative to its parent queue
    capacity: float
    # Configured maximum queue capacity in percentage
    # relative to its parent queue
    max_capacity: float
    # The maximum number of applications this queue can have
    max_applications: Optional[int]
    max_applications_per_user: Optional[int]
    """Minimum User Percentage and User Limit Factor are ways to control
     how resources get assigned to users within the queues they are utilizing.
     The Min User Percentage is a soft limit on the smallest amount of resources 
     a single user should get access to if they are requesting it
    """
    user_limit: Optional[int]
    """User Limit Factor is set as a multiple of the queues minimum capacity
     where a user limit factor of 1 means the user can consume the entire minimum 
     capacity of the queue.
     """
    user_limit_factor: Optional[int]
    queues: Optional[List]


@dataclass
class Config:
    """Process results from REST API call on
    - `resourcemanager/v1/cluster/scheduler`
    - `resourcemanager/v1/cluster/metrics`

    more info on
    https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Information_API
    https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Scheduler_API
    """

    scheduler: dict
    metrics: dict
    queues: List[Queue] = field(init=False)
    cluster: Capacity = field(init=False)

    def __post_init__(self):
        self.queues = Config._proc_scheduler(self.scheduler)
        self.cluster = Config._proc_metrics(self.metrics)

    @classmethod
    def from_file(cls, schedulerjson: Path, metricsjson: Path):
        scheduler = json.load(schedulerjson.open())
        metrics = json.load(metricsjson.open())

        return cls(scheduler, metrics)

    def get(self, queue_name: str) -> Capacity:
        """capacity that should be always available"""
        try:
            queue = [elt for elt in self.queues if elt.queue_name == queue_name][0]
        except IndexError:
            raise ValueError(f"queue `{queue_name}` not found")

        return Capacity(
            memory_mb=round(self.cluster.memory_mb * queue.capacity / 100, 1),
            vcores_nb=round(self.cluster.vcores_nb * queue.capacity / 100, 1),
        )

    def get_queue(self,queuename)->Queue:
        try:
            return [queue for queue in self.queues if queue.queue_name==queuename][0]
        except IndexError:
            raise ValueError(f"queue `{queuename}` not found")

    def get_queue_maxcapacity(self, queuname: str):
        """capacity that can be used if there is extra free ressources"""
        pass

    @staticmethod
    def _proc_metrics(payload: dict) -> Capacity:
        config = payload["clusterMetrics"]
        return Capacity(
            memory_mb=config["totalMB"], vcores_nb=config["totalVirtualCores"]
        )

    @staticmethod
    def _proc_scheduler(payload: dict) -> List[Queue]:
        queues = Config._get_queues(payload)
        return [Config._proc_queue(queue) for queue in queues]

    @staticmethod
    def to_snake(queue: dict) -> dict:
        return toolz.dicttoolz.keymap(stringcase.snakecase, queue)

    @staticmethod
    def _proc_queue(queue: dict) -> Queue:
        clean = Config.to_snake(queue)
        if "queues" in clean:
            clean["queues"] = clean["queues"]["queue"]
        return Queue(**clean)

    @staticmethod
    def _get_queues(payload: dict) -> list:
        """extract list of queues from a scheduler json dump"""
        return payload["scheduler"]["schedulerInfo"]["queues"]["queue"]

    @staticmethod
    def _get_subqueue(queue: Queue, quename: str) -> Queue:
        if queue.queues:
            subqueues = [Queue(**(Config.to_snake(elt))) for elt in queue.queues]
            return [elt for elt in subqueues if elt.queue_name == quename][0]
        else:
            raise ValueError(f"no subqueue in {queue}")

    @staticmethod
    def _get_queue_raw(payload: dict, queuename: str) -> dict:
        try:
            queues = Config._get_queues(payload)
            return [queue for queue in queues if queue["queueName"] == queuename][0]
        except IndexError:
            return {}

    @staticmethod
    def _calculate_capacity(user_limit_factor: float, capacity: int) -> float:
        return user_limit_factor * capacity

import itertools
import time
import importlib

from multiprocessing import Queue
from threading import Thread

import yaml
from addict import Dict as ADict
from schema import SchemaError
from typing import Dict, Any, List

from pipelines.schema import config_schema


class PipelineExecutor(Thread):

    def __init__(self, yaml_file_path, *args, **kwargs):
        super().__init__(**kwargs)
        self._yaml_path = yaml_file_path
        self._queues = {}
        self._output_queues: Dict[Queue, int] = {}
        self._workers: Dict[str, List[Any]] = {}

    def _get_worker_klass(self, worker):
        module_path = worker.location.replace("/", ".").replace(".py", "")
        try:
            module = importlib.import_module(module_path)
            WorkerKlass = getattr(module, worker.klass)
        except Exception as err:
            raise err
        return WorkerKlass

    def _count_input_queue_consumers(self, queue: Queue, num_of_threads: int):
        if self._output_queues.get(queue) is None:
            self._output_queues[queue] = 0
        self._output_queues[queue] += num_of_threads

    def _get_args_kwargs_klass(self, worker):
        args = ()
        kwargs = {"start": False}

        if worker.input_queue:
            queue = self._queues[worker.input_queue]
            args = (queue,)
            self._count_input_queue_consumers(queue, worker.num_of_threads)
        if len(worker.output_queues) > 0:
            output_queues = []
            for q in worker.output_queues:
                output_queues.append(self._queues[q])
            kwargs["output_queue"] = output_queues[0]  # just one at the minute

        return args, kwargs

    def _load_pipeline(self):
        with open(self._yaml_path, "r") as config:
            config_yaml = yaml.safe_load(config)
            try:
                configuration = ADict(config_schema.validate(config_yaml))
                print("Configuration is valid.")
            except SchemaError as se:
                raise se
            return configuration

    def _initialize_queues(self, queues):
        for queue in queues:
            self._queues[queue.name] = Queue()

    def _initialize_workers(self, workers):
        for worker in workers:
            num_of_threads = worker.num_of_threads
            WorkerKlass = self._get_worker_klass(worker)
            args, kwargs = self._get_args_kwargs_klass(worker)
            self._workers[worker.klass] = []
            for _ in range(num_of_threads):
                self._workers[worker.klass].append(WorkerKlass(*args, **kwargs))

    def _join_workers(self):
        for items in self._workers.values():
            for worker in items:
                worker.join()

    def _run(self):
        for items in self._workers.values():
            for worker in items:
                worker.start()

    def process_pipeline(self):
        data = self._load_pipeline()
        self._initialize_queues(data.queues)
        self._initialize_workers(data.workers)
        self._run()

    def run(self):
        self.process_pipeline()
        total_worker_threads_alive = None
        while total_worker_threads_alive != 0:
            total_worker_threads_alive = 0
            for items in self._workers.values():
                for worker in items:
                    if worker.is_alive():
                        total_worker_threads_alive += 1
            print(f"There are {total_worker_threads_alive} Workers alive")
            if total_worker_threads_alive == 0 and len(self._output_queues.keys()) > 0:
                print(f"Finished queues")
                for queue, consumers_count in self._output_queues.items():
                    for _ in range(consumers_count):
                        queue.put("DONE")
                        print(f"{Queue} finished")

            time.sleep(5)

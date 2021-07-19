import os
import random
from threading import Thread
from typing import Dict, List

# Use @classmethod Polymorphism to Construct Objects Generically

Config = type(Dict[str, str])


class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config: Config):
        raise NotImplementedError


class PathInputData(GenericInputData):
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path

    def read(self) -> str:
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config: Config):
        data_dir = config["data_dir"]
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:
    def __init__(self, input_data) -> None:
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config: Config):
        return [cls(input_data) for input_data in input_class.generate_inputs(config)]


class LineCountWorker(GenericWorker):
    def map(self) -> None:
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other) -> None:
        self.result += other.result


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(worker_class, input_class, config: Config) -> None:
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


def write_test_files(tmpdir: str) -> None:
    if not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), "w") as f:
            f.write("\n" * random.randint(0, 100))


if __name__ == "__main__":
    config = {"data_dir": "test_inputs"}
    write_test_files(config["data_dir"])
    result = mapreduce(LineCountWorker, PathInputData, config)
    print(f"There are {result} lines")

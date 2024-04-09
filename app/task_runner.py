from queue import Queue
from threading import Thread, Event, Lock
from app import helper as hp

import time
import os

class ThreadPool:
    def __init__(self, data_ingestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.data_ingestor = data_ingestor
        self.num_threads = self.get_num_threads()
        self.tasks_queue = Queue()
        self.shutdown_event = Event()
        self.threads = []
        self.lock = Lock()
        self.job_counter = 1
        self.jobs = {}
        
        for _ in range(self.num_threads):
            thread = TaskRunner(self.tasks_queue, self.shutdown_event, self.jobs, self.data_ingestor)
            thread.start()
            self.threads.append(thread)

    def get_num_threads(self):
        if 'TP_NUM_OF_THREADS' in os.environ:
            return int(os.environ['TP_NUM_OF_THREADS'])
        return os.cpu_count()

    def register_job(self, task):
        job_id = self.job_counter
        task['job_id'] = job_id
        self.jobs[job_id] = ("running", -1)
        self.tasks_queue.put(task)
        # print("s-a inregistrat jobul cu job id " + str(job_id) + " si tipul " + str(task['type']))

        with self.lock:
            self.job_counter += 1

        return job_id

    def shutdown(self):
        self.shutdown_event.set()

        for thread in self.threads:
            thread.join()

class TaskRunner(Thread):
    def __init__(self, tasks_queue, shutdown_event, jobs, data_ingestor):
        super().__init__()
        self.tasks_queue = tasks_queue
        self.shutdown_event = shutdown_event
        self.jobs = jobs
        self.data_ingestor = data_ingestor

    def run(self):
        while True:
            # Repeat until graceful_shutdown
            if self.shutdown_event.is_set():
                break
            try:
                # Get pending job
                task = self.tasks_queue.get()

                # Execute job
                job_id = task['job_id']
                # print("SE EXECUTA jobul cu job id " + str(job_id) + " si tipul " + str(task['type']))

                result = self.execute(task)
                # print("s-a intors ")
                # print(result)
                # print(f"Executing job {job_id}")
                
                # Signal that the job is done
                self.jobs[job_id] = ("done", result)
            except:
                continue

    """
        Returns the JSON response for the given data
    """
    def execute(self, data):
        print("INTRU IN EXECUTE")
        if data['type'] == hp.STATES_MEAN:
            return self.states_mean(data)
        elif data['type'] == hp.STATE_MEAN:
            return self.state_mean(data)
        elif data['type'] == hp.BEST5:
            print("IF LA BEST5")
            return self.best5(data)
        elif data['type'] == hp.WORST5:
            return self.worst5(data)
        elif data['type'] == hp.GLOBAL_MEAN:
            return self.global_mean(data)
        elif data['type'] == hp.STATE_DIFF_FROM_MEAN:
            return self.state_diff_from_mean(data)
        elif data['type'] == hp.MEAN_BY_CATEGORY:
            return self.mean_by_category(data)
        elif data['type'] == hp.GRACEFUL_SHUTDOWN:
            return self.graceful_shutdown()
        elif data['type'] == hp.JOBS:
            return self.jobs()
        elif data['type'] == hp.NUM_JOBS:
            return self.num_jobs()

    """
        Returns the mean value for the best 5 states for the given question
    """
    def best5(self, data):
        question = data['question']
        data_value_index = self.data_ingestor.index_dict["Data_Value"]
        question_values = self.data_ingestor.data[question]
        result = {}
        for location in question_values.keys():
            num_values = question_values[location].__len__()
            sum = 0.0

            for field in question_values[location]:
                sum += float(field[data_value_index])

            avg = sum / num_values
            result[location] = avg

        if question in self.data_ingestor.questions_best_is_min:
            return dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[-5:])
        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:5])
    
    def worst5(self, data):
        question = data['question']
        print(question)
        data_value_index = self.data_ingestor.index_dict["Data_Value"]
        question_values = self.data_ingestor.data[question]
        result = {}
        for location in question_values.keys():
            num_values = question_values[location].__len__()
            sum = 0.0

            for field in question_values[location]:
                sum += float(field[data_value_index])

            avg = sum / num_values
            result[location] = avg

        if question in self.data_ingestor.questions_best_is_max:
            return dict(sorted(result.items(), key=lambda item: item[1])[:5])
        return dict(sorted(result.items(), key=lambda item: item[1])[-5:])
    
    def global_mean(self, data):
        return {"Global Mean": 0.0}
    
    def state_diff_from_mean(self, data):
        return {"State Diff From Mean": 0.0}
    
    def mean_by_category(self, data):
        return {"Mean By Category": 0.0}
    
    def graceful_shutdown(self):
        return {"Graceful Shutdown": 0.0}
    
    def states_mean(self, data):
        return {"States Mean": 0.0}
    
    def state_mean(self, data):
        return {"State Mean": 0.0}
    
    def jobs(self):
        return {"Jobs": 0}
    
    def num_jobs(self):
        return {"Num Jobs": 0}
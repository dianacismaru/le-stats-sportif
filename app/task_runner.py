from queue import Queue
from threading import Thread, Event, Lock

import statistics
import os

from app import helper as hp

class ThreadPool:
    """
        Class that manages a pool of threads that execute different jobs
    """
    def __init__(self, data_ingestor):
        self.data_ingestor = data_ingestor
        self.tasks_queue = Queue()
        self.shutdown_event = Event()
        self.threads = []
        self.lock = Lock()
        self.job_counter = 1
        self.jobs = {}

        num_threads = self.get_num_threads()
        for _ in range(num_threads):
            thread = TaskRunner(self.tasks_queue, self.shutdown_event, self.jobs,
                                self.data_ingestor)
            thread.start()
            self.threads.append(thread)

    def get_num_threads(self):
        """
            Returns the number of threads to be used
        """
        if 'TP_NUM_OF_THREADS' in os.environ:
            return int(os.environ['TP_NUM_OF_THREADS'])
        return os.cpu_count()

    def register_job(self, task):
        """
            Registers a new job in the queue and increments the job counter
            Returns the job id of the registered task
        """
        job_id = self.job_counter
        task['job_id'] = job_id
        self.jobs[job_id] = ("running", -1)

        self.tasks_queue.put(task)

        with self.lock:
            self.job_counter += 1

        return job_id

    def graceful_shutdown(self):
        """
            Gracefully shuts down the thread pool
        """
        self.shutdown_event.set()

        for thread in self.threads:
            thread.join()

class TaskRunner(Thread):
    """
        Class that represents a thread that responds to different requests
    """
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
                result = self.execute(task)

                # Signal that the job is done
                self.jobs[job_id] = ("done", result)
            except Exception:
                continue

    def execute(self, data):
        """
            Returns the JSON response for the given data
        """
        result = {}
        question = data['question']

        if data['type'] == hp.STATES_MEAN:
            result = self.states_mean(question)
        elif data['type'] == hp.STATE_MEAN:
            result = self.state_mean(question, data['state'])
        elif data['type'] == hp.BEST5:
            result = self.top5(True, question)
        elif data['type'] == hp.WORST5:
            result = self.top5(False, question)
        elif data['type'] == hp.GLOBAL_MEAN:
            result = self.global_mean(question)
        elif data['type'] == hp.DIFF_FROM_MEAN:
            result = self.diff_from_mean(question)
        elif data['type'] == hp.STATE_DIFF_FROM_MEAN:
            result = self.state_diff_from_mean(question, data['state'])
        elif data['type'] == hp.MEAN_BY_CATEGORY:
            result = self.mean_by_category(question)
        elif data['type'] == hp.STATE_MEAN_BY_CATEGORY:
            result = self.state_mean_by_category(question, data['state'])

        return result

    def top5(self, best, question):
        """
            Returns the mean value for the best or worst 5 states for the given question
        """
        states_dict = self.data_ingestor.data[question]
        result = {}

        for state in states_dict:
            result[state] = statistics.mean(self.data_ingestor.data[question][state]["Data_Value"])

        if question in self.data_ingestor.questions_best_is_min:
            return dict(sorted(result.items(), key=lambda item: item[1], reverse=best)[-5:])
        return dict(sorted(result.items(), key=lambda item: item[1], reverse=best)[:5])

    def global_mean(self, question):
        """
            Returns the global mean value for the given question
        """
        states_dict = self.data_ingestor.data[question]
        num_data = 0
        sum_data = 0

        for state in states_dict:
            sum_data += sum(states_dict[state]["Data_Value"])
            num_data += len(states_dict[state]["Data_Value"])

        return {"global_mean": sum_data / num_data}

    def diff_from_mean(self, question):
        """
            Returns the difference of the global mean value and the mean value for each state 
            for the given question
        """
        global_mean = self.global_mean(question)["global_mean"]
        states_mean = self.states_mean(question)

        return {key: global_mean - value for key, value in states_mean.items()}

    def state_diff_from_mean(self, question, state):
        """
            Returns the difference of the global mean value and the mean value for the specified
            state for the given question
        """
        global_mean = self.global_mean(question)["global_mean"]
        state_mean = self.state_mean(question, state)[state]

        return {state: global_mean - state_mean}

    def mean_by_category(self, question):
        """
            Returns the mean value for each touple of 
            (State, StratificationCategory1, Stratification1)
        """
        states_dict = self.data_ingestor.data[question]
        result = {}

        for state in states_dict:
            state_data = self.data_ingestor.data[question][state]
            for key in state_data:
                if key not in ('Data_Value', "('', '')"):
                    new_key = key[0:1] + f"'{state}', " + key[1:]
                    result[new_key] = statistics.mean(state_data[key])

        return result

    def state_mean_by_category(self,  question, state):
        """
            Returns the mean value for each touple of (StratificationCategory1, Stratification1)
            for the specified state for the given question
        """
        state_data = self.data_ingestor.data[question][state]

        result = {}
        for key in state_data:
            if key != "Data_Value":
                result[key] = statistics.mean(state_data[key])

        return {state: result}

    def states_mean(self, question):
        """
            Returns the mean value for each state for the given question
        """
        states_dict = self.data_ingestor.data[question]
        result = {}

        for state in states_dict:
            state_values = self.data_ingestor.data[question][state]["Data_Value"]
            result[state] = statistics.mean(state_values)

        return dict(sorted(result.items(), key=lambda item: item[1]))

    def state_mean(self, question, state):
        """
            Returns the mean value for the specified state for the given question
        """
        state_values = self.data_ingestor.data[question][state]["Data_Value"]
        result = statistics.mean(state_values)

        return {state : result}

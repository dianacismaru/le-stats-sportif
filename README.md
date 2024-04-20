Copyright (C) 2024 Cismaru Diana-Iuliana (331CA - 2023/2024)

# Le Stats Sportif

Implementation
-

At the beginning of the implementation, I fetch the data from the file `nutrition_activity_obesity_usa_subset.csv` and store it as efficiently as possible, so that I can access the data as quickly as possible when requests are received. Thus, I use a main dictionary, `data`, with the following structure:

    {
        "Question1": {
            "State1": {
                "Data_Value": [value1, value2, ...],
                "('StratificationCategory1', 'Stratification1')": [value1, value2, ...],
                ...
            },
            ...
        },
        ...
    }

   After initializing the date, I create a ThreadPool with a predefined number of
threads that will execute tasks from a `tasks_queue`. As requests come in, jobs are
registered, each being assigned an id. Depending on the type of request, the thread 
handling the job will call the `execute()` function to return the specific answer to 
the input question. These results are written to a file named `{job_id}.json`, and then 
extracted following requests of the type `/api/get_results/{job_id}`. If a job is still 
in progress, the corresponding json will be returned.

   In the event of a request of type `/api/graceful_shutdown`, the ThreadPool's 
shutdown event will be set, and the threads will finish executing the tasks in the queue and close. Any POST request after the graceful shutdown will return an error 
message.

Usage
-
Requirements:
```bash
   make create_venv
   make install
```
To run the server, you need to run the following command:

```bash
   source venv/bin/activate
   make run_server
```

To run the tests, you need to run the following command:

```bash
   source venv/bin/activate
   make run_tests
```

Resources
-
* [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
* [REST Client in VSCode](https://www.youtube.com/watch?v=fmOFjkHvS84&t=252s)
* [Event](https://ocw.cs.pub.ro/courses/asc/laboratoare/03#event)
* [CSV File Reading](https://docs.python.org/3/library/csv.html#csv.DictReader)
* [Json dumps](https://www.geeksforgeeks.org/json-dumps-in-python/)
* [Json loads](https://www.geeksforgeeks.org/json-loads-in-python/)

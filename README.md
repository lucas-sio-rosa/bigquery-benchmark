# BigQuery Benchmarking Tool

This is a simple script designed to help benchmarking Big Query usage. This can be especially useful when benchmarking reservation slots in order to decide if it's worth it.

# Setup

Just install the requirements.txt

## Arguments

* **credential_file**: path to the json file with a service account to authenticate
* **job_prefix**: a string which will be added to all the queries in this execution, making it easier to group this execution when checking the BQ logs
* **query_file**: path to the json file with the queries
* **query_param_list**: OPTIONAL - path to the json file with the parameter list
* **pool_size**: DEFAULT 50 - size of the pool where executions will be stored while they run
* **log_level**: DEFAULT 20 - sets the log level (20 = INFO)

## Files

In order to run, a query file must be supplied, along with an optional parameter file.

The query file is a json file, with a collection of documents, with a single "query" entry on each document, e.g.:

```json
[
    { "query": "SELECT 1 AS a,\n{param1} AS b" },
    { "query": "SELECT 2 AS a,\n{param1} AS b" }
]
```

If you want to use a parameter file, it must be a json file with a list of documents, where each entry must fill all parameters (extra parameters will be ignored but missing ones will fail the program at that moment), e.g.:

```json
[
    { "param1": "1", "param2": "2", "param3": "3" },
    { "param1": "A", "param2": "B", "param3": "C" }
]
```

Parameters will be applied to the queries in round-robin fashion, meaning that the first set will be applied to the first query and so forth. If the parameter list ends, it loops back to the first one.

# Output

Since this is a benchmark tool, the query results are considered unimportant. Setting the log level to DEBUG will allow it to at least be logged, even if it might not be ideal.
Unfortunately, getting execution statistics through the BQ client seems impossible, so it's best to create a sink in Stackdriver Logging to analyze the results in BQ as shown [here](https://medium.com/google-cloud/visualize-gcp-billing-using-bigquery-and-data-studio-d3e695f90c08).

# Author

* [**Lucas Rosa**](https://github.com/lucas-sio-rosa)
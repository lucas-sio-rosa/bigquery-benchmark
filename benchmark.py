from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import bigquery as bq
from datetime import datetime as dt

import argparse
import json
import logging
import time

if __name__ == "__main__":
    start_time = time.time()
    
    threads = []
    results = []

    parser = argparse.ArgumentParser()

    parser.add_argument('credential_file', help='The path to a json credential file to authenticate the client')
    parser.add_argument('job_prefix', help='The job prefix to be added to the BQ jobs')
    parser.add_argument('query_file', help='The json file with a list of queries to be executed simultaneously')
    parser.add_argument('--query_param_list', help='The json file with a list of parameters to be supplied to the query in round-robin fashion')
    parser.add_argument('--pool_size', default=50, type=int, help='Sets the logging level (default INFO)')
    parser.add_argument('--log_level', default=20, type=int, choices=(0, 10, 20, 30, 40, 50), help='Log level')

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    executor = ThreadPoolExecutor(args.pool_size)
    client = bq.Client.from_service_account_json('/home/lucas/Downloads/teste-r.json')

    job_config = bq.job.QueryJobConfig(use_legacy_sql=False, use_query_cache=False)

    with open(args.query_file, 'r') as q:
        query_list = json.loads(q.read())
    
    param_list = None
    if args.query_param_list:
        with open(args.query_param_list, 'r') as p:
            param_list = json.loads(p.read())
    
    setup_time = time.time()
    job_list = []
    param_index = 0
    param_reset = len(param_list) - 1 if param_list else 0
    for q in query_list:
        if param_list:
            query = q['query'].format(**param_list[param_index])
            logging.debug(query)
        else:
            query = q['query']
            logging.debug(query)

        job = client.query(query, job_id_prefix=args.job_prefix, job_config=job_config)
        threads.append(executor.submit(job.result))
        param_index = param_index + 1 if param_index < param_reset else 0

    sent_time = time.time()
    for future in as_completed(threads):
        results.append(list(future.result()))
        
    logging.debug('Execution results: {}'.format(results))
    logging.info('Start time: {}'.format(dt.utcfromtimestamp(start_time).isoformat()))
    logging.info('Time spent in setup: {}, {}s'.format(dt.utcfromtimestamp(setup_time).isoformat(), setup_time - start_time))
    logging.info('Time spent in execution: {}, {}s'.format(dt.utcfromtimestamp(sent_time).isoformat(), sent_time - setup_time))
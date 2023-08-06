from __future__ import print_function
import pymongo
import json
from time import sleep


# for python 2, 3 compatible
def _parse_data(data):
    # python3
    if isinstance(data, bytes):
        return json.loads(data.decode("utf-8"))
    # python2
    return json.loads(data)


def _get_job_id_stdout_line(message, job_id):
    if not message or message["type"] != "message":
        return None

    parsed_data = _parse_data(message["data"])
    if parsed_data.get("jobId", "") != job_id:
        return None

    return parsed_data.get("line", "")


def get_log_from_container(host, job_id, port=13206):
    client = pymongo.MongoClient(host, port)
    collection = client.logs.joblogs
    print(collection)

    # line = ""
    # while line != "[SYSTEM] Train completed.":
    #     sleep(0.1)
    #     line = _get_job_id_stdout_line(p.get_message(), job_id)
    #     if line:
    #         print(line)


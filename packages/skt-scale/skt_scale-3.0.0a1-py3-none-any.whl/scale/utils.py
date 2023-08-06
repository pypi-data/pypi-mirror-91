from __future__ import print_function
import sys
import pymongo
import json
from time import sleep


def convert_source_file_to_user_command(source_file):
    with open(source_file, "r") as f:
        content = f.read()

    return """cat <<EOF > app.py
{}
EOF
python app.py""".format(
        content
    )


def get_job_body(job_name, image_name, gpu_type, gpu, cpu, mem, user_cmd):
    return {
        "jobName": job_name,
        "imageName": image_name,
        "gpuType": gpu_type,
        "gpu": gpu,
        "cpu": cpu,
        "mem": mem,
        "comment": "",
        "userCmd": user_cmd,
        "tags": [],
        "interactive": False,
    }


def print_container_log(host, job_id, port=13206):
    client = pymongo.MongoClient(host, port)
    collection = client.logs.joblogs

    def get_documents(skip):
        cursor = collection.find(
            {"jobId": job_id},
            sort=[("lineNo", pymongo.ASCENDING)],
            projection={"line": True, "lineNo": True},
            skip=skip,
            limit=10,
        )
        return list(cursor)

    while len(get_documents(0)) == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
        sleep(1)

    line = ""
    skip = 0

    while line != "[SYSTEM] Train completed.":
        documents = get_documents(skip)
        if len(documents) == 0:
            sleep(1)
        for document in documents:
            line = document.get("line")
            line_no = document.get("lineNo")
            skip = line_no
            print(line)
        sleep(0.1)


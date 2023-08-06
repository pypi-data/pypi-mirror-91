import re
import os
import sys
import time
import fire
import requests
import json
import getpass
from scale.utils import (
    get_job_body,
    convert_source_file_to_user_command,
    print_container_log,
)


class Client(object):
    def __init__(self, endpoint=None, secret=None):
        self.config_dir = os.path.join(os.environ.get("HOME", "/tmp"), ".scale")
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        self.config_path = os.path.join(self.config_dir, "config")
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w+") as f:
                default = {"endpoint": None, "secret": None}
                json.dump(default, f)

        with open(self.config_path, "r") as f:
            self.conf = json.load(f)
        if endpoint:
            self.conf["endpoint"] = endpoint
        if secret:
            self.conf["secret"] = secret

    def _config_check(self):
        if not self.conf["secret"]:
            print("configure first before create job\nex) scalecli configure")
            sys.exit(1)

    def configure(self):
        self.conf["secret"] = self._get_input("secret")
        self.conf["endpoint"] = self._get_input("scale endpoint")
        with open(self.config_path, "w") as f:
            json.dump(self.conf, f)

    def _get_input(self, name):
        input_str = ""
        if sys.version_info[0] == 2:
            input_str = raw_input("Enter %s: ", name)
        else:
            input_str = input(f"Enter {name}: ")
        return input_str.strip()

    def create_job(
        self,
        job_name,
        image_name,
        source_file,
        gpu_type=None,
        gpu=0,
        cpu=1,
        mem=1,
    ):
        if not gpu_type and gpu > 0:
            print("gpu type is null but gpu count > 0")
            return
        self._config_check()
        user_cmd = convert_source_file_to_user_command(source_file)
        body = get_job_body(
            job_name=job_name,
            image_name=image_name,
            gpu_type=gpu_type,
            gpu=gpu,
            cpu=cpu,
            mem=mem,
            user_cmd=user_cmd,
        )
        try:
            r = requests.post(
                "http://{}/api/v3/paas/batch/job".format(
                    self.conf.get("endpoint")
                ),
                json=body,
                headers={
                    "Authorization": "Bearer {}".format(self.conf.get("secret"))
                },
            )
            if r.status_code != 200:
                print(r.text)
                return
            job_id = r.json()["jobId"]
            print("job id: ", job_id)
            host = re.search(r"(.*):\d+", self.conf["endpoint"]).group(1)
            print_container_log(host, job_id)

        except requests.exceptions.RequestException as e:
            print(e)

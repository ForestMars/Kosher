# dockerize_model.py - Package a trained domain model in a docker image, copy to remote server, and run it.

import os
import sys

from common import cli


args = cli.get_args(sys.argv)

DOMAIN = args.domain or 'hackles' # example domain
DOCKER_HOST = args.docker_host or '3.12.163.71'
DOCKER_USER = args.docker_user or 'ubuntu'
KEY = args.host_key or None
FLASK_PORT = args.port or 5531

DIR = 'images/'
IMAGE_NAME=DOMAIN
FILE_NAME = DIR + IMAGE_NAME + '_latest.tar'


build_cmd = "docker build -f build/predict/Dockerfile --build-arg FLASK_RUN_PORT={flask_port} -t {image_name} .".format(
    flask_port=FLASK_PORT,
    image_name=IMAGE_NAME,
    )
save_cmd = "docker save {image_name}:latest > {file_name}".format(
    image_name=IMAGE_NAME,
    file_name=FILE_NAME,
    )

os.system(build_cmd)
os.system(save_cmd)


if __name__ == '__main__':
    # For testing & development only. We use ansible/airflow to move our dockerized model.
    os.system("scp -i {key} {filename} {user}@{host}:~/".format(
        key=KEY,
        user=DOCKER_USER,
        host=DOCKER_HOST,
        filename=FILE_NAME,
        )
    )

    LOAD_CMD="ssh -i {key} {user}@{host} docker load -i {filename}".format(
        key=KEY,
        user=DOCKER_USER,
        host=DOCKER_HOST,
        filename=FILE_NAME,
        )
    os.system(LOAD_CMD)

    if USE_REDIS is not None:
        REDIS = "--link my-redis-container:redis"
    else:
        REDIS = ''

    RUN_CMD = "ssh -i {key} {user}@{host} docker run --expose {port} -p {port}:{port} {image_name} {redis}".format(
        key=KEY,
        user=DOCKER_USER,
        host=DOCKER_HOST,
        filename=FILE_NAME,
        port=FLASK_PORT,
        image_name=IMAGE_NAME,
        redis=REDIS
        )
    os.system(RUN_CMD)

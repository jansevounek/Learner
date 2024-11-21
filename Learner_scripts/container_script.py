import docker
import re
import time
import sys
import logging
from logger import CircularBufferHandler

docker = docker.from_env()

# taken from https://stackoverflow.com/questions/17544307/how-do-i-run-python-script-using-arguments-in-windows-command-line
ram_limit = float(sys.argv[1])
load_limit = float(sys.argv[2])
log_file = str(sys.argv[3])
prefix = str(sys.argv[4])

def main():
    logger, handler = setup_logger(log_file, max_logs=1000)
    while True:
        time.sleep(1)
        containers = get_named_containers(prefix)

        if len(containers) == 0:
            logger.debug('No containers with prefix "' + str(prefix) + '" found')
            break
        
        for container in containers:
            stats = container.stats(decode=True)

            for stat in stats:
                if (stat['memory_stats']):
                    memory_usage = stat['memory_stats']['usage']
                    memory_limit = stat['memory_stats']['limit']
                    memory_percentage = float((memory_usage / memory_limit) * 100)
                    if (ram_limit < memory_percentage):
                        logger.debug("container: " + container.name + " stopped")
                        container.stop()
                    logger.debug("container: " + container.name + " is running and using " + str(memory_percentage))
                else:
                    logger.debug("container: " + container.name + " is not running")
        
                handler.flush_to_file()

    handler.flush_to_file()


def get_named_containers(name_prefix):
    client = docker.from_env()
    containers = client.containers.list(all=True)
    matching_containers = []

    for container in containers:
        if container.name.startswith(name_prefix):
            matching_containers.append(container)

    return matching_containers

def setup_logger(log_file, max_logs=100):
    logger = logging.getLogger("CircularLogger")
    logger.setLevel(logging.DEBUG)

    handler = CircularBufferHandler(log_file, max_logs)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, handler

main()

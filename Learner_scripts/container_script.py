import pprint
import docker, time, sys, logging, itertools
from datetime import datetime, timezone, timedelta
from CircularBufferHandler import CircularBufferHandler

docker = docker.from_env()

# taken from https://stackoverflow.com/questions/17544307/how-do-i-run-python-script-using-arguments-in-windows-command-line
ram_limit = float(sys.argv[1])
load_limit = float(sys.argv[2])
log_file = str(sys.argv[3])
prefix = str(sys.argv[4])

def main():
    logger, handler = setup_logger(log_file, max_logs=1000)
    while True:
        containers = get_named_containers(prefix)
        time.sleep(len(containers))

        if len(containers) == 0:
            logger.debug('No containers with prefix "' + str(prefix) + '" found')
            break
        
        for container in containers:
            if container.status == "running":
                container.reload()
                #exec_id = container.attrs["ExecIDs"]
                stats = container.stats(decode=True)

                logs = container.logs(timestamps=True).decode('utf-8').strip()

                last_log_line = logs.split('\n')[-1]
                timestamp_str, message = last_log_line.split(' ', 1)

                last_interaction_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

                elapsed = datetime.now(last_interaction_time.tzinfo) - last_interaction_time

                uptime = get_container_uptime(container)
                logger.debug("Containers: " + container.name + " uptime is " + str(uptime))

                if uptime > timedelta(minutes=1):
                    # taken from https://medium.com/@martinkarlsson.io/control-and-monitor-your-docker-containers-with-python-7a3bdc4b88fa
                    for stat in itertools.islice(stats, 1):
                        memory_percentage = get_memory_percantage(stat)
                        if (ram_limit < memory_percentage):
                            logger.debug("container: " + container.name + " stopped - ram limit exceeded")
                            container.stop()
                        logger.debug("container: " + container.name + " is running and using: " + f"{memory_percentage:.2f}%" + " ram")

                        handler.flush_to_file()

                    if not check_container_timeout(container, logger):
                        logger.debug("container: " + container.name + " stopped - timeout")
                        container.stop()
                        handler.flush_to_file()

                else:
                    logger.debug("container: " + container.name + " is not yet running for more then 1 minute -> not taking action")
                    handler.flush_to_file()
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

def get_container_uptime(container):
    started_at = container.attrs['State']['StartedAt']
    
    started_at_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))

    now = datetime.now(timezone.utc)
    uptime = now - started_at_dt

    return uptime

def check_container_timeout(container, logger):
    logs = container.logs(timestamps=True).decode('utf-8').strip()

    last_log_line = logs.split('\n')[-1]
    timestamp_str, message = last_log_line.split(' ', 1)

    last_interaction_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

    elapsed = datetime.now(last_interaction_time.tzinfo) - last_interaction_time

    logger.debug("ltime since container: " + container.name + " received last command: " + str(elapsed))

    if elapsed > timedelta(seconds=30):
        return False
    
    return True

def get_memory_percantage(stat):
    memory_stats = stat.get('memory_stats', {})
    memory_usage = memory_stats.get('usage', 0)
    memory_limit = memory_stats.get('limit', 1)

    memory_limit = max(memory_limit - memory_stats.get('stats', {}).get('cache', 0), 1)

    ram_percentage = (memory_usage / memory_limit) * 100

    return ram_percentage

def setup_logger(log_file, max_logs=100):
    logger = logging.getLogger("CircularLogger")
    logger.setLevel(logging.DEBUG)

    handler = CircularBufferHandler(log_file, max_logs)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, handler

main()

import os, requests, json
from time import sleep
import docker, sys, logging, itertools
from datetime import datetime, timezone, timedelta
from CircularBufferHandler import CircularBufferHandler
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

docker = docker.from_env()

# taken from https://stackoverflow.com/questions/17544307/how-do-i-run-python-script-using-arguments-in-windows-command-line
load_limit = float(sys.argv[1])
network_limit = float(sys.argv[2])
container_name = str(sys.argv[3])

MAX_NETWORK = 50
LOG_FILE = "logs/" + container_name + ".log"

network_load_limit = MAX_NETWORK * (network_limit / 100)

previous_networks_stats = {}

def main():
    logger, handler = setup_logger(LOG_FILE, max_logs=1000)
    while True:
        sleep(2)

        try:
            container = docker.containers.get(container_name)
        except Exception as e:
            logger.debug('No containers with name "' + str(container_name) + '" found')
            handler.flush_to_file()
            break
        
        if container.status == "running":
            output = "Container: " + container.name + "\n"
            container.reload() 
            stats = container.stats(decode=True)
            uptime = get_container_uptime(container)
            output += " - uptime: " + str(uptime) + "\n"
            if uptime > timedelta(minutes=1):
                memory = check_container_memory(stats)
                if not memory:
                    logger.debug("container: " + container.name + " stopped - ram limit exceeded")
                    stop_container(container)
                else:
                    output += memory
                timeout = check_container_timeout(container)
                if not timeout:
                    logger.debug("container: " + container.name + " stopped - timeout")
                    stop_container(container)
                else:
                    output += timeout
                network = check_container_network(stats, container)
                if not network:
                    logger.debug("container: " + container.name + " stopped - netwrok limit exceeded")
                    stop_container(container)
                else:
                    output += network
            else:
                output += " - running more then a minute: False \n"
            
            logger.debug(output)
            handler.flush_to_file()
            
        else:
            logger.debug("Container: " + container.name + " is not running")
            handler.flush_to_file()

    handler.flush_to_file()

def get_container_uptime(container):
    started_at = container.attrs['State']['StartedAt']
    
    started_at_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))

    now = datetime.now(timezone.utc)
    uptime = now - started_at_dt

    return uptime

def check_container_timeout(container):
    logs = container.logs(timestamps=True).decode('utf-8').strip()

    last_log_line = logs.split('\n')[-1]
    timestamp_str, message = last_log_line.split(' ', 1)

    last_interaction_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

    elapsed = datetime.now(last_interaction_time.tzinfo) - last_interaction_time

    if elapsed > timedelta(minutes=2):
        return False
    
    return " - last activity: " + str(elapsed) + "\n"

def check_container_network(stats, container):
    for stat in itertools.islice(stats, 1):
        if container.name in previous_networks_stats:
            prev_stat = previous_networks_stats.get(container.name)

            rx_delta = stat['networks']['eth0']['rx_bytes'] - prev_stat["last_rx"]
            tx_delta = stat['networks']['eth0']['tx_bytes'] - prev_stat["last_tx"]

            previous_networks_stats.get(container.name)["last_rx"] = stat['networks']['eth0']['rx_bytes']
            previous_networks_stats.get(container.name)["last_tx"] = stat['networks']['eth0']['tx_bytes']

            if rx_delta / 1_000_000 > network_load_limit or tx_delta / 1_000_000 > network_load_limit:
                return False
            
            rx_percent = (rx_delta / 1_000_000) / (network_load_limit / 100)
            tx_percent = (tx_delta / 1_000_000) / (network_load_limit / 100)
            
            return " - network out: " + str(rx_delta / 1_000_000) + " mb (" + f"{rx_percent:.2f}%" + ") \n" + " - network in: " + str(tx_delta / 1_000_000) + " mb (" + f"{tx_percent:.2f}%" + ") \n"
        else:
            previous_networks_stats.update({ 
                container.name: {
                    "last_rx": stat['networks']['eth0']['rx_bytes'],
                    "last_tx": stat['networks']['eth0']['tx_bytes']
                }
            })
            
            return " - network: Not yet calculated"

def check_container_memory(stats):
    # taken from https://medium.com/@martinkarlsson.io/control-and-monitor-your-docker-containers-with-python-7a3bdc4b88f
    for stat in itertools.islice(stats, 1):
        memory_percentage = get_memory_percantage(stat)
        if (load_limit < memory_percentage):
            return False

        return " - memory usage: " + f"{memory_percentage:.2f}%" + "\n"

def get_memory_percantage(stat):
    memory_stats = stat.get('memory_stats', {})
    memory_usage = memory_stats.get('usage', 0)
    memory_limit = memory_stats.get('limit', 1)

    memory_limit = max(memory_limit - memory_stats.get('stats', {}).get('cache', 0), 1)

    ram_percentage = (memory_usage / memory_limit) * 100

    return ram_percentage

def stop_container(container):

    # taken from https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/
    url = os.getenv("VITE_API_URL") + "/lessons/user/stop-container"

    #taken from https://www.geeksforgeeks.org/get-post-requests-using-python/
    response = requests.post(url=url, data=json.dumps({"name": container.name}), headers={'Content-Type': 'application/json'})
    j = response.json()

    if j.get("status"):
        sys.exit()


def setup_logger(log_file, max_logs=100):
    logger = logging.getLogger("CircularLogger")
    logger.setLevel(logging.DEBUG)

    handler = CircularBufferHandler(log_file, max_logs)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, handler

main()

import docker

docker = docker.from_env()

__all__ = ["docker"]
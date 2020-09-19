import os
from distutils.util import strtobool

LOCALHOST = '127.0.0.1'


class BaseConfig:
    API_HOST = LOCALHOST
    API_PORT = 5000
    RABBITMQ_HOST = LOCALHOST
    DOCKER_URI = 'unix://var/run/docker.sock'

    def __init__(self):
        env_vars = [v for v in os.environ.keys() if (v in vars(BaseConfig)) and not v.startswith('__')]
        [self.apply_env_var(k) for k in env_vars]

    def apply_env_var(self, env_var) -> None:
        v = os.environ[env_var]

        try:
            type_ = type(getattr(BaseConfig, env_var))
            if type_ is bool:
                v = strtobool(v)
            else:
                v = type_(v)
        except (TypeError, ValueError):
            print(f'[FAILED] TYPE CASTING ENV VARIABLE {env_var} TO TYPE {type(getattr(BaseConfig, env_var))}')
            print(f'[FAILED] ENV VARIABLE {env_var} MAY PRODUCE AN UNEXPECTED ERROR')

        setattr(self, env_var, v)

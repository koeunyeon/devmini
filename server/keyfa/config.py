import os
import yaml


class RdbConfig:
    type: str
    echo: bool
    host: str
    port: int
    dbname: str
    username: str
    userpass: str

    @classmethod
    def get_url(cls):
        url = "mysql+aiomysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
            cls.username,
            cls.userpass,
            cls.host,
            cls.port, 
            cls.dbname
        )

        return url

class ServerConfig:
    host: str
    port: str
    reload: bool

class LogConfig:
    path: str
    name: str

class ExtraConfig:
    pass

class Config:
    name: str
    rdb: RdbConfig = RdbConfig
    server: ServerConfig = ServerConfig
    log: LogConfig = LogConfig
    extra: ExtraConfig = ExtraConfig

    _conf_dict: dict

    @classmethod
    def load(cls):
        env = os.getenv("env", "dev")
        with open(f"config/{env}.yaml", 'r', encoding='utf-8') as f:
            cls._conf_dict = yaml.load(f, Loader=yaml.FullLoader)
        
        cls.name = cls._conf_dict["name"]
        #cls.rdb = RdbConfig
        #cls.server = ServerConfig
        composit_keys = ["rdb", "server", "log", "extra"]

        for yaml_key in composit_keys:
            target_class = getattr(cls, yaml_key)
            for k, v in cls._conf_dict[yaml_key].items():                
                setattr(target_class, k, v)

Config.load()

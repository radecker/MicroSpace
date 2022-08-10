import yaml


class ConfigLoader():
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.__config_data = None   # Dictionary of config data

    def __parse_params(self):
        pass

    def read_config(self):
        with open(self.config_path, 'r') as stream:
            try:
                self.__config_data = yaml.safe_load(stream)
                return self.__config_data
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def get_config_data(self):
        return self.__config_data


if __name__=="__main__":
    config_fp = "/home/jhu-ep/InSECTS-Vehicle-Testbed/main_service/config.yaml"
    cl = ConfigLoader(config_path=config_fp)
    data = cl.read_config()
    print(data)

import yaml
import inspect
import traceback


def load_yaml_file(path):
    try:
        with open(path, 'r') as file:
            try:
                return yaml.unsafe_load(file)
            except yaml.YAMLError:
                traceback.print_exc()
    except FileNotFoundError:
        traceback.print_exc()


def get_param_names(method):
    assert callable(method)
    sig = inspect.signature(method)
    parameters = [p for p in sig.parameters.values() if p.name != 'self' and p.kind != p.VAR_KEYWORD]
    return sorted([p.name for p in parameters])

import importlib.resources as pkg_resources

def get_data_path(dir):
    if __package__:
        return str(pkg_resources.files(__package__).joinpath(dir))
    else:
        return dir
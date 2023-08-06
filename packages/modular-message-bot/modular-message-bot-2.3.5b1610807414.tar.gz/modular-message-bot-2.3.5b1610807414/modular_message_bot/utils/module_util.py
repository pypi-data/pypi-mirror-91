from importlib import import_module

from modular_message_bot.utils.common_utils import dir_files, root_dir


def get_module_definition(module: str, name: str):
    """
    Gets a definition from module if it exists
    :param module: str
    :param name: str
    :return: Callable|None
    """
    try:
        module = import_module(module)
        if not hasattr(module, name):
            return None
        definition = getattr(module, name)
        return definition
    except ModuleNotFoundError:
        # No extension if the module is not found
        return None


def get_extension(name: str):
    """
    Gets an extension from extensions.py if it exists
    :param name: str
    :return: Callable|None
    """
    return get_module_definition("modular_message_bot.extension", name)


def get_handler_files(name: str) -> list:
    folder = f"{root_dir()}/modular_message_bot/handlers/{name}"
    file: str
    results = []
    for file in dir_files(folder):
        if file.startswith("abstract"):
            continue
        if file.startswith("_"):
            continue
        file_full = f"{folder}/{file}"
        results.append(file_full)
    return results


def get_handler_module_name(file_full: str) -> (str, str):
    # "/some/root/path/modular_message_bot/handlers/inputs/github_prs_input.py"
    # to
    # "modular_message_bot.handlers.inputs.github_prs_input.GithubPrsInput"
    remove_prefix_length = len(root_dir()) + 1
    remove_suffix_length = -len(".py")
    relative_path = file_full[remove_prefix_length:remove_suffix_length]
    module_path = relative_path.replace("/", ".")
    file_name = module_path.split(".")[-1]
    module_name_parts = [x.capitalize() for x in file_name.split("_")]
    return module_path, "".join(module_name_parts)


def get_handlers_module_definitions(name: str) -> list:
    results = []
    for file in get_handler_files(name):
        module_name, class_definition_name = get_handler_module_name(file)
        results.append(get_module_definition(module_name, class_definition_name))
    return results

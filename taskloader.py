import importlib
import logging
import os
import pkgutil

package_path = os.path.dirname(__file__)


# package_name = os.path.basename(package_path)


def load_plugin_modules(task_directory: str) -> list:
    plugins = []
    importlib.invalidate_caches()
    for _, module_name, _ in pkgutil.iter_modules([task_directory]):
        module = task_directory + '.' + module_name
        logging.debug(f'Import task module {module}')
        plugins.append(
            importlib.import_module(module)
        )
    return plugins

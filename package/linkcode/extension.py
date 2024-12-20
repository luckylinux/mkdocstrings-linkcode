# Import Core Libraries
import ast
import griffe
import sys
import pprint
import yaml
from pathlib import Path as Path

# Import Custom Libraries
# ...

# Setup Logger
logger = griffe.get_logger(__name__)

# Reference: https://mkdocstrings.github.io/griffe/reference/api/
# Example: https://mkdocstrings.github.io/griffe/guide/users/extending/

# MkDocs Configuration
CONFIG_FILE = "mkdocs.yml"
CONFIG_DATA = dict[str, str]()


# Load Configuration
# (Only required because it's not clear how to Access Parameters from `mkdocs.yml` from within Griffe Extensions)
def load_config():
    # Allow Function to modify Global Variable
    global CONFIG_DATA

    # Load Configuration if not done already
    if len(CONFIG_DATA) == 0:
        with open(CONFIG_FILE, 'r') as f:
            # Open YAML File in Safe Mode
            config = list(yaml.load_all(f, Loader=yaml.SafeLoader))

            if config is not None and len(config) > 0:
                # Unpack the List
                data = config[0]

                # Set Config
                CONFIG_DATA = data


# Class Definition
class LinkToGitHubSource(griffe.Extension):
    # Class Constructor
    def __init__(self, object_paths: list[str] | None = None) -> None:
        # Store Object Paths
        self.object_paths = object_paths

        # Initialize Config if not done already
        load_config()

    # Process Object and create link to Repository
    def on_instance(
        self,
        *,
        node: ast.AST | griffe.ObjectNode,
        obj: griffe.Object,
        agent: griffe.Visitor | griffe.Inspector,
        **kwargs,
    ) -> None:

        # Get Settings Dictionary
        # This is a bit tricky because Jinja2 Template has only access to the Items under `plugins` -> `mkdocstrings` -> `handlers` -> `python` -> `options`
        # The Jinja2 Template Renderer does NOT expose Context for MkDocs own Parameters into MkDocStrings
        # With the `yaml` Parser CONFIG_DATA Also makes MkDocs own Parameters Accessible so we can e.g. use `repo_url` as well as other Parameters
        plugins = CONFIG_DATA.get("plugins", {})
        repo_url = CONFIG_DATA['repo_url']
        options = None

        # Get the `options` Dictionary (need to process like this because plugins can be a list[] of different Types, e.g. `str` and `dict`)
        for item in plugins:
            if isinstance(item, dict):
                key = list(item.keys())[0]
                if key == "mkdocstrings":
                    content = item.get("mkdocstrings")
                    options = content.get("handlers", {}).get("python", {}).get("options", {})

        # Check if it's relevant to the Package we are Documenting / we want to Document (`python_namespace``)
        if options is not None and options.get("python_namespace") in obj.canonical_path:
            if isinstance(node, griffe.ObjectNode):
                return  # Skip runtime objects, their docstrings are already right.

            if self.object_paths and obj.path not in self.object_paths:
                return  # Skip objects that were not selected.

            # Source Code Start Line
            line_start = obj.lineno
            # logger.debug(f"\tObject Source Code Line Start: {line_start}")

            # Source Code End Line
            line_end = obj.endlineno
            # logger.debug(f"\tObject Source Code Line End: {line_end}")

            if line_start is not None and line_end is not None:
                # Mainly for Debug Purposes
                line_delta = line_end - line_start
                line_count = len(obj.lines)
                # logger.debug(f"\tObject Source Code Line Delta: {line_delta}")
                # logger.debug(f"\tObject Source Code Line Count: {line_count}")

                # Get Relative File Path (relative to the Current Directory = Root of the Repository Source Code)
                file_relative_path = Path(obj.filepath).relative_to(Path().cwd())

                # Set GitHub Link based on Branch Name
                # setattr(obj, "source_link", f"{CONFIG_DATA['repo_url']}/tree/{options.get('repo_branch')}/{file_relative_path}#L{line_start}-L{line_end}")

                # Set GitHub Link based on Short Commit Hash
                # setattr(obj, "source_link", f"{CONFIG_DATA['repo_url']}/blob/{options.get('repo_reference_short')}/{file_relative_path}#L{line_start}-L{line_end}")

                # Set GitHub Link based on Long Commit Hash
                setattr(obj, "source_link", f"{repo_url}/blob/{options.get('repo_reference_long')}/{file_relative_path}#L{line_start}-L{line_end}")

                # Stop here
                return
            else:
                # Nothing to do
                return
        else:
            # Nothing to do
            return

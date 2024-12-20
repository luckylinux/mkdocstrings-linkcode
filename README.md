# mkdocstrings-linkcode
Extension for mkdocstrings to Link Source Code to GitHub

# Introduction
A minimal Reproduction Example is shown here containing:
- `package`: the Extension itself
- `docs/mkdocs/templates` the Templates Overrides to display the Link to the Repository Source Code
- `mkdocs.yml` or `mkdocs.yml.jinja2`: an Example of Configuration for the whole Project

# Configuration
The Configuration is to be defined in `mkdocs.yml`.

It needs to be located under under `plugins` -> `mkdocstrings` -> `handlers` -> `python` -> `options`.

```
# ...
# ...

plugins:
- mkdocstrings:
    # Python is the Default Handler
    default_handler: python

    # Custom Templates to use
    # Relative to Project Root
    custom_templates: docs/mkdocs/templates

    # Handlers
    handlers:
      python:
          # ...
          # ...

          ########################################################################
          ################ SOURCE LINK CONFIGURATION PARAMETERS ##################
          ########################################################################

          # Repository Branch - e.g. e.g. Obtained via `git branch`
          repo_branch: {{ package['repository_current_local_branch'] }}
          
          # Repository Reference Long Hash - e.g. Obtained via `git log -1 --format=%H`
          repo_reference_long: {{ package['repository_current_reference_long'] }}
          
          # Repository Reference Short Hash - e.g. Obtained via `git log -1 --format=%h`
          repo_reference_short: {{ package['repository_current_reference_short'] }}
          
          # Python Namespace
          python_namespace: {{ package['namespace'] }}

          # Show Link to Repository Source Code
          show_source_link: true

          # Label for Repository Source Code
          source_link_label: GitHub Repository

          ########################################################################
          ######################## SOURCE LINK EXTENSION #########################
          ########################################################################

          # Extensions
          extensions:
            - package.linkcode
```

# Extension
The Extension itself is located in the `package` Folder and is named `package.linkcode`.

# Template Override
The Template Overrides are defined in `docs/mkdocs/templates`.

There were some Debug Messages that Overriding `_base` is not supported/reccomended and the Files in the Parent Folder should be modified instead.

I didn't manage to try that yet and it seems to works just fine like this :rofl:.

Some better CSS Stylesheets can/should be applied in the Future.

# Extra Stylesheets
An extra Stylesheet is located in `docs/mkdocs/source/extra.css`.

This is NOT required for the Functionality, but makes it a bit easier to separate one Function/Method/Attribute from each Othe :wink:.
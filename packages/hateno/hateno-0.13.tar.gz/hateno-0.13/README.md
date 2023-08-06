# Hateno

This package helps you manage your simulations, based on their settings. To be handled by this package, a simulation must be launched from a command line and must save its output into a folder. This folder is then stored by the manager into a base directory and can be retrieved by using its settings. The base directory is a simple folder containing a configuration file where all the details about the simulations are listed.

If a simulation does not exist, this package can generate the scripts to create it. These scripts can then be sent to any computer to be executed. Then, the results can be automatically downloaded and added to the base directory without any efforts.

*Note: this README is under construction.*

## Base directory and configuration file

The base directory used by the manager is a folder initialized with a `.simulations.conf` file. This file contains, in JSON format, the details about your simulations, especially the settings they accept and their output file(s).

### Configuration keys

The configuration file must contain the definition of a dictionary, with available keys listed in the table below.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`name` | Required | string | Name of the program.
`description` | Optional | string | A description of the program.
`exec` | Required | string | The base command to launch a simulation.
`setting_pattern` | Required | string | The pattern to use to include the settings in a simulation's command line. The tag `{name}` is replaced by the name of the setting and `{value}` is replaced by its value.
`output` | Required | dictionary | Description of all the files and folders a simulation can create. See a complete description below.
`globalsettings` | Required | list | A complete list of global settings a simulation can use (see below).
`settings` | Required | list | A complet list of settings a simulation can use (see below).
`fixes` | Optional | list | The list of fixes to apply to each setting (see below).

### Output of a simulation

#### Output files

A simulation must write its output into a unique folder, this folder being stored by the manager. The complete list of files that can be generated are listed in the `output` key of the configuration file, in a dictionary with keys described in the table below. Details follow.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`files` | Required | list | The list of generated files, each being a dictionary.
`folders` | Optional | list | The list of generated folders, also as dictionaries.
`checks` | Optional | list | List of checks to apply to the global output.

Files and folders are described by a dictionary with two possible keys, described below.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`name` | Required | string | Name of the file/folder. Wildcard is allowed, as well as the `{setting}` and `{globalsetting}` tag (see details below).
`checks` | Optional | list | List of integrity checks to apply to this file/folder.

#### Integrity checks

Sometimes, things go wrong and a simulation is not run as usual. Such simulations, without the expected output, shouldn't be stored. When simulations are added to the manager, integrity checks can be applied to each file or folder individually, or to the global list of files/folders. If at least one check fails, the simulation is not added to the manager. Some checkers are available by default and described in the table below.

Checker | Type | Description
------- | ---- | -----------
`exists` | file/folder | Succeeds only if the file/folder exists.
`notEmpty` | file | Fails if the file is empty.
`notEmpty` | folder | Fails if the folder does not contain any file.
`noMore` | global | Fails if an unknown file/folder is present in the generated tree.

### Global settings

A global setting represents an information about the simulation. It is not necessarily aimed to be passed as an argument to the command line. A global setting is defined as a dictionary with keys described in the table below. Note that you must always have a global setting named `folder`, indicating the path where the simulation can be found.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`name` | Required | string | Name of the global setting.
`default` | Required | mixed | Default value of the global setting.
`generators` | Optional | list | List of generators to use with this global setting (see the description of the simulations generator).

### Settings

Settings represent the definition of a simulation. They are organized in sets. The idea is that, if a setting is included, all settings of its set are included too. The settings list is a list of sets, defined by a dictionary with keys described in the table below.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`set` | Required | string | Name of the set.
`required` | Optional | boolean | If `true`, the settings of the sets are always included. If `false`, the set is included only if at least one setting is defined in the simulation to manage.
`settings` | Required | list | List of settings in the set.

Each setting is a dictionary, described in the table below.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`name` | Required | string | Name of the setting.
`default` | Required | mixed | Default value of the setting.
`exclude` | Optional | boolean | If `true`, the setting is not used to define the simulation. Default value is `false`.
`pattern` | Optional | string | Replace `setting_pattern` for this setting only.

### Settings fixes

Fixes are functions applied to the values of the settings when parsed by the manager. For example, it can be useful when values are automatically generated and we want `0.0` to be treated as the same as `0`. The `fixes` list is the list of fixers to apply, in the order they must be applied. Each item of this list can be either a string (the name of the fixer), or a list containing the name of the fixer and then the arguments to pass to it, if allowed. Default fixers are listed in the table below.

Fixer | Arguments | Description
----- | --------- | -----------
`intFloats` | None | Applied to floats. Cast them to integers if it is what they are.
`round` | `n_digits` | Applied to floats. Round them with `n_digits` digits.

## Using the Simulations Manager

The addition, deletion and extraction of one or more simulations are all based on a list of dictionaries representing them. By default, a simulation uses all global settings and required sets of settings with their default values. The dictionary representing the simulation you want should define its own values for these settings.

This dictionary admits as keys all available global settings. Then, you have to add a `settings` key, valued as a list containing all the sets of settings you want to define. Each item if this list is a dictionay with two keys: `set` to define the name of the settings set you are defining, and `settings` to define the settings. The `settings` key is filled with a dictionary with keys corresponding to the settings you define and values the values of these settings.

## Using the Simulations Generator

Scripts to create simulations can be generated with a system of skeletons. A skeleton is a script where the generator will put the command lines or other informations used to create the simulations, directy by the execution of the scripts, or by using a job scheduler (on a shared supercomputer for example).

There are two types of skeletons: "subgroups" skeletons, and "wholegroup" skeletons. The set of simulations to generate is split into subgroups. For each subgroup, all the subgroups skeletons are called. Then, the wholegroup skeletons are called.

The generator is called with a "recipe", a dictionary with keys described in the table below.

Key | Required | Type | Description
--- | -------- | ---- | -----------
`max_simulations` | Optional | integer | The set of simulations is split according to this number: each subgroup contains at most `max_simulations` simulations. Default is `0`: only one subgroup is generated, containing all simulations.
`make_executable` | Required | boolean | If `true`, the generated scripts will receive the permission to be executed.
`subgroups_skeletons` | Required | list | List of skeletons to call for each subgroup, in the order they should be called.
`wholegroup_skeletons` | Required | list | List of skeletons to call for the whole group, after the subgroups.
`launch` | Required | string | Used by the maker to detect the script to launch to create the simulations with the generated scripts.
`jobs_output_filename` | Required | string | Name of the file where the output of the jobs is written.
`jobs_states_filename` | Required | string | Name of the file to use to read/write the jobs states. Optional if you use the mails to get these states.
`data_lists` | Optional | dictionary | Lists to pass to the generator.
`data_variables` | Optional | dictionary | Variables to pass to the generator.
`data_variables_cases` | Optional | dictionary | Special variables to pass to the generator, with values based on values of other variables.

## Using the Simulations Maker

The maker is probably the most used component. It uses all the other components to extract/generate/add simulations without effort.

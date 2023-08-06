# Modular Message Bot
This is a bot that runs in a container and schedules taking input from sources and pushing them to other places.

## Notes:
It's probably really easy to push things that are not escaped correctly, so be careful! At this point the code is not
very well documented, so it is a good idea to read the source anyway!

## Run Detail (Job Config)
The run details config is read from YAML. Have a look in `tests/component-resources` for examples. By default, we load
no jobs. All the methods below can be used (i.e. it will combine them)

### Run Detail Methods
1. A base64 encoded config (e.g. ENV). Set RUN_DETAILS_B64 to the appropriate value
   For example (`cat config/jobs.yml | base64 -w0`)
2. A Single file. This uses the config `RUN_DETAILS_FILE` to specify it
3. A directory containing files with extension `.yaml` or `.yml`. This directory is specified with the config
   RUN_DETAILS_FILE

### Scheduling
Scheduling is done via a cron like syntax and is handled by [APScheduler]: https://apscheduler.readthedocs.io/en/stable/
Each job can have zero or more schedules.
Note: The day of the week is not the same as Linux, so it is recommended to instead use MON, FRI, MON-THR etc

## Global Config (ENVs)

| Key | Required | Description |
|---|---|---|
| SCHEDULER_TIMEZONE | No | The timezone to use. The default is 'utc'. See http://pytz.sourceforge.net/. Note: This is also used for datetime zone default |
| RUN_DETAILS_B64 | No | A base64 encoded job YAML definition. E.g. `base64 config/jobs.yml` |
| RUN_DETAILS_FILE | No | Location of the job YAML file |
| RUN_DETAILS_DIR | No | A directory we will look for all yml or yaml files and load jobs from |

## Config and Interpolation
The config comes from envs as well as secret files. It should be easy to extend though.
You can use config to replace parts of your jobs file as well (note: it is case-sensitive!)
| Name | Type | Notes |
|---|---|---|
| Runtime substitution | `${CONFIG_NAME}` | Only runs once on application start but is very flexible |
| Dynamic substitution | `$[CONFIG_NAME]` | Only works in module parameters but is loaded everytime |

## Job strings
Job strings are messages you want to interpolate with inputs and then pass to output modules.
Each input has a code that is replaced inside the job string. For example `var: datehere` in an input module, would
replace `{datehere}` in any job string.
Each job string has a code and that code is then interpolated into the output parameters.
E.g.
```yaml
strings:
  my_message: "This is a test message"
```
Would replace `{my_message}` in any output parameter for that job

# Modules
Currently, we just have input modules and output modules. Each module is typically a wrapper around something like an
API. Please read the license for each module before using it. You are responsible for each module you use!
Each input module uses interpolation to inject a "var" into a string which is then interpolated into output parameters.

See each individual module groups README file (`README-modules-*.md`) for more details


## Extensions (advanced)
Feature Maturity Status: Alpha
If you fork this repo and want to customise the application, you can create a file called "extensions.py". In it you can
create functions to overwrite parts of the application.
Note: Please be really careful when using these and doing updates

### run_init_extension - Customise configuration and logging
You can overwrite the modular_message_bot/utils/run_utils.run_init by adding an extension function called
"run_init_extension". This function by default sets up loads envs (dotenv), sets config and logging.
Have a look at the existing function for details and what it exactly does

Example:
```python
import logging
from modular_message_bot.config.config_collection import DictConfigProvider
from modular_message_bot.config.config_collection import ConfigCollection


def run_init_extension():
   logging.basicConfig(level="DEBUG")
   config = {
      "A": "b",
      "c": 3
   }
   config_collection = ConfigCollection()
   config_collection.add_provider(DictConfigProvider(config, "config", 1))
   return config_collection
```

## Healthchecks (readiness and liveness)
Feature Maturity Status: Alpha
Since this job is CLI, we do not have HTTP healthchecks instead we write files to disk depending on config (i.e. ENV)
See: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/


Example:
```shell
HEALTHCHECK_LIVENESS_FILE=/tmp/liveness
HEALTHCHECK_READINESS_FILE=/tmp/readiness
```

```yaml
livenessProbe:
   initialDelaySeconds: 30
   periodSeconds: 55
   exec:
      command:
      - cat
      - /tmp/liveness
readinessProbe:
   initialDelaySeconds: 30
   periodSeconds: 5
   exec:
      command:
      - cat
      - /tmp/readiness
```

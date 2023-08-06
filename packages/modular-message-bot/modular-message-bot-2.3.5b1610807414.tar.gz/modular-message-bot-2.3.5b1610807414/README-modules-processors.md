# Processors
Processors make decisions before outputs run

## Specifics

### Regex Match All Abort
If all matches do not match, abort the job

```yaml
- code: regex_match_all_abort
  parameters:
     match:
        weather_edi: clouds
        weather_gla: clouds
```


### Regex Match All Continue
Only continue if all matches exist

```yaml
- code: regex_match_all_continue
  parameters:
     match:
        weather_edi: sun
        weather_gla: sun
```

### Regex Match One Abort
Abort job if we match one of the regexes

```yaml
- code: regex_match_one_abort
  parameters:
     match:
        weather_edi: clouds
        weather_gla: clouds
```


### Regex Match One Continue
Continue if one of the following matches

```yaml
- code: regex_match_one_continue
  parameters:
     match:
        weather_edi: sun
        weather_gla: sun
```

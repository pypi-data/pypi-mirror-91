# SettingsFile
### Autoload and autoupdate your configuration with native implementation
<br>

## Installation
```shell
$ pip install settingsfile
```

## Quickstart
```python
from settingsfile import Settings

settings = Settings('config.json')

# use settings object instance as a dict
settings['language'] = 'fr'

# however, you can use it via class attributes too with caution
settings.language = 'fr'

print(settings['language'])  # 'fr'
print(settings.language)  # 'fr'
```

While using the module via class attributes, there are some names that are reserved and cannot be used as they would conflict. Hence, avoid using commonplace names via attributes such as **path, json, name.** Of course, you can use these names in peace via dict-like assignment.
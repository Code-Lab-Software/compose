def merge_settings(settings, *imports):
    for settings_name in imports:
        module = __import__(settings_name, globals(), locals(), [settings_name.split('.')[-1]], -1)
        settings_attrs = tuple((attr for attr in dir(module) if attr.isupper()))
        settings.update(dict((attr_name, getattr(module, attr_name)) for attr_name in settings_attrs))


def load_settings_attrs(settings, settings_attrs, settings_name):
    module = __import__(settings_name, globals(), locals(), [settings_name.split('.')[-1]], -1)
    module_settings_attrs = tuple((attr for attr in dir(module) if attr.isupper()))
    settings.update(dict((attr_name, getattr(module, attr_name)) for attr_name in settings_attrs if attr_name in module_settings_attrs))



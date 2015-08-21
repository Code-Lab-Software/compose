def merge_settings(settings, *imports):
    for settings_name in imports:
        module = __import__(settings_name, globals(), locals(), [settings_name.split('.')[-1]], -1)
        settings_attrs = tuple((attr for attr in dir(module) if attr.isupper()))
        settings.update(dict((attr_name, getattr(module, attr_name)) for attr_name in settings_attrs))

merge_settings(globals(), *('{{ deployment_name }}.conf.global_settings', '{{ deployment_name }}.conf.sitesettings'))




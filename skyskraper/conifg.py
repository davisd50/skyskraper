from sparc.config.yaml.documents import SparcYamlConfigContainers
default_config = {
    'SkyGolf':
        {'identity':
            {'username': '',
             'password': ''
             },
         'urls':
            {'authentication': 'https://www.skygolf.com/signin.aspx',
             'skytrack_sessions': 'http://clubsg.skygolf.com/skytrak/davisd50'
             },
         'export':
            {'format': 'csv',
             'file': ''
             }
         },
    'Selenium':
        {'webdriver': 'PhantomJS',
         'timeout': '10'
         },
    'Logging':
        {'root':
            {'level': 'WARNING'}
         }
    }


def get_runtime_config(runtime_args):
    config = default_config.copy()
    if runtime_args.config:
        config.update(SparcYamlConfigContainers().first(runtime_args.config))
    if runtime_args.format:
        config['SkyGolf']['export']['format'] = runtime_args.format
    if runtime_args.file:
        config['SkyGolf']['export']['file'] = runtime_args.file
    if runtime_args.username:
        config['SkyGolf']['identity']['username'] = runtime_args.username
    if runtime_args.password:
        config['SkyGolf']['identity']['password'] = runtime_args.password
    if runtime_args.driver:
        config['Selenium']['webdriver'] = runtime_args.driver
    if runtime_args.verbose:
        config['Logging']['root']['level'] = 'INFO'
    if runtime_args.debug:
        config['Logging']['root']['level'] = 'DEBUG'
    return config
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Add sections and options to the config file
config.add_section('root')
config.set('root', 'ssh_password', '1234')
config.add_section('Output for templates')

config.set('Output for templates', 'Path', 'output/' )

with open('config.ini', 'w') as configfile:
    config.write(configfile)
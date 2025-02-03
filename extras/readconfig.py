import configparser

config = configparser.ConfigParser()

# Read the config file
config.read('config.cnf')

password = config.get('root', 'ssh_password')
output = config.get('output_cfg_files', 'path')

# Use the config values

print(password,output)
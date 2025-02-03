
from jinja2 import Environment, FileSystemLoader, Template

# file_loader = FileSystemLoader('user.html.jinja.html')
env = Environment(loader=FileSystemLoader(''))
template = env.get_template('host.jinja')

host_name = ''
ip = ''
disk =[]
data = {
    'host_name': host_name,
    'ip': ip
    }

rendered = template.render(data =data, data2 =disk)

output_file_path = 'host'+ ip + '.cfg'
with open(output_file_path, 'w') as file:
    file.write(rendered)


#
# # Define a template string
# template_string = "Hello, {{ name }}!"
#
# # Create a Jinja Template object
# template = Template(template_string)
#
# # Render the template with data
# rendered = template.render(name="Alice")
#
# # Print the rendered output
# print(rendered)


# from jinja2 import Environment, FileSystemLoader
#
# # Set up the Jinja environment and load the template file
# env = Environment(loader=FileSystemLoader('path/to/template/directory'))
# template = env.get_template('template.txt')
#
# # Prepare the data for the template

#
# # Render the template with the provided data
# rendered = template.render(data)
#
# # Specify the output file path and write the rendered content to the file
# output_file_path = 'path/to/output/file.txt'
# with open(output_file_path, 'w') as file:
#     file.write(rendered)

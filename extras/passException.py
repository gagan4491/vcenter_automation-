
pass_exception ={}

with open("../passwordException.txt", "r") as lines:
    next(lines)
    for line in lines:
        key, value = line.strip().split()
        pass_exception[key] = value
print(pass_exception)


test_ip = '192.168.4.90'
if test_ip in pass_exception:
    print('yes')
    print(pass_exception[test_ip])
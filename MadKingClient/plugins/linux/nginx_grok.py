import re

f = open('access.log','r',encoding='utf-8')
nginx_list = []
error_log = []

# for line in f.readlines():
#     nginx_compile = '''(?P<remote_addr>[\d\.]{7,}) - - (?:\[(?P<datetime>[^\[\]]+)\]) "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?:[^"]+)" "(?P<user_agent>[^"]+)"'''
#     regex = re.compile(nginx_compile)
#     matcher = regex.match(line)
#     try:
#         nginx_list.append(matcher.groupdict())
#     except AttributeError as e:
#         error_log.append(e)
#     print(nginx_list)

for line in f.readlines():
    nginx_list.append(line)
print(len(nginx_list))
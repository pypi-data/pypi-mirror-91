import re


def format(plain):
    clearplain = re.sub('^\s*[Cc]ookie\s*[:：]', '', plain).strip()
    clearplain = re.sub('\s*;\s*$', '', clearplain) + ";"
    dic = {}
    for i in re.finditer("(?P<Key>.+?)=(?P<Value>.+?);", clearplain):
        dic[i.group('Key').strip()] = i.group('Value').strip()
    return dic

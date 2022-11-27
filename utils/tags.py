import re

SPLIT_SYMBOLS = r'[ -.]'
REMOVE_PATTERN = r'^[\W\d]|[\W\d]$'


def tag_elements(tag: str) -> list:
    '''
    Разделяет очищенный тэг на составляющие.
    '''
    tag = re.sub(string=tag, repl='', pattern=REMOVE_PATTERN)

    return [elm for elm in re.split(string=tag, pattern=SPLIT_SYMBOLS) if len(elm) > 2]

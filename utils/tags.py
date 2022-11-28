import re

remove_pattern = r'[^a-zа-я. -]'
split_pattern = r'[- .]'
min_tag_lenght = 3


def tag_elements(tag: str) -> list:
    '''Разделяет очищенный тэг на составляющие.'''
    
    return [tag for tag in re.split(split_pattern, re.sub(remove_pattern, '', tag)) if len(tag) >= min_tag_lenght]


if __name__ == '__main__':
    pass

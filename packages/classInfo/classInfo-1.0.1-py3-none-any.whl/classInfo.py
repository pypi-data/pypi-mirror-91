"""
classInfo

Module that can help you writing information about something
"""

def information(**info):
    """
    Create a new information
    return all information into dict
    """
    information = {}
    for about, value in info.items():
        information[str(about)] = value
    return information

def read_info(info):
    data = []
    for about, value in info.items():
        data.append(f'{about}: {value}')
    return '\n'.join(data)
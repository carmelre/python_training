FILE_METADATA_DEFAULT_MAPPING = {
    'properties': {
        'size': {'type': 'integer'},
        'mode': {'type': 'integer'},
        'uid': {'type': 'integer'},
        'gid': {'type': 'integer'},
        'path': {'fields': {'keyword': {'type': 'keyword'}},
                 'norms': False,
                 'type': 'text'},
        'file_name': {'fields': {'keyword': {'type': 'keyword'}},
                      'norms': False,
                      'type': 'text'},
        'access time': {'type': 'date', 'format': 'yyyy-mm-dd hh-mm-ss'},
        'modification time': {'type': 'date', 'format': 'yyyy-MM-dd HH:mm:ss'},
        'change time': {'type': 'date', 'format': 'yyyy-MM-dd HH:mm:ss'}
    }
}

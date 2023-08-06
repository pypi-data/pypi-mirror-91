

class MtlsException(Exception):
    """
    """
    error_msg = ''

class FileSystemException(MtlsException):
    pass

class FileNotExistsException(FileSystemException):
    """
    """
    error_msg = ''

    def __init__(self,file_path:str):
        """
        """
        self.error_msg = f"file '{file_path}' not exists."









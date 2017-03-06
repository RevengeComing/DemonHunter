

class FileLogger:

    def __init__(self, file_path):
        self.file_path = file_path
    
    def log(self, data):
        string = ' '.join(["%s=%s" % (key, value) for key, value in data.items()])
        string += '\r\n'
        self.write(string)

    # TODO: make write function async <<<
    def write(self, string):
        """ Not async :(( """
        with open(self.file_path, "a") as logfile:
            logfile.write(string)
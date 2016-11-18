
class TorrentParser():
    
    general_info = {}
    file_info = {}

    def __init__(file_name = None):
        if file_name == None:
            return
        else:
            self._parse_torrent()
    
    def open_file(self, file_name):

        #TODO Make sure the file actually exists

        self._file_name = file_name

        self._parse_torrent()

    def _parse_torrent(self):

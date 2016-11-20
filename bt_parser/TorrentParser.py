
import time
from StringIO import StringIO

class TorrentParser():
    """
    Object that is used to parse torrent files

    Can be initialized with bit torrent file name, or passed to open_file

    """
    def __init__(self, file_name=None):

        if file_name is None:
            return
        else:
            self.open_file(file_name)

    def open_file(self, file_name):

        self._file_name = file_name
        # read out the initial 'd' char
        with open(self._file_name, 'rb') as file:
            self._raw_text = StringIO(file.read()).getvalue()

        self._parse_torrent()

    def _parse_torrent(self):

        # remove the initial d
        char = self._pop_raw_string(1)
        if char == 'd':
            self._info_dict = self._decode_dict()

        print self._info_dict

    def _pop_raw_string(self, n=1):
        popped_string = self._raw_text[:n]
        self._raw_text = self._raw_text[n:]
        return popped_string

    def _read_next_item(self):
        size_char = ''
        val = None

        while len(self._raw_text) > 0:
            char = self._pop_raw_string()
            if len(self._raw_text) == 0:
                return None
            if char == 'd':
                return self._decode_dict()
            
            if char == 'i':
               return self._decode_integer()
            if char == 'e':
                return 'e'
            
            if char == 'l':
                return self._decode_list()
            elif char == ':':
                    break
            
            else:
                size_char += char
        if size_char == '':
            return None
        return self._pop_raw_string(int(size_char))
    
    def _decode_integer(self):
        val_char = ''
        while len(self._raw_text) > 0:
            char = self._pop_raw_string()
            if char == 'e':
                return val_char
            else:
                val_char += char
    
    def _decode_dict(self):
        original_dict = {}
        while len(self._raw_text) > 0:
            
            key = self._read_next_item()

            # reached end of file, or end of dict
            if key == None or key == 'e':
                return original_dict

            val = self._read_next_item()

            original_dict[key] = val

        return original_dict

    def _decode_list(self):
        original_list = []
        while len(self._raw_text) > 0:
            
            item = self._read_next_item()

            # reached end of file, or end of dict
            if item == None or item == 'e':
                return original_list

            if item == 'd':
                original_list.append(self._decode_dict())
                continue

            original_list.append(item)
        return original_list
            
    
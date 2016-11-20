
from StringIO import StringIO

class TorrentParser(object):
    """
    Object that is used to parse torrent files

    Can be initialized with bit torrent file name, or passed to open_file
    This class uses protocols defined by the Bittorrent Protocol Specification v1.0 
    (https://wiki.theory.org/BitTorrentSpecification)

    """
    _info_dict = {}
    _raw_binary = []

    def __init__(self, file_name=None):

        if file_name is None:
            return
        else:
            self.open_file(file_name)

    def open_file(self, file_name):
        """
        Open a bit torrent file, and parse the contents

        :param file_name: string containing the file name, note this should include the directory
        :type cmd: str
        :returns: None
        """
        self._file_name = file_name
        # read out the initial 'd' char
        with open(self._file_name, 'rb') as torrent_file:
            self._raw_binary = StringIO(torrent_file.read()).getvalue()

        self._parse_torrent()
        print self._info_dict

    def _parse_torrent(self):

        # remove the initial dictionary indicatory, and begin parsing info as dictionary
        char = self._pop_raw_string(1)
        if char == 'd':
            self._info_dict = self._decode_dict()

    def _pop_raw_string(self, num_pop=1):
        
        # retrieve the value of the required string
        popped_string = self._raw_binary[:num_pop]

        # pop the string from the raw data
        self._raw_binary = self._raw_binary[num_pop:]
        return popped_string

    def _read_next_item(self):

        # string used to hold the size of the next item
        size_char = ''

        while len(self._raw_binary) > 0:
            char = self._pop_raw_string()

            # return none if we reached end of file
            if len(self._raw_binary) == 0:
                return None

            # begin parsing dict, if next item is a dict
            if char == 'd':
                return self._decode_dict()

            # begin parsing int, if next item is an int
            if char == 'i':
                return self._decode_integer()

            # return e to indicate an end to the current item being parsed
            if char == 'e':
                return 'e'
            # begin parsing list
            if char == 'l':
                return self._decode_list()

            # colon indicates the current item has ended
            elif char == ':':
                break

            else:
                size_char += char
        if size_char == '':
            return None
        # return the item, if the item was a string
        return self._pop_raw_string(int(size_char))

    def _decode_integer(self):
        val_char = ''
        # keep reading values
        while len(self._raw_binary) > 0:
            char = self._pop_raw_string()

            # if e is reached, integer has ended, return the integer value
            if char == 'e':
                return int(val_char)
            else:
                val_char += char

    def _decode_dict(self):
        original_dict = {}
        while len(self._raw_binary) > 0:

            key = self._read_next_item()

            # reached end of dict
            if key is None or key == 'e':
                return original_dict

            val = self._read_next_item()

            #TODO: REMOVE BEFORE RELEASE
            if key == 'pieces':
                original_dict[key] = 2
            else:
                original_dict[key] = val

        return original_dict

    def _decode_list(self):
        original_list = []
        while len(self._raw_binary) > 0:

            item = self._read_next_item()

            # reached end of file, or end of dict
            if item is None or item == 'e':
                return original_list

            if item == 'd':
                original_list.append(self._decode_dict())
                continue

            original_list.append(item)
        return original_list

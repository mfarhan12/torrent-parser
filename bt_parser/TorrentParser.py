
from datetime import datetime
from StringIO import StringIO

# constants set by the Bittorent Protocol Specificationss v1.0
INT_BEGIN = 'i'
DICT_BEGIN = 'd'
LIST_BEGIN = 'l'
ITEM_END = 'e'
SIZE_END = ':'
class NoFileException(Exception):
    """
    Class used as an exception to be  raised when an error occurs
    """
    pass


class TorrentParser(object):
    """
    Object that is used to parse torrent files

    Can be initialized with bit torrent file name, or passed to open_file.
    This class uses protocols defined by the Bittorrent Protocol Specification v1.0
    (https://wiki.theory.org/BitTorrentSpecification)

    """
    _info_dict = {}
    _raw_binary = []
    _file_name = None
    def __init__(self, file_name=None):
        """
        TOrrentParser Constructer


        :param file_name (optional): string containing the file name.
        note this should include the directory
        :type cmd: str
        :returns: None
        """
        if file_name is None:
            return
        else:
            self.open_file(file_name)

    def open_file(self, file_name):
        """
        Open a bit torrent file, and parse the contents

        Note: the file_name should include the current directory
        :param file_name: string containing the file name, note this should include the directory
        :type cmd: str
        :returns: None
        """

        # read out the initial 'd' char
        try:
            with open(file_name, 'rb') as torrent_file:
                self._raw_binary = StringIO(torrent_file.read()).getvalue()
        except IOError:
            raise NoFileException(
                "Cannot open file, make sure to include directory in file name")
        self._parse_torrent()
        self._file_name = file_name


    def get_url(self):
        """
        Return the url of the current bit torrent file

        :returns: URL string
        """
        # if no file is open, or info dict has not been parsed
        if self._file_name is None or self._info_dict == {}:
            raise NoFileException(
                "No file given, use the open_file method to open a torrent file.")
        return self._info_dict['announce']

    def get_creation_date(self):
        """
        Return the creation date of the current bit torrent file
        Note the creation date is optional, and if the creation date is not available in the
        torrent file, None will be returned

        :returns: datetime object containing the time of the created file
        """
        # if no file is open, or info dict has not been parsed
        if self._file_name is None:
            raise NoFileException(
                "No file given, use the open_file method to open a torrent file.")

        if 'creation date' not in self._info_dict:
            return None

        unix_time = self._info_dict['creation date']
        return datetime.utcfromtimestamp(unix_time)

    def get_creator_name(self):
        """
        Return the name of torrent file's creater
        Note created by field is optional, and if not available torrent file,
        None will be returned
        :returns: string containing the creator's name, or None if no name is in file
        """
        # if no file is open, or info dict has not been parsed
        if self._file_name is None:
            raise NoFileException(
                "No file given, use the open_file method to open a torrent file.")

        if 'created by' not in self._info_dict:
            return None

        return self._info_dict['created by']

    def get_files(self):
        """
        Returns a dictionary where the key is the name of the file, and the value is
        a dict containing the files parameters
        file_dict = {'file1': {'size':x,
                              'checksum': y}

                     'file2': {'size':x,
                                'checksum': y}
                     ...

                     'fileN': {'size':x,
                                'checksum': y}

                    }
        Note that the checksum is optional, so it will have a value of None if Not Implemented
        Note the size is in Bytes
        :returns: dict containing the file, and their corresponding attributes
        """
        # if no file is open, or info dict has not been parsed
        if self._file_name is None:
            raise NoFileException(
                "No file given, use the open_file method to open a torrent file.")
        files_dict = {}
        raw_files_dict = self._info_dict['info']
  
        # read if multiple files
        if 'files' in raw_files_dict:
            for f in raw_files_dict['files']:

                file_size = f['length']

                # combine the file name with directory if the file is in a directory
                file_name = '/'.join(f['path'])

                # check for md5sum, note other files may have md5, but for now we will
                # folllow the standard set by Bittorrent Protocol Specification v1.0.0
                if 'md5sum' in f:
                    check_sum = f['md5sum']

                # some files have md5 listed, instead of md5sum
                elif 'md5' in f:
  
                    check_sum = f['md5']
                else:
                    check_sum = None
                # add file name to dict
                files_dict[file_name] = {'size': file_size,
                                         'checksum': check_sum}

        # if the torrent only has 1 file, retrieve data for 1 file
        else:
            file_size = raw_files_dict['length']

            file_name = raw_files_dict['name']

            # md5sum is an optional paramater
            if 'md5sum' in raw_files_dict:
                check_sum = raw_files_dict['md5sum']

            # some files have md5 listed, instead of md5sum
            elif 'md5' in raw_files_dict:
                check_sum = raw_files_dict['md5']

            else:
                check_sum = None
        files_dict[file_name] = {'size': file_size,
                                 'checksum': check_sum}
        return files_dict

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
            if len(self._raw_binary) == 0 or char == '':
                return None

            # begin parsing dict, if next item is a dict
            if char == DICT_BEGIN:
                return self._decode_dict()

            # begin parsing int, if next item is an int
            if char == INT_BEGIN:
                return self._decode_integer()

            # return e to indicate an end to the current item being parsed
            if char == ITEM_END:
                return ITEM_END
            # begin parsing list
            if char == LIST_BEGIN:
                return self._decode_list()

            # colon indicates the current item has ended
            elif char == SIZE_END:
                break

            else:
                size_char += char

        # return the item, if the item was a string
        return self._pop_raw_string(int(size_char))

    def _decode_integer(self):
        val_char = ''
        # keep reading values
        while len(self._raw_binary) > 0:
            char = self._pop_raw_string()

            # if e is reached, integer has ended, return the integer value
            if char == ITEM_END:
                return int(val_char)
            else:
                val_char += char

    def _decode_dict(self):
        original_dict = {}
        while len(self._raw_binary) > 0:

            key = self._read_next_item()

            # reached end of dict
            if key is None or key == ITEM_END:
                return original_dict

            val = self._read_next_item()

            original_dict[key] = val

        return original_dict

    def _decode_list(self):
        original_list = []
        while len(self._raw_binary) > 0:

            item = self._read_next_item()

            # reached end of file, or end of dict
            if item is None or item == ITEM_END:
                return original_list

            original_list.append(item)
        return original_list

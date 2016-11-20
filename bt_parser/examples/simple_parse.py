
import os
from bt_parser.TorrentParser import TorrentParser

# get the current directory
cwd = os.getcwd()
torrent_name = cwd + '/dobba_graphics_archive.torrent'

# initialize torrent parser
bt_parse = TorrentParser(torrent_name)

# get URL
url_name = bt_parse.get_url()
print url_name

# get creation date
creation_date = bt_parse.get_creation_date()
print creation_date
# get creator's name'

creator_name = bt_parse.get_creator_name()
print creator_name

# get all the files in the torrent
torrent_files = bt_parse.get_files()

# print out the files in the torrent, with the corresponding key
for file_name in torrent_files:
    print file_name, torrent_files[file_name]

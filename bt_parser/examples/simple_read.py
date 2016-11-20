#pylint: skip-file
from StringIO import StringIO

#TODO: USE os.cwd to retrieve directory

file_name = '/home/mohammad/torrent-parser/bt_parser/examples/sample.torrent'
from bt_parser.TorrentParser import TorrentParser 


bt_parse = TorrentParser(file_name)

print bt_parse.get_files()


#pylint: skip-file
from StringIO import StringIO

file_name = '/home/mohammad/torrent-parser/bt_parser/examples/Elephants Dream (avi) (1024x576).torrent'
file_name2 = '/home/mohammad/torrent-parser/bt_parser/examples/Honest Man- The Life of R. Budd Dwyer (720p).torrent'
file_name3 = '/home/mohammad/torrent-parser/bt_parser/examples/sample.torrent'
from bt_parser.TorrentParser import TorrentParser 


bt_parse = TorrentParser(file_name3)

# bt_parse = TorrentParser(file_name)

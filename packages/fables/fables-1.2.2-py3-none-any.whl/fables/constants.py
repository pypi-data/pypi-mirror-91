"""
Constants that are used around the fables src tree and that are exposed to
the user.
"""


# These may get put into the zip file when compressed using finder on OSX.
OS_PATTERNS_TO_SKIP = [".DS_STORE", ".DS_Store", "__MACOSX"]

# Throw a ValueError when files of size > 1 GB are passed in.
# The user can reset this var after importing fables, e.g.
"""
>>> import fables
>>> fables.MAX_FILE_SIZE = 4 * 1024 ** 3  # 4 GB
>>> fables.detect('a_really_big_csv.csv')
"""
MAX_FILE_SIZE = 1024 ** 3  # bytes -> 1 GB

# Number of bytes used to determine a mimetype from an io-stream. 30k was
# found to accurately set mimetypes as a result of fables tests. User can
# reset this var the same as MAX_FILE_SIZE.
NUM_BYTES_FOR_MIMETYPE_DETECTION = 30000

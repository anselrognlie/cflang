from cflang.io.file_binary_reader import FileBinaryReader, EndOfFileBinaryReader

r = FileBinaryReader('sample_data/cfsm/bin/sum_to_5')
try:
    while True:
        i = r.read_dword()
        print(i)
except EndOfFileBinaryReader:
    pass

print("Done.")

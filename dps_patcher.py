import os
import sys
from shutil import copyfile

REPLACE_FINISHED = "ffffffff"


def apply_patch(patch_file, dest_file):
    with open(patch_file, "rb") as patch_file_stream:
        # Ignore first 6 bytes maybe should verify but /shrugs
        bytes_string = patch_file_stream.read(6)
        write_new = False
        while True:
            # Next Address to write to if still replacing, otherwise append to end
            if not write_new:
                bytes_string = patch_file_stream.read(4).hex()
            if not bytes_string:
                break

            if bytes_string == REPLACE_FINISHED and not write_new:
                write_new = True
                bytes_string = patch_file_stream.read(4).hex()
            num_bytes = int.from_bytes(patch_file_stream.read(2), byteorder='big')
            new_bytes = patch_file_stream.read(num_bytes)
            if num_bytes == 0:
                break
            if not write_new:
                with open(dest_file, "r+b") as dest_file_stream:
                    dest_file_stream.seek(int(bytes_string, 16))
                    # print(f"{dest_file_stream.tell()}: Overwrote {num_bytes} Bytes")
                    dest_file_stream.write(new_bytes)
            else:
                with open(dest_file, "a+b") as dest_file_stream:
                    # print(f"{dest_file_stream.tell()}: Added {num_bytes} New Bytes")
                    dest_file_stream.write(new_bytes)


def main():
    src_file, patch_file, dest_file = None, None, None

    if len(sys.argv) > 1:
        src_file = sys.argv[1]
    if len(sys.argv) > 2:
        patch_file = sys.argv[2]
    if len(sys.argv) > 3:
        dest_file = sys.argv[3]
    if len(sys.argv) > 4:
        print("ERROR: Usage 'python dps_patcher <src> <patch> <dest>'")

    if src_file is None:
        src_file = input("Enter Source ROM Path: ")
    if patch_file is None:
        patch_file = input("Enter DPS File Path: ")
    if dest_file is None:
        dest_file = input("Enter Destination ROM Path: ")

    src_file = src_file if os.path.isabs(src_file) else os.path.abspath(src_file)
    patch_file = patch_file if os.path.isabs(patch_file) else os.path.abspath(patch_file)
    dest_file = dest_file if os.path.isabs(dest_file) else os.path.abspath(dest_file)

    copyfile(src_file, dest_file)
    apply_patch(patch_file, dest_file)


main()

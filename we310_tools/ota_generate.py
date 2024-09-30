#!/usr/bin/python3

import sys, os, struct

header_num = struct.pack('<I', 0x01)
ota_sig = struct.pack('<4s', b'OTA1')
header_len = struct.pack('<I', 0x18)
offset_addr = struct.pack('<I', 0x20)
value_reserved = struct.pack('<I', 0xFFFFFFFF)

def ota_generate(bin_path, fw_ver, dest_path):
    if os.path.exists(dest_path) == True:
        os.remove(dest_path)

    ota_path = dest_path;
    ota_all = open(ota_path, 'ab')
    firmware_ver = struct.pack('<I', int(fw_ver, base = 16))
    ota_all.write(firmware_ver)
    ota_all.write(header_num)
    ota_all.write(ota_sig)
    ota_all.write(header_len)
    
    bin_file = open(bin_path, 'rb')
    data = bin_file.read()

    bin_size = os.path.getsize(bin_path)
    bin_file = open(bin_path, 'rb')
    data = bin_file.read()
    ota_checksum = 0
    for i in range(bin_size):
        ota_checksum += ord(data[i])
        if ota_checksum > 0xFFFFFFFF:
            ota_checksum = ota_checksum & 0xFFFFFFFF
    bin_file.close()
    ota_all.write(struct.pack('<I', ota_checksum))

    ota_size = struct.pack('<I', bin_size)
    ota_all.write(ota_size)
    ota_all.write(offset_addr)
    ota_all.write(value_reserved)
    ota_all.write(data)
    ota_all.close()
    print('ota generate success')

if __name__ == '__main__':
    if len(sys.argv) == 4:
        print sys.argv[3]
        ota_generate(sys.argv[1], sys.argv[2], sys.argv[3])

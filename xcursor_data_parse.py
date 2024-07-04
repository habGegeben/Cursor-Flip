import re
import sys
import struct

"""
Files you'll most likely need this run on:

- circle
- copy
- dnd-ask
- dnd-copy
- dnd-link
- dnd-move
- dnd_no_drop
- grabbing
- hand1
- hand2
- left_ptr
- left_ptr_watch
- link
- pencil
- pointer-move
- right_ptr
- zoom-in
- zoom-out

!! Do not forget to update:
 - Folder name of the theme
 - cursor.theme file
 - index.theme file
!! 
!! Otherwise, you risk the theme reverting and referencing the old cursors.
"""

def error_handling(error_code):
    if error_code == 1:
        print('! Parsing Error')
        print('Not a valid xcursor file. The first 4 bytes are not "Xcur".')
    if error_code == 2:
        print('! Parsing Error')
        print('Invalid Table of Contents entry. Does not match Image or Comment.')
    if error_code == 3:
        print('! Data Size Error')
        print('The expected size of the Table of Contents does not equal the size of the data given.')

def toc_parsing(toc_data, toc_size):
    print('=== Parsing Table of Contents')
    if toc_size != len(toc_data):
        error_handling(3)
        quit
    toc_counter = 0
    toc_dict = {}
    for x in range(0, toc_size, 12):
        #toc_counter += 1
        toc_type = toc_data[x:x+4]
        if toc_type == b'\x02\x00\xfd\xff':
            toc_type = 'Image'
        elif toc_type == b'\x01\x00\xfd\xff':
            toc_type = 'Comment'
        else:
            error_handling(2)
            exit
        ##print('Type:', toc_type)
        toc_dict[toc_counter] = [toc_type]
        toc_subtype, = struct.unpack('i', toc_data[x+4:x+8])
        #print('Size (bytes):', toc_subtype)
        toc_dict[toc_counter].append(toc_subtype)
        toc_pos, = struct.unpack('i', toc_data[x+8:x+12])
        #print('Position in file:', hex(toc_pos))
        toc_dict[toc_counter].append(hex(toc_pos))
        toc_counter += 1
    print('')
    print('=== Done')
    return(toc_dict)
    #print('Table of Contents size:', toc_counter)

def chunk_parsing(toc_table, file_data, thefhandle):
    for chunk in toc_table:
        print('Chunk ===', chunk)
        chunk_pos = int(toc_table[chunk][2], 16)
        chunk_header_size, = struct.unpack('i', file_data[chunk_pos:chunk_pos + 4])
        chunk_header = file_data[chunk_pos:chunk_pos+chunk_header_size]
        #print(chunk_header)
        # We would need to verify the chunk type here with something akin to:
        #if chunk_header[4:8] != b'\x02\x00\xfd\xff'
        chunk_size, = struct.unpack('i', chunk_header[8:12])
        #print('\tNominal Size:', chunk_size)
        chunk_version, = struct.unpack('i', chunk_header[12:16])
        #print('\tVersion:', chunk_version)
        chunk_width, = struct.unpack('i', chunk_header[16:20])
        print('\tWidth:', chunk_width)
        chunk_height, = struct.unpack('i', chunk_header[20:24])
        #print('\tHeight:', chunk_height)
        chunk_xhot, = struct.unpack('i', chunk_header[24:28])
        print('\tX Hotspot:', chunk_xhot)
        new_xhot = chunk_width - chunk_xhot
        chunk_yhot, = struct.unpack('i', chunk_header[28:32])
        if new_xhot != chunk_xhot:
            print('\tWriting new X Hotspot of', new_xhot)
            packed_xhot = struct.pack('i', new_xhot)
            thefhandle.seek(chunk_pos+24)
            thefhandle.write(packed_xhot)
        #print('\tY Hotspot:', chunk_yhot)
        chunk_delay, = struct.unpack('i', chunk_header[32:36])
        #print('\tFrame Delay  (milliseconds):', chunk_delay)
        #print('\tImage pixels:', file_data[chunk_pos+36:chunk_pos+((chunk_width*chunk_height)*4)])
        flipped_img = xflip(file_data[chunk_pos+36:chunk_pos+((chunk_width*chunk_height)*4)], chunk_width)
        thefhandle.seek(chunk_pos+36)
        thefhandle.write(flipped_img)
        print('')

def xflip(pixel_array, img_width):
    """ Perfom horizontal rotation of pixels """

    print('\tFlipping Image...')

    # Create transform array that each pixel will shift by.
    transform_array = []
    img_width += 1 #in order for the first value to be correct and use -2 for every iteration, gotta add one.
    for x in range(0, img_width - 1):
        transform_array.append(img_width - 2)
        img_width -= 2

    #print(transform_array)
    
    # Move image pixels to bytearray, so we can edit values via item assignment
    pixel_array = bytearray(pixel_array)

    # Rearrange pixel_array in the order designated by transform_array.
    # Iterating over pixel_array will be in 4 byte increments as we are moving 4-byte pixels.
    for x in range(0, len(pixel_array), 4):
        transform_val = transform_array[int(x/4) % len(transform_array)]
        #print(transform_val)
        if transform_val > 0:
            swap_pixel = pixel_array[x:x + 4]
            pixel_array[x:x + 4] = pixel_array[x + (transform_val * 4):(x + (transform_val * 4)) + 4]
            pixel_array[x + (transform_val * 4):(x + (transform_val * 4)) + 4] = swap_pixel
        else:
            pass
    
    # Convert our flipped image to bytes so it can be written.
    #pixel_array = bytes(pixel_array)
    return(pixel_array)

def parse_file(data, the_fhandle):
    if data[0:4] != b'Xcur':
        error_handling(1)
        quit
    file_header, = struct.unpack('i', data[4:8])
    print('Bytes in header:', file_header)
    file_version, = struct.unpack('i', data[8:12])
    print('File version:', file_version)
    ntoc, = struct.unpack('i', data[12:16])
    print('Number of toc entries:', ntoc)
    toc_byte_size = (ntoc * 12)
    pos_after_toc = toc_byte_size + 16
    toc_table = toc_parsing(data[16:pos_after_toc], toc_byte_size)
    chunk_parsing(toc_table, data, the_fhandle)

def main():
    cursor_file = sys.argv[1]
    with open(cursor_file, 'rb+') as file_handle:
        file_data = file_handle.read()
        parse_file(file_data, file_handle)

if __name__ == '__main__':
    main()
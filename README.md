# Cursor-Flip
Convert right-handed X11 cursors to left-handed (or vice-versa, I guess). 
Also seconds as a xcursor parser.

!! This code is "I just wanted it to work" level. There are so many poor coding practices in it.

: I got tired of finding so many great X11 mouse cursor themes out there that aren't left-handed (not anyone's fault).   
: I got bored of having to use GIMP to flip the xcursor files, and then having to edit the X-hotspots.   
: I wasn't bored enough to just point this at a folder or compressed file and have it do _everything_, so...

### Files you'll most likely need to run this on within the `cursors` directory:

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

!! **Do not forget to update**:
 - Folder name of the theme
 - cursor.theme file
 - index.theme file

!! Otherwise, you risk the theme reverting and referencing the old cursors.

## Parser

This is as basic (read: lazy) as a parser can get, but will provide the following data if you wish to enable them by removing the comments:

- Table of Contents
- - Bytes in header
  - File version
  - Number of entries
  - Chunk Types (comment or image)
  - Absolute Chunk address
- Chunk data
- - Chunk Header
  - Size
  - Version
  - Width
  - Height
  - X-hotspot
  - Y-hotspot
  - Frame Delay in milliseconds (if animated)
  - Pixel bytes

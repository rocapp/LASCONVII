#!/bin/bash
# Usage: ./vid_cmd.sh 'path/to/images/image.png' output_file_name.mp4
cat $1 | ffmpeg -f image2pipe -i - -framerate 1/5 -c:v libx264 -vf "fps=15,format=yuv420p,scale=trunc(iw/2)*2:trunc(ih/2)*2" $2.mp4 

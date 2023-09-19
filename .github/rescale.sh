#!/bin/bash
MAXSIZE=1024
if [ $# -ne 2 ]; then
  echo "Usage: $0 input_image output_path"
  exit 1
fi

input_image="$1"
output_path="$2"

if [ ! -f "$input_image" ]; then
  echo "Input image file does not exist."
  exit 1
fi

# Get the dimensions of the input image
width=$(identify -format "%w" "$input_image")
height=$(identify -format "%h" "$input_image")

# Determine the size of the largest square that fits within the image
if [ "$width" -gt "$height" ]; then
  size="$height"
else
  size="$width"
fi

# Ensure the output size is no larger than 1024px
if [ "$size" -gt $MAXSIZE ]; then
  size=$MAXSIZE
fi

# Create a temporary file for the intermediate image
tmpfile=$(mktemp "${TMPDIR:-/tmp}/tempimage.XXXXXXXXXX")

if [[ -f "$output_path.webp" ]]; then
  rm "$output_path.webp"
fi


# Trim the image to fit within a 1024x1024 square, maintaining the aspect ratio
convert "$input_image" -auto-orient  -resize "${size}x${size}"^ -gravity center -extent ${size}x${size} "$tmpfile"
cwebp -q 90 "$tmpfile" -o "$output_path.webp"

# Clean up the temporary file
rm "$tmpfile"

echo "Image trimmed and saved as $output_path.webp"

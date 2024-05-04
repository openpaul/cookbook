#!/bin/bash

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick could not be found. Please install it to use this script."
    exit 1
fi

# Check if input image file is provided
if [ -z "$1" ]; then
    echo "Please provide an input image file as the first argument."
    exit 1
fi

# Check if output path is provided
if [ -z "$2" ]; then
    echo "Please provide an output path as the second argument."
    exit 1
fi

# Input image file (e.g., icon.png)
input_image="$1"

# Output path
output_path="$2"

# Check if the input file exists
if [ ! -f "$input_image" ]; then
    echo "Input image file '$input_image' does not exist."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$output_path"

# List of target icon sizes for PNG
icon_sizes=(72 96 128 144 152 167 180 192 384 512)

# List of target icon sizes for favicon (ico)
favicon_sizes=(16 32 48 64)

# Resize the input image to each target size and save to the output path
for size in "${icon_sizes[@]}"; do
    output_image="$output_path/icon-${size}.png"
    convert "$input_image" -resize "${size}x${size}" "$output_image"
    echo "Resized $input_image to $output_image"
done

# Create favicon.ico with multiple sizes
favicon_output="$output_path/favicon.ico"
convert "$input_image" -resize "16x16" "$output_path/tmp-16.png"
convert "$input_image" -resize "32x32" "$output_path/tmp-32.png"
convert "$input_image" -resize "48x48" "$output_path/tmp-48.png"
convert "$input_image" -resize "64x64" "$output_path/tmp-64.png"

# Combine the resized images into favicon.ico
convert "$output_path/tmp-16.png" "$output_path/tmp-32.png" "$output_path/tmp-48.png" "$output_path/tmp-64.png" "$favicon_output"

# Remove temporary files
rm "$output_path/tmp-16.png" "$output_path/tmp-32.png" "$output_path/tmp-48.png" "$output_path/tmp-64.png"

echo "Favicon created at '$favicon_output' and all icons resized and saved in the specified output path: '$output_path'."

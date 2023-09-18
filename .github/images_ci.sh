#!/bin/bash

# Check for the correct number of arguments
if [ $# -ne 2 ]; then
  echo "Usage: $0 folder_path rescale_script_path"
  exit 1
fi

# Get the folder path and rescale script path from the arguments
folder_path="$1"
rescale_script_path="$2"

# Use find to search for .cook, .jpg, and .jpeg files and process them
find "$folder_path" -type f -name "*.cook" | while read -r cook_file; do
  # Check if the file is a .cook file
  echo "$cook_file"
  base_name="${cook_file%.*}"

  # Determine the image suffix based on the existence of corresponding files
  if [ -f "$base_name.jpg" ]; then
    image_suffix=".jpg"
  elif [ -f "$base_name.png" ]; then
    image_suffix=".png"
  elif [ -f "$base_name.jpeg" ]; then
    image_suffix=".jpeg"
  else
    continue  # Skip this .cook file if no corresponding image files are found
  fi

  # Check if there is no .webp file with the same name
  if [ ! -f "$base_name.webp" ]; then
    # Call the rescale.sh script with the required arguments
    "$rescale_script_path" "${base_name}${image_suffix}" "$base_name"
    echo "Rescaled: $cook_file -> $base_name.webp"
  fi
done

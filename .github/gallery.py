import os
import argparse


def card(md, image):
    link = md.rsplit('.',1)[0]
    title = os.path.basename(link).title()
    return f"""<a href="../{link}" class="card-link">
  <div class="card">
    <div class="card-image">
      <img src="../{image}" onerror="this.src='/default.webp'" alt="{title}">
    </div>
    <div class="card-content">
      <h3 class="card-title">{title}</h3>
    </div>
  </div>
</a>"""

def find_markdown_files(root_dir):
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                p = os.path.join(root, file)
                markdown_files.append(p)

    return markdown_files

def group_markdown_files_by_folder(markdown_files):
    grouped_files = {}
    for file_path in markdown_files:
        parts = file_path.split(os.sep, 3)
        current_group = grouped_files
        for part in parts:
            current_group = current_group.setdefault(part, {})
    return grouped_files

def loop_recursivly(data, prefix="", depth=0):
    md_keys = sorted([key for key in data.keys() if key.endswith(".md") and len(data[key]) == 0])
    dict_keys = sorted(list(set(data.keys()) - set(md_keys)))
    sorted_keys = md_keys + dict_keys
    for i, key in enumerate(sorted_keys):
        value = data[key]

        if isinstance(value, dict) and not key.endswith(".md"):
            if depth > 0 or i > 0:
                print('</div>\n\n')
            print(f"\n\n{'#'*(depth+2)} {key.title()}")

            print('<div class="my-card-grid">')
            loop_recursivly(value, prefix = os.path.join(prefix, key), depth = depth + 1)
        else:
            image_link = os.path.join(prefix, key.replace(".md", ".webp"))
            md = os.path.join(prefix, key)
            c = card(md, image=image_link)
            print(c)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Group Markdown files in a folder hierarchy and output to a Markdown file.")
    parser.add_argument("input_folder", help="Path to the input folder containing Markdown files.")
    parser.add_argument("output_file", help="Path to the output Markdown file.")
    args = parser.parse_args()

    input_folder = args.input_folder
    output_file = args.output_file

    markdown_files = find_markdown_files(input_folder)

    grouped_data = group_markdown_files_by_folder(markdown_files)
    grouped_data = grouped_data.get(input_folder)

    # hacky but well remvoes all top level mds
    ignore = [x for x in grouped_data.keys() if x.endswith(".md")]
    for k in ignore:
        if k in grouped_data.keys():
            del grouped_data[k]
    
    loop_recursivly(grouped_data)

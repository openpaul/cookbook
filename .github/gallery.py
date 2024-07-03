import os
import argparse
from typing import List
import os
from typing import Dict, List, Union

from numpy import deprecate_with_doc
from regex import R
from pydantic import BaseModel

import os
from typing import Dict, List, Union

DEFAULT_IMAGE = "default.webp"


def card(md: str, image: str) -> str:
    link = md.rsplit(".", 1)[0]
    title = os.path.basename(link).title()
    return f"""<a href="../{link}" class="card-link">
  <div class="card">
    <div class="card-image">
      <img src="../{image}"  alt="{title}">
    </div>
    <div class="card-content">
      <h3 class="card-title">{title}</h3>
    </div>
  </div>
</a>"""


class Recipe(BaseModel):
    cook: str

    @property
    def name(self):
        return os.path.basename(self.cook).replace(".cook", "")

    @property
    def image(self):
        path = self.cook.replace(".cook", ".webp")
        if os.path.exists(path):
            # remove first segment of path
            return path.split("/", 1)[1]
        else:
            return DEFAULT_IMAGE

    @property
    def md(self):
        md = self.cook.replace(".cook", ".md")
        # remove first segment of path
        return md.split("/", 1)[1]

    @property
    def card(self):
        return card(self.md, self.image)

    def __str__(self):
        return f"Recipe: {self.name}"


class RecipeFolder(BaseModel):
    path: str
    recipes: List[Recipe]
    subfolders: List["RecipeFolder"]
    depth: int

    @property
    def name(self):
        return os.path.basename(self.path).title()

    def __hash__(self):
        return hash(self.path)

    def __str__(self):
        s = f"Folder: {self.name}\n"
        s += f"Recipes: {len(self.recipes)}\n"
        s += f"Subfolders: {len(self.subfolders)}\n"
        for r in self.recipes:
            s += f"  {r}\n"
        for f in self.subfolders:
            s += f"  {f}\n"

        return s

    def gallery(self):
        # ensure subfolders are sorted by name
        self.subfolders.sort(key=lambda f: f.name)
        # now in addition we sort the recipes by name
        self.recipes.sort(key=lambda r: r.name)

        # ensure key folders are sorted by this list
        key_folders = ["Mains"]
        self.subfolders.sort(key=lambda f: key_folders.index(f.name) if f.name in key_folders else len(key_folders))
        
        gallery_md = ""
        if self.depth > 1:
            gallery_md += f"\n\n{'#'* (self.depth+2)} {self.name}"
            gallery_md += '\n<div class="my-card-grid">'
            for r in self.recipes:
                gallery_md += "\n\n"
                gallery_md += r.card
            gallery_md += "\n</div>\n\n"
        
       
        for f in self.subfolders:
            gallery_md += f.gallery()
        
        return gallery_md

def find_recipes(root_dir: str, suffix: str = ".cook") -> List[Recipe]:
    suffix_files: List[str] = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(suffix):
                p = os.path.join(root, file)
                suffix_files.append(Recipe(cook=p))

    return suffix_files

def create_recipe_folder(path: str, max_depth: int = 3) -> RecipeFolder:
    def search_directory(current_dir: str, current_depth: int):
        result = RecipeFolder(path=current_dir, recipes=[], subfolders=[], depth=current_depth)

        if current_depth > max_depth:
            result.recipes = find_recipes(current_dir)
            return result
        else:
            for entry in os.listdir(current_dir):
                path = os.path.join(current_dir, entry)
                if os.path.isdir(path):
                    result.subfolders.append(search_directory(path, current_depth + 1))
                elif entry.endswith(".cook"):
                    result.recipes.append(Recipe(cook=path))

        return result

    return search_directory(path, 1)


md = create_recipe_folder("cook", 2).gallery()
print(md)
exit()

def find_files_with_suffix(
    root_dir: str, suffix: str = ".cook", max_depth: int = 3
) -> Dict[str, Union[Dict[str, Union[Dict, List[str]]], List[str]]]:
    def search_directory(current_dir: str, current_depth: int):
        result = {}

        if current_depth > max_depth:
            return find_recipes(current_dir, suffix)
        else:
            for entry in os.listdir(current_dir):
                path = os.path.join(current_dir, entry)
                if os.path.isdir(path):
                    result[RecipeFolder(path=path)] = search_directory(
                        path, current_depth + 1
                    )
                elif entry.endswith(suffix):
                    if "files" not in result:
                        result["files"] = []
                    result["files"].append(Recipe(cook=path))

        return result

    return search_directory(root_dir, 1)


# Example usage:
# files_dict = find_files_with_suffix('/path/to/root', '.txt', 2)


def group_markdown_files_by_folder(markdown_files):
    grouped_files = {}
    for file_path in markdown_files:
        parts = file_path.split(os.sep, 3)
        current_group = grouped_files
        for part in parts:
            current_group = current_group.setdefault(part, {})
    return grouped_files


def loop_recursivly(data, prefix="", depth=0):
    md_keys = sorted(
        [key for key in data.keys() if key.endswith(".md") and len(data[key]) == 0]
    )
    dict_keys = sorted(list(set(data.keys()) - set(md_keys)))
    sorted_keys = md_keys + dict_keys

    exit()
    for i, key in enumerate(sorted_keys):
        value = data[key]

        if isinstance(value, dict) and not key.endswith(".md"):
            if depth > 0 or i > 0:
                print("</div>\n\n")
            print(f"\n\n{'#'*(depth+2)} {key.title()}")

            print('<div class="my-card-grid">')
            loop_recursivly(value, prefix=os.path.join(prefix, key), depth=depth + 1)
        else:
            image_link = os.path.join(prefix, key.replace(".md", ".webp"))
            md = os.path.join(prefix, key)
            c = card(md, image=image_link)
            print(c)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Group Markdown files in a folder hierarchy and output to a Markdown file."
    )
    parser.add_argument(
        "input_folder", help="Path to the input folder containing Markdown files."
    )
    parser.add_argument("cook_folder", help="Path to the cook folder")
    parser.add_argument("output_file", help="Path to the output Markdown file.")
    parser.add_argument(
        "--depth", "-d", default=3, help="Depth of the folder hierarchy"
    )
    args = parser.parse_args()

    cook_files = find_files_with_suffix(args.cook_folder, ".cook", args.depth)

    print(cook_files)
    exit()
    # hacky but well removes all top level mds
    ignore = [x for x in grouped_data.keys() if x.endswith(".md")]
    for k in ignore:
        if k in grouped_data.keys():
            del grouped_data[k]

    loop_recursivly(grouped_data)

import os
import argparse
from typing import List
import os
from typing import  List

from pydantic import BaseModel

import os
from typing import List

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
        self.subfolders.sort(
            key=lambda f: key_folders.index(f.name)
            if f.name in key_folders
            else len(key_folders)
        )

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
        result = RecipeFolder(
            path=current_dir, recipes=[], subfolders=[], depth=current_depth
        )

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Group Markdown files in a folder hierarchy and output to a Markdown file."
    )
    parser.add_argument(
        "input", help="Path to the input folder containing Markdown files."
    )
    parser.add_argument(
        "--depth", "-d", default=3, help="Depth of the folder hierarchy"
    )
    args = parser.parse_args()
    md = create_recipe_folder(args.input, args.depth).gallery()
    print(md)

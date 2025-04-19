git restore docs/index.md
uv venv  --python 3.12
source .venv/bin/activate 
uv pip install mkdocs\
            'mkdocs-material>=9.5.12' \
            mkdocs-minify-plugin \
            ../pycook
# convert images
bash .github/images_ci.sh cook .github/rescale.sh


# compile icons
#bash .github/resize_icons.sh icon.png docs/icons/

# convert md
pycook -i cook/ -o docs/
rsync -av --ignore-existing --include "*/" --include="*.webp"  --exclude="*" cook/ docs/
python .github/gallery.py cook >> docs/index.md
mkdocs build -c
rsync -za --delete site $USER@ginger:/var/www/recipes/
mkdocs serve
git restore docs
rm -rf site
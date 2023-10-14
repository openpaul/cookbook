#sudo apt install hugo
pyenv activate 
pip install mkdocs\
            mkdocs-material \
            mkdocs-minify-plugin 

# convert images
bash .github/images_ci.sh cook .github/rescale.sh

# convert md
pycook -i cook/ -o docs/
rsync -av --ignore-existing --include "*/" --include="*.webp"  --exclude="*" cook/ docs/
python .github/gallery.py docs abc >> docs/index.md
mkdocs build -c
mkdocs serve
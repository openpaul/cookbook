# Cookbook

Simple recipe collection of home-cooking meals. 
Look around and find something delicious.

## Prepare images for uploading
Its in the CI code base but not a CI to save space and only upload webp images:

Run locally:
```sh
pyenv activate cookbook
bash .github/images_ci.sh cook .github/rescale.sh
```

## Spell check

```sh
fdfind  --type file .cook$ . -x echo "aspell check '{}'"
```
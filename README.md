# Cookbook

## Prepare iamges for uploading
Its in the CI code base but not a CI to save space and only upload webp images:

Run locally:
```sh
pyenv activate cookbook
bash .github/images_ci.sh cook .github/rescale.sh
```
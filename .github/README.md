How to Update
=============

1. Update nlopt submodule
   ```shell
   git submodule update --remote
   # if there are changes
   git add extern/
   git commit -m "Update nlopt submodule"
   ```
2. `[Optional]` If there is a need, update the `ci/nlopt_manylinux2014_x64_64.Dockerfile` image. This is used to build the linux images
   1. This should be done in `image/*` branch as the github action `manylinux-image.yml` will automatically update the image in dockerhub on push.
3. Update `.github/workflows/build.yaml` if necessary

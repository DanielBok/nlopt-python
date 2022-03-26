How to Update
=============

1. Update nlopt submodule
   ```shell
   git submodule update --remote
   # if there are changes
   git add extern/
   git commit -m "Update nlopt submodule"
   ```
2. `[Optional]` If there is a need, update the `ci/nlopt_manylinux2014_x64_64.Dockerfile` image. This is used to build
   the linux images
    * This should be done in `image/*` branch as the github action `manylinux-image.yml` will automatically update the
      image in dockerhub on push.
3. Update `.github/workflows/build.yaml` if necessary
4. There are already tests in the github workflows to test that `pip install nlopt` works. But none to test the module specifically
   1. Spin up a docker image and run the sample code
   2. ```shell
      docker container run -it --rm --entrypoint bash python:3.10-slim-buster
      pip install nlopt
      apt-get update
      apt-get install curl -y
      curl https://raw.githubusercontent.com/DanielBok/nlopt-python/master/test_scripts/sample_test_script.py --output test.py
      python test.py
      ```

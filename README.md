Reuseable supporting Python3 module for image analysis and *vision tracking*
on our robots. Game-specific features (for particular FRC years) will not live
in this project, as this library will be shared each year. This project uses
the [opencv](https://docs.opencv.org/3.4.0/d6/d00/tutorial_py_root.html) library.

We expect that most Python scripts in this package to be both *stand-alone* (run
it directly from the command line) as well as a *module* where the functions can
be called by code in other projects.


Learning Vision Tracking
========================

Along with the official [OpenCV tutorials](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html),
we have found the following useful:

  * [Video Tutorials](https://pythonprogramming.net/loading-video-python-opencv-tutorial/)
  * [OpenCV Computer Vision with Python](https://www.packtpub.com/application-development/opencv-computer-vision-python)
  * [OpenCV with Python by Example](https://www.packtpub.com/application-development/opencv-python-example)
  * [OpenCV: Computer Vision Projects](https://www.packtpub.com/application-development/opencv-computer-vision-projects-python)


Using the Project
=================

As a reusable project, this repository would be a dependency to other game-specific projects.

**Note:** Eventually, we should flesh this section out with details on how to include
this project as a dependency for other projects, but for the moment, we'll gloss over
that feature.


We are using `pipenv` to set up a correct shell, so enter:

    pipenv shell      # To make a subshell with access to Python version 3
    pipenv install    # To download all dependencies (should be automatic)

You will need to make sure that your system is functional by running the following
`support` programs:

  * `support/has_library.py` makes sure you have the OpenCV library installed

  * `support/has_camera --channel 1` makes sure you have a USB camera properly
           connected and readable. Give `--help` to explain the options.


Developing the Project
======================

As a developer of this project, make sure you follow our global policies including
this workflow. First, create a branch with _your initials_`/`_feature_`-`_issue_,
for instance:

    git checkout -b fa/coloring-42 master

Then make all the changes you want, making sure that all the tests pass:

    make all

While creating unit tests for code that depends on OpenCV, cameras and images, may
be a challenge, we should at least test what we can, and learn more about mocking the
OpenCV library.

The final step is a commit and push. Make sure your commit includes a reference to
the Issue number associated with the change. For example:

    git commit
    git push origin fa/coloring-42

Hop on Github, following [these instructions](https://yangsu.github.io/pull-request-tutorial/).

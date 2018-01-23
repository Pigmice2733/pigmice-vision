Reuseable supporting Python3 module for image analysis and *vision tracking* on
our robots. Game-specific features (for particular FRC years) will not live in
this project, as this library will be shared each year. This project uses the
[opencv](https://docs.opencv.org/3.4.0/d6/d00/tutorial_py_root.html) library.

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

As a reusable project, this repository would be a dependency to other
game-specific projects.

**Note:** Eventually, we should flesh this section out with details on how to
include this project as a dependency for other projects, but for the moment,
we'll gloss over that feature.


We are using `pipenv` to set up a correct shell, so enter:

    pipenv shell      # To make a subshell with access to Python version 3
    pipenv install    # To download all dependencies (should be automatic)

You will need to make sure that your system is functional by running the following
programs in the `support` directory (cd into support):

  * `has_library.py` makes sure you have the OpenCV library installed

  * `has_camera --channel 1` makes sure you have a USB camera properly
           connected and readable. Give `--help` to explain the options.


Calibrating Cameras
-------------------

Cameras can have small distortions in the lens that may be unnoticeable under
typical scenarios, but could adversely affect the precision of our
code...besides, correcting for abnormalities is a great initial project in
OpenCV.

First, print a checkerboard pattern, run the following program in the `support`
directory:

    verify_checkerboard.py --channel 1 --rows 8 --columns 8

Where the `--channel` option specifies the USB channel of your camera. `0` is
typically the built-in canera on most laptops, so `1` may be a good choice. Make
sure the `--rows` and `--columns` are correct for your pattern (as it doesn't
*have* to be a standard 8x8 board). Hold the pattern in front of your camera,
and if all goes well, the corners for each board will have a colored circle.
This means, you can use this pattern for calibration.

To calibrate your camera, run the following program from the `tools` directory:

    tools/camera_calibrator.py --channel 0 --rows 8 --columns 8

Again, adjust the options to match your computer system and checkerboard
pattern. Follow the instructions printed on the screen, and when you press `s`,
you will have a file containing the calibration data. The other programs will
call the `lib.calibration()` function with the name of this file, in order to
`undistort` the camera, e.g.

    mtx, dist, newcammtx = calibration('calibration-values.npz')
    newimage = cv2.undistort(img, mtx, dist, None, newcammtx)


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

# Complex-Fourier
An implementation of [Fourier Transform](https://en.wikipedia.org/wiki/Fourier_transform) on any svg file

The Idea for this project came together after watching [a video by 3blue1brown](https://www.youtube.com/watch?v=r6sGWTCMz2k) about the fourier transform.
This project is an implementation of the demos shown in this video, using nothing but the information featured on it.

# Features
the code can generate a set of circles to draw any vector path (stored as an SVG file).
Built into the project are some example svgs to play around with.

CONTROLS - 
<br> Mouse - Movement and zoom
<br> E - Toggle focus on the moving dot
<br> Q - Toggle circle highlights
<br> G - Toggle gaming mode
<br> N - Open up a new SVG file.
<br> Arrows - Increase / Decrease Animation speed

# Demo
https://user-images.githubusercontent.com/54374032/174783846-e55b32d8-00b2-427b-8c8a-471fd417063e.mp4


# Running The Project
In order to run the program, you could either go to the latest build on github and run the attached exe file or download the code directly.
<br> the code is dependent on the <b>numpy</b>, <b>pygame</b> and <b>svgpathtools</b> libraries.
<br>To install them: run `pip install numpy`, `pip install pygame`, `pip install svgpathtools` on your local terminal.
<br> If done correctly you can now run the `main.py` file directly (with the `svg` folder in the same directory) and play the simulation!

# cairo_visualization_wheel

**cairo_visualization_wheel** is a Python script that uses matplotlib to create visualization wheels as seen in [Alberto Cairo's book](http://www.thefunctionalart.com/2012/09/download-three-chapters-of-functional.html) (see Figure 3.2).

## Author
[Dent Earl](https://github.com/dentearl/)

## Dependencies
* Python 2.7
* [matplotlib](http://matplotlib.sourceforge.net/) 1.1.0

## Installation
1. Download the package.
2. <code>cd</code> into the directory.
3. Type <code>make</code>.

## Input file format
The input file may contain comment lines (lines that start with #). The file must contain at least six lines that consist of a decimal number between 0.0 and 1.0 (inclusive).

## Usage
    usage: cairo_visualization_wheel input_file

    positional arguments:
      metrics_file          path to metrics file.

    optional arguments:
      -h, --help            show this help message and exit
      --out OUT             basename and path of output image. default=cairo_wheel
      --out_format OUT_FORMAT
                            output format, may be all, pdf, eps or png. default=eps
      --width WIDTH         Width of the image in inches. default=5.000000
      --height HEIGHT       Height of the image in inches. default=4.000000
      --dpi DPI             DPI for png output. default=300


## Examples
    bin/cairo_visualization_wheel example/metrics.txt --outFormat png --out img/example.png
![Example image](https://github.com/dentearl/cairo_visualization_wheel/raw/master/img/example.png)
=======
cairo_visualization_wheel
=========================

#!/usr/bin/env python
"""
cairo_visualization_wheel
4 October 2013
Dent Earl (dentearl@gmail.com)

A Python script that draws Visualization Wheels in the style of Alberto Cairo,
as seen in "the functional art: an introduction to information graphics and
visualization" by Alberto Cairo, 2013 New Riders, Berkeley, CA, USA.

"""
##############################
# Copyright (C) 2013 by
# Dent Earl (dearl@soe.ucsc.edu, dent.earl@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##############################
# plotting boilerplate
import matplotlib
matplotlib.use('Agg')
# pdf.fonttype : Output Type 3 (Type3) or Type 42 (TrueType)
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.backends.backend_pdf as pltBack
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy
##############################
from argparse import ArgumentParser
import os
import sys

class BadInput(Exception):
  pass

def InitArguments(parser):
  parser.add_argument('metrics_file', type=str,
                      help='path to metrics file.')
  parser.add_argument(
    '--out', type=str, default='cairo_wheel',
    help='basename and path of output image. default=%(default)s')
  parser.add_argument(
    '--out_format', type=str, default='eps',
    help='output format, may be all, pdf, eps or png. default=%(default)s')
  parser.add_argument(
    '--width', type=float, default=5.,
    help='Width of the image in inches. default=%(default)f')
  parser.add_argument(
    '--height', type=float, default=4.,
    help='Height of the image in inches. default=%(default)f')
  parser.add_argument(
    '--dpi', type=int, default=300,
    help='DPI for png output. default=%(default)d')


def CheckArguments(args, parser):
  if args.metrics_file is None:
    parser.error('Specify a path to a metrics_file to read')
  if args.out_format not in ('all', 'eps', 'pdf', 'png'):
    parser.error('Unknown --format type, %s' % args.format)
  if args.dpi < 72:
    parser.error('DPI setting --dpi %d is too low. Must be > 72.' % args.dpi)
  if args.width < 1:
    parser.error('width setting --width %d is too low. Must be >= 1.'
                 % args.width)
  if args.height < 1:
    parser.error('height setting --height %d is too low. Must be >= 1.'
                 % args.height)
  extension = args.out.split('.')[-1]
  if extension in ('all', 'eps', 'pdf', 'png'):
    # if supplied, remove the extension since we append it at the end
    args.out, extension = os.path.splitext(args.out)


def InitImage(args):
  """Initialize a new image.

  Args:
    args: an argparse arguments object

  Returns:
    fig: a matplotlib figure object
    pdf: a matplotlib pdf drawing (backend) object
  """
  pdf = None
  if args.out_format == 'pdf' or args.out_format == 'all':
    pdf = pltBack.PdfPages(args.out + '.pdf')
  fig = plt.figure(figsize=(args.width, args.height),
                   dpi=args.dpi, facecolor='w')
  return fig, pdf


def EstablishAxis(fig, args):
  """Create a single axis on the figure object

  Args:
    fig: a matplotlib figure object
    args: an argparse arguments object

  Returns:
    ax: a matplotlib axis object
  """
  args.ax_left = 0.1
  args.ax_width = 0.8
  args.ax_bottom = 0.1
  args.ax_height = 0.8
  ax = fig.add_axes([args.ax_left, args.ax_bottom,
                     args.ax_width, args.ax_height], polar=True)
  plt.box(on=False)
  return ax


def WriteImage(fig, pdf, args):
  """Write the image to disk.

  Args:
    fig: a matplotlib figure object
    pdf: a matplotlib pdf drawing (backend) object
    args: an argparse arguments object
  """
  if args.out_format == 'pdf':
    fig.savefig(pdf, format = 'pdf')
    pdf.close()
  elif args.out_format == 'png':
    fig.savefig(args.out + '.png', format='png', dpi=args.dpi)
  elif args.out_format == 'all':
    fig.savefig(pdf, format='pdf')
    pdf.close()
    fig.savefig(args.out + '.png', format='png', dpi=args.dpi)
    fig.savefig(args.out + '.eps', format='eps')
  elif args.out_format == 'eps':
    fig.savefig(args.out + '.eps', format='eps')


def DrawAxis(ax, args):
  """Draw the axis that we will then plot data upon.

  Args:
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  ax.grid(False)
  thetas = []
  angles = []
  angle_labels = ['Abstraction', 'Figuration',
                  'Functionality', 'Decoration',
                  'Density', 'Lightness',
                  'Multidimensionality', 'Unidimensionality',
                  'Originality', 'Familiarity',
                  'Novelty', 'Redundancy']
  for i in xrange(0, 6):
    offset_theta = numpy.pi / 12.0
    offset_angle = 180 / 12.0
    delta_theta = i * numpy.pi / 6.0
    delta_angle = i * 180 / 6.0
    angles.append(180 - offset_angle - delta_angle)
    angles.append(360 - offset_angle - delta_angle)
    thetas.append(numpy.pi - offset_theta - delta_theta)
    thetas.append(2 * numpy.pi - offset_theta - delta_theta)
    ax.add_line(
      lines.Line2D(
        [2 * numpy.pi - offset_theta - delta_theta,
         numpy.pi - offset_theta - delta_theta],
        [1.0, 1.0],
        color='grey',
        linewidth=.75,
      ))
  ax.plot(thetas, 12 * [1.0], markeredgecolor='grey', marker='o',
          markerfacecolor='grey', linestyle='none')
  # ax.set_title("Cairo Visualization Wheel", va='bottom')
  ax.set_rmax(1.15)
  ax.set_yticklabels([])
  ax.set_thetagrids(angles, labels=angle_labels, fontsize=8.0)


def ReadData(args):
  """Read the metrics file and validate the data.

  Args:
    args: an argparse arguments object

  Returns:
    data: a list of six floats in [0.0, 1.0]
  """
  data = []
  f = open(args.metrics_file, mode='r')
  for line_number, line in enumerate(f, 1):
    line = line.strip()
    if line.startswith('#'):
      continue
    try:
      d = float(line)
    except ValueError:
      sys.stderr.write('Bad value on line %d, %s' % (line_number, line))
      raise
    if 0.0 <= d <= 1.0:
      data.append(d)
    else:
      raise BadInput('Value out of range on line %d, %f not in [0.0, 1.0]'
                     % (line_number, d))
  if len(data) != 6:
    raise BadInput('Wrong number of values in %s! Expected 6 but saw %d'
                   % (args.metrics_file, len(data)))
  return data


def CleanData(data, args):
  """Read the data and convert it into a form we can plot directly

  Args:
    data: a list of six floats in [0.0, 1.0]
    args: an argparse arguments object

  Returns:
    plot_data: a numpy array, twelve by 2, one column floats in [0.0, 1.0]
      and one column floats in [0.0, 2 pi]
  """
  plot_data = numpy.empty([12, 2], dtype=float, order='C')
  for i, d in enumerate(data, 0):
    offset_theta = numpy.pi / 12.0
    delta_theta = i * numpy.pi / 6.0
    plot_data[i, 0] = numpy.pi - offset_theta - delta_theta
    plot_data[i, 1] = d
    plot_data[i + 6, 0] = 2 * numpy.pi - offset_theta - delta_theta
    plot_data[i + 6, 1] = 1.0 - d
  return plot_data


def DrawData(data, ax, args):
  """Draw the data on the axis as a single transparent polygon.

  Args:
    data: a numpy array twelve by 2 of floats in [0.0, 1.0]
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  ax.add_patch(patches.Polygon(data, alpha=0.5,
                               color='#1f77b4'))


def main():
  usage = ('%(prog)s metrics_file')
  parser = ArgumentParser(usage=usage)
  InitArguments(parser)
  args = parser.parse_args()
  CheckArguments(args, parser)

  figure, pdf = InitImage(args)
  ax = EstablishAxis(figure, args)
  DrawAxis(ax, args)
  data = ReadData(args)
  data = CleanData(data, args)
  DrawData(data, ax, args)
  WriteImage(figure, pdf, args)


if __name__ == '__main__':
  main()

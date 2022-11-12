"""Writes an SVG of a proposed flag of Berkeley to standard output.

See https://github.com/nanaze/berkeleyflag/
"""

import math
import string

_HEADER = """\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg>
<svg  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="-1.5 -1 3 2">
"""

_STYLES = """\
.flag-background {
  fill: #003262;
}

.star {
  fill: $copper_green;
}

.star-dark {
  fill: $dark_copper_green;
}
"""

_FOOTER = """\
</svg>
"""

_COPPER_GREEN_RGB = (185, 211, 182)
_DARK_COPPER_GREEN_RGB = tuple(v * 0.8 for v in _COPPER_GREEN_RGB)

def _GetPathString(points):
    path_string = 'M %f, %f ' % points[0]
    for point in points[1:]:
        path_string += 'L %f,%f ' % point
    path_string += 'Z'
    return path_string

def _GetRgbString(rgb):
    return 'rgb(%d,%d,%d)' % rgb

def main():
    print (_HEADER)
    print ('<style>')

    styles = string.Template(_STYLES).substitute(
        {'copper_green': _GetRgbString(_COPPER_GREEN_RGB),
         'dark_copper_green': _GetRgbString(_DARK_COPPER_GREEN_RGB)})
    print(styles)
    print ('</style>')

    print ('<rect x="-1.5" y="-1" width="3" height="3" class="flag-background"></rect>')

    # http://www.jdawiseman.com/papers/easymath/surds_star_inner_radius.html
    midpoint_scale = (3 - math.sqrt(5)) / 2

    points = []
    fractional_parts = 10

    angles = [(i / fractional_parts) * 2 * math.pi for i in range(fractional_parts)] # radians

    for angle in angles:
        point = (math.sin(angle), -math.cos(angle))
        points.append(point)

    star_points = []
    for i, point in enumerate(points):
        odd = i % 2 != 0
        if odd:
            point = tuple(coord * midpoint_scale for coord in point)
        star_points.append(point)

    print ('<g class="star" transform="scale(0.8) translate(0, 0.05)">')
    print ('<path d="%s"></path>' % _GetPathString(star_points))

    for i in range(0, fractional_parts, 2):
        path_str = _GetPathString([(0,0)] + star_points[i:i+2])
        print ('<g class="star-dark" transform="scale(0.90)">')
        print ('<path d="%s"></path>' % path_str)
        print ('</g>')

    print ('</g>')
    print(_FOOTER)


if __name__ == '__main__':
    main()

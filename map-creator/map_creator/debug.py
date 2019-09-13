import subprocess

template = '''
<html>
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.js"></script>
  </head>
  <body>
    <div id="map" style="width: 800px; height: 600px"></div>
    <script>
    const map = L.map('map', {{
      'center': [{center}],
      'zoom': 16,
      'layers': [
        L.tileLayer('http://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
          'attribution': 'Map data &copy; OpenStreetMap contributors'
        }})
      ]
    }});
    {polylines}
    </script>
  </body>
</html>
'''

polyline_template = 'new L.Polyline([{points}], {{color: "blue", weight: 6}}).addTo(map);'


def show_paths_in_browser(paths):
    if len(paths) == 0 or all(len(path.points) < 2 for path in paths):
        return

    polylines = []

    for path in paths:
        if len(path.points) < 2:
            continue

        center = f'{path.points[0].position.latitude}, {path.points[0].position.longitude}'
        points = ','.join([f'[{point.position.latitude}, {point.position.longitude}]'
                           for point in path.points])

        polyline = polyline_template.format(points=points)
        polylines.append(polyline)

    html = template.format(center=center, polylines='\n'.join(polylines))

    with open('debug.html', 'w') as f:
        f.write(html)

    subprocess.call(['firefox', 'debug.html'])


def show_path(f):
    def wrapper(*args, **kwargs):
        path = f(*args, **kwargs)
        show_paths_in_browser([path, ])
        return path
    return wrapper


def show_paths(f):
    def wrapper(*args, **kwargs):
        paths = f(*args, **kwargs)
        show_paths_in_browser(paths)
        return paths
    return wrapper

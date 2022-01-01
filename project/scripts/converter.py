import sys

import pyproj


class GeoConverter:
    def __init__(self):
        self.fips4203 = pyproj.Proj('+proj=lcc +lat_1=30.11666666666667 +lat_2=31.88333333333333 '
                                    '+lat_0=29.66666666666667 +lon_0=-100.3333333333333 +x_0=700000 +y_0=3000000 '
                                    '+datum=NAD83 +units=us-ft +no_defs')
        self.wgs84 = pyproj.Proj("+init=EPSG:4326")

    def convert(self, x, y) -> tuple[float, float]:
        lon, lat = pyproj.transform(self.fips4203, self.wgs84, x, y)
        return lat, lon


def convert(infile, outfile):
    converter = GeoConverter()
    count = 0
    with open(infile) as f, open(outfile, 'w') as out:
        for line in f:
            if line:
                split = line.split(',')
                x, y = split[6], split[7]
                if x and y:
                    lat, lon = converter.convert(float(x), float(y))
                else:
                    lat, lon = '', ''
                split[6] = lat
                split[7] = lon
                out.write(','.join([str(item) for item in split]))
                count += 1
                if count % 100 == 0:
                    print(count)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Invalid arguments')
    else:
        convert(sys.argv[1], sys.argv[2])

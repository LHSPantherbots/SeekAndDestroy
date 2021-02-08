RAD = 80


POINTS = {'C3': {'coordinates': (313, 320), 'radius': RAD, 'isBall': False},
          'D5': {'coordinates': (387, 272), 'radius': RAD, 'isBall': False},
          'A6': {'coordinates': (168, 247), 'radius': RAD, 'isBall': False},
          'E6': {'coordinates': (450, 257), 'radius': RAD, 'isBall': False},
          'B7': {'coordinates': (247, 237), 'radius': RAD, 'isBall': False},
          'C9': {'coordinates': (308, 206), 'radius': RAD, 'isBall': False},
          'B3': {'coordinates': (221, 325), 'radius': RAD, 'isBall': False},
          'D6': {'coordinates': (388, 260), 'radius': RAD, 'isBall': False},
          'B8': {'coordinates': (247, 224), 'radius': RAD, 'isBall': False},
          'D10': {'coordinates': (379, 191), 'radius': RAD, 'isBall': False}
        }


for point in POINTS:
    print(POINTS[point]['radius'])
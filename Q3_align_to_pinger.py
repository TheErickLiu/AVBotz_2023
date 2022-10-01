import numpy as np
import scipy
import math
import sys
import os

def signal_process(samples):
    '''normalizes pressure data to [-1, 1] and run fft.'''

    max_value = np.max(samples)
    min_value = np.min(samples)

    mid, halfrange = (max_value + min_value) / 2, (max_value - min_value) / 2  
    normalized = (samples - mid) / halfrange

    return scipy.fft.fft(normalized)


def calc_angle(p1: float, p2: float, p3: float) -> int:
    ''' Calculate angle for each case '''

    if (p1 == p2 == p3):
        raise ValueError(f"Equal phases {p1}")

    # top left upper 45 degree octant
    if p1 >= p2 >= p3:
        result = -45 * (p1 - p2) / (p1 - p3)
    # top left lower 45 degree octant
    elif p1 >= p3 >= p2:
        result = -45 - 45 * (p1 - p3) / (p1 - p2)
    # upper right 90 quadrant
    elif p2 >= p1 >= p3:
        result = 90 * (p2 - p1)/(p2 - p3)
    # bottom right upper 45 degree octant
    elif p2 >= p3 >= p1:
        result = 90 + 45 * (p2 - p3) / (p2 - p1)
    # bottom left 90 quadrant
    elif p3 >= p1 >= p2:
        result = -90 - 90 * (p3 - p1) / (p3 - p2)
    # bottom right lower 45 degree octant
    elif p3 >= p2 >= p1:
        result = 135 + 45 * (p3 - p2) / (p3 - p1)
    
    return int(result)  


def angle_to_pinger(audio_file: str) -> int:

     # Separates into 3 columns for each hydrophone
    raw = np.loadtxt(audio_file, delimiter=';')
    phases = []

    for i in range(3):

        # gets index of largest / most significant frequency signal
        fft = signal_process(raw[:, i]) 
        fft_max = np.max(abs(fft))
        index = np.argwhere(abs(fft)[:400] == fft_max)

        # puts phases of each hydrophone into list
        angle = np.angle(fft[index], deg=True)[0][0]
        angle = (angle + 360) % 360
        phases.append(angle) 

    return calc_angle(phases[0], phases[1], phases[2])


def main():
    if len(sys.argv) <= 1:
        sys.stderr.write('Error: missing input file\n')
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        sys.stderr.write('Error: input file does not exist.\n')
        sys.exit(1)

    result = angle_to_pinger(input_file)
    print(f'{result}')


if __name__ == "__main__":
    main()

import math
import sys
import os

def pixel_to_meter(p: float, scale: float) -> float:
    return (p * scale) / 1000 # pixels to mm to meters

def calc_dist(focalLength, objRealHeight, imgDimY: float, objImgHeight, sensorSize) -> float:
    ''' Distance Formula '''

    d = (focalLength*objRealHeight*imgDimY) / (objImgHeight*sensorSize)
    d = d/1000

    return d

def angle_of_points(p1: list, p2: list, dist: float) -> tuple:
    ''' inverse of dist between 2 points over dist to object, for yaw and pitch '''

    yaw_r = math.atan((p1[0] - p2[0]) / dist)
    yaw_d = math.degrees(yaw_r)

    pitch_r = math.atan((p2[1] - p1[1]) / dist)
    pitch_d = math.degrees(pitch_r)

    return yaw_d, pitch_d


def align_to_target(align_in: tuple) -> tuple:
    ''' main function to take input align_in and calculate align_out '''

    imgDimX, imgDimY, centerX, centerY, focalLength, sensorSize, objRealHeight, objImgHeight, hfov, vfov = align_in
    relativeYaw, relativePitch, dist, relativeYOffset, relativeZOffset = 0, 0, 0, 0, 0 

    # height length to pixel scale. Horizontal scale may be different.
    vertical_scale = objRealHeight/float(objImgHeight)

    # convert heights based on pixel scale 
    vfov_height = pixel_to_meter(imgDimY, vertical_scale)
    imgCenterY = vfov_height / 2
    objCenterY = pixel_to_meter(centerY, vertical_scale) 

    # calculate distance 
    dist = calc_dist(focalLength, objRealHeight, imgDimY, objImgHeight, sensorSize)

    # converts pixels to meters for widths based on hfov and dist
    hfov_width = math.tan(math.radians(hfov/2)) * dist * 2
    imgCenterX = hfov_width / 2 
    objCenterX = centerX/imgDimX * hfov_width 
    
    # difference of how off it is from middle
    relativeYOffset = objCenterX - imgCenterX
    relativeZOffset = objCenterY - imgCenterY

    # calculate yaw and pitch based on object center and img center
    relativeYaw, relativePitch = angle_of_points([objCenterX, objCenterY], [imgCenterX, imgCenterY], dist)

    return (relativeYaw, relativePitch, dist, relativeYOffset, relativeZOffset)


def read_input(inputfile: str) -> list:
    # Takes nums from input file and returns a list

    with open(inputfile, 'r') as infile:

        for line in infile:
            if line.startswith('#'):
                continue
            rec = line.strip().split(' ')
            if len(rec) < 10:
                sys.stderr('WARNING: input missing fields. SKIP\n')
                continue
            return [float(v) for v in rec]

    return None

def main():
    if len(sys.argv) <= 1:
        sys.stderr.write('Error: missing input file\n')
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        sys.stderr.write('Error: input file does not exist.\n')
        sys.exit(1)

    result = align_to_target(read_input(input_file))
    print(' '.join([str(round(v)) for v in result]))
    print(' '.join([str(v) for v in result]))
    
if __name__ == "__main__":
    main()


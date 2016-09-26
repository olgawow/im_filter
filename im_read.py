import png
import numpy
import itertools

##f = open('dolphin.png', 'wb')
##w = png.Writer(255, 1, greyscale=True)
##w.write(f, [range(256)])
##f.close

def read_file(f='dolphin.png'):
    f = open(f, 'rb')
    pngdata = png.Reader(f).asDirect()
    arr = to_array_from_png(pngdata)
    f.close()
    return arr

def to_array_from_png(data):
    planes = data[3]['planes']
    bitdepth = data[3]['bitdepth']
    it = data[2]
    image_2d = numpy.vstack(itertools.imap(numpy.uint8, it))[:, ::planes]
    return image_2d

def unsharp_mask(input_image=read_file(f='dolphin.png')):
    multiplicator = -1/256
    kernel = numpy.array([[1, 4, 6, 4, 1], [4, 16, 24, 16, 4], [6, 24, -476, 24, 6], [4, 16, 24, 16, 4], [1, 4, 6, 4, 1]], dtype='uint8')
    output_image = input_image
    for image_row in output_image:
        for i in range(len(image_row) - 1):
            pixel = image_row[i]
            accumulator = 0
            for kernel_row in kernel:
                for j in range(len(kernel_row) - 1):
                    element = kernel_row[j]
                    if i == j:
                        result = pixel * element
                        accumulator += result
            image_row[i] = multiplicator * accumulator
    return output_image

def write_file(f='dolphin_changed.png', png_data):
    f = open(f, 'wb')
    png.Writer(f)
    f.close()

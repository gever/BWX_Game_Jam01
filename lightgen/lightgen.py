import numpy
import pygame.pixelcopy
import pygame.image

# from https://github.com/pygame/pygame/issues/1244#issuecomment-794617518
def make_surface_rgba(array):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha
    """
    shape = array.shape
    if len(shape) != 3 and shape[2] != 4:
        raise ValueError("Array not RGBA")

    # Create a surface the same width and height as array and with
    # per-pixel alpha.
    surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)

    # Copy the rgb part of array to the new surface.
    pygame.pixelcopy.array_to_surface(surface, array[:,:,0:3])

    # Copy the alpha part of array to the surface using a pixels-alpha
    # view of the surface.
    surface_alpha = numpy.array(surface.get_view('A'), copy=False)
    surface_alpha[:,:] = array[:,:,3]

    return surface

SIZE = 256
HALF_SIZE = SIZE // 2

arr = numpy.zeros((SIZE, SIZE, 4), dtype=numpy.uint8)
for x in range(SIZE):
    for y in range(SIZE):
        relx = (x - HALF_SIZE)/HALF_SIZE
        rely = (y - HALF_SIZE)/HALF_SIZE
        radial = 1 - (relx**2 + rely**2)**0.5
        # radial = 1 - (relx**2 + rely**2)
        alpha = max(0, min(1, radial))
        arr[x,y,0] = 255
        arr[x,y,1] = 255
        arr[x,y,2] = 255
        arr[x,y,3] = int(alpha * 255)
surface = make_surface_rgba(arr)

pygame.image.save(surface, '../gfx/light.png')

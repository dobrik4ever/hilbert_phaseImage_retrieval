from matplotlib import pyplot as plt
import numpy as np
import cv2
from .Hilbert import HilbertPhase

def to_image(surface,name):
    surface -= surface.min()
    surface /= surface.max()
    surface *= 255
    # surface = np.uint8([surface, surface, surface])
    cv2.imwrite(name, surface)

def surface(res,dz):
    M = np.zeros(res)
    dz = np.linspace(0,dz,res[0])
    M += dz
    return M

# E = E0 cos(kz-wt) 2pi/l * z = phi
def interfere(surface, wv):
    I = np.cos(2*np.pi/wv * surface)
    return I

def add_cell(surface, y, x, r):
    cell = np.zeros_like(surface)
    yy, xx = np.meshgrid(np.arange(cell.shape[0]), np.arange(cell.shape[1]))
    cell += -np.sqrt((xx-x)**2+(yy-y)**2+r)+r
    cell[cell<=0] = 0
    return cell


if __name__ == '__main__':  
    surface = surface((100,100),100)
    cell = add_cell(surface, 50,50,30)
    cells = surface
    I = interfere(cells, 10)

    plt.imshow(interfere(surface+cell,10))
    plt.show()
    to_image(interfere(cells, 10),'sim.jpg')
    h = HilbertPhase('sim.jpg').retrieve()
    plt.subplot(131)
    plt.imshow(cell)
    plt.plot(cell[50,:])
    plt.colorbar()
    plt.subplot(132)
    plt.imshow(h)
    plt.plot(h[50,:])
    plt.colorbar()
    plt.subplot(133)
    diff = cell-h
    plt.imshow(diff)
    plt.plot(diff[50,:])
    plt.colorbar()
    plt.show()
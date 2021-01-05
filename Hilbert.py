import numpy as np
from scipy import signal
from skimage import io, color
from skimage.restoration import unwrap_phase

class HilbertPhase:

    def __init__(self, fname, regularize = False):
        # self.wv = wavelength
        self.wv = 6378e-9
        self.fname = fname
        self.REG = regularize
        self.img = np.float64(color.rgb2gray(io.imread(self.fname)))

    def retrieve(self, delete_trend = True, wv = 1):
        self.wv = wv
        def regularize(y):
            y2 = abs(signal.hilbert(y))
            y2 /= y2.max()
            y /= y.max()
            y2 = 1/y2
            return y*y2

        def del_trend(a):
            X = np.ones([2,len(a[1])])
            X[0,:] = np.arange(0, len(a[1]))
            k = a[1] @ np.linalg.pinv(X)
            nl = k[0] * X[0,:] + k[1]
            a -= nl
            a -= a.min()
            return a

        self.img /= self.img.max()
        self.img -= self.img.mean()
        cimg = np.zeros_like(self.img)
        for i in range(cimg.shape[0]):
            if self.REG: self.img[i] = regularize(self.img[i])
            s = signal.hilbert(self.img[i,:]).imag
            cimg[i,:] = s

        pimg = -np.arctan(self.img/cimg)*2
        rimg = unwrap_phase(pimg)
        if delete_trend: rimg = del_trend(rimg)
        rimg = rimg / np.ones_like(rimg) * self.wv
        return rimg

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    h = HilbertPhase('neuron.png', True).retrieve()
    fig, ax = plt.subplots(1)
    im = ax.imshow(h)
    fig.colorbar(im)
    plt.show()
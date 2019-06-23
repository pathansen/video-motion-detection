import numpy as np

from utils.fourier_transform import FourierTransform


class PhasePlaneCorrelation(object):

    @classmethod
    def detect_motion(self, g1, g2, local=False):
        """
        Detect true motion between images `g1` and `g2`.

        :param g1: First image \\
        :param gl Second image \\
        :param local: Flag to detect local or global motion \\
        :return: Motion vector between images `g1` and `g2`
        """

        # Compute the normalized 2D Fourier Transform of the two images
        G1 = FourierTransform.fft2d(g1, normalize=True)
        G2 = FourierTransform.fft2d(g2, normalize=True)

        # Compute the Phase Plane Correlation and zero the DC component
        R = np.multiply(G2, np.conj(G1))
        r = np.fft.ifft2(R)
        r[0, 0] = 0

        max_pixel = r[0, 1]
        max_i, max_j = 0, 0

        hgt, wdt = r.shape

        for i in range(r.shape[0]):
            for j in range(r.shape[1]):
                if r[i, j] > max_pixel:
                    max_pixel = r[i, j]
                    max_i, max_j = i, j

        if max_i > (hgt / 2):
            max_i = max_i - hgt
        if max_j > (wdt / 2):
            max_j = max_j - wdt

        return max_j, max_i

    @classmethod
    def _max_pixel(self, img):
        """
        Find pixel in image with the maximum value.

        :param img: Image to find the max pixel in \\
        :return: TBD
        """
        max_pixel = img[0, 1]
        max_i, max_j = 0, 0
        hgt, wdt = img.shape

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j] > max_pixel:
                    max_pixel = img[i, j]
                    max_i = i
                    max_j = j

        if max_i > (hgt / 2):
            max_i = max_i - hgt
        if max_j > (wdt / 2):
            max_j = max_j - wdt

        return max_j, max_i


if __name__ == '__main__':
    print('working')
    PhasePlaneCorrelation.detect_motion(0, 0)

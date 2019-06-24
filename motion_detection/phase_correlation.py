import numpy as np

from .utils.fourier_transform import FourierTransform


class PhaseCorrelation(object):

    @classmethod
    def detect_motion(self, g1, g2, local=False, block_size=None):
        """
        Detect true motion between images `g1` and `g2`.

        :param g1: First image \\
        :param gl Second image \\
        :param local: Flag to detect local or global motion \\
        :param block_size: Local block size for motion detection \\
        :return: Motion vector between images `g1` and `g2`
        """

        if local is False:
            # Compute the normalized 2D Fourier Transform of the two images
            G1 = FourierTransform.fft2d(g1, normalize=True)
            G2 = FourierTransform.fft2d(g2, normalize=True)

            # Compute the Phase Correlation and zero the DC component
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

        else:
            # Compute the normalized 2D Fourier Transform of the two images
            G1 = FourierTransform.fft2d(g1, block_size=block_size,
                                        normalize=True)
            G2 = FourierTransform.fft2d(g2, block_size=block_size,
                                        normalize=True)

            # Get image height and width
            img_hgt, img_wdt = g1.shape

            # Seperate into blocks
            if block_size is None:
                vrt_blocks = 1
                hrz_blocks = 1
                block_size = (img_hgt, img_wdt)
            else:
                vrt_blocks = img_hgt // block_size[0]
                hrz_blocks = img_wdt // block_size[1]

            # Array of complex data type for output of Fourier Transform
            r = np.zeros((img_hgt, img_wdt), dtype=complex) + 1
            p = []

            i_min, i_max = 0, block_size[0]
            j_min, j_max = 0, block_size[1]
            for i in range(vrt_blocks):
                for j in range(hrz_blocks):

                    # Split images up by block
                    current_G1 = G1[i_min:i_max, j_min:j_max]
                    current_G2 = G2[i_min:i_max, j_min:j_max]
                    current_R = np.multiply(current_G2, np.conj(current_G1))

                    # Compute the Phase Correlation and zero the DC component
                    r[i_min:i_max, j_min:j_max] = FourierTransform.ifft2d(
                        current_R)
                    r[i_min, j_min] = 0

                    max_pixel = r[i_min, j_min]
                    max_i, max_j = i_min, j_min
                    # hgt, wdt = r.shape

                    for m in range(i_min, i_max):
                        for n in range(j_min, j_max):
                            if r[m, n] > max_pixel:
                                max_pixel = r[m, n]
                                max_i = m - i_min
                                max_j = n - j_min

                    if max_i > (block_size[0] / 2):
                        max_i = max_i - block_size[0]
                    if max_j > (block_size[1] / 2):
                        max_j = max_j - block_size[1]

                    # Append motion vectors as (delta_x, delta_y)
                    p.append((max_j, max_i))

                    j_min += block_size[1]
                    j_max += block_size[1]

                i_min += block_size[0]
                i_max += block_size[0]
                j_min, j_max = 0, block_size[1]

            return p

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

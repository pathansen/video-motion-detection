import numpy as np


class FourierTransform(object):

    @staticmethod
    def fft2d(g_img, block_size=None, normalize=False):
        """
        Compute the 2D Fourier Transform (FT) of image `g_img`.

        :param g_img: Image in 2D spatial domain \\
        :param block_size: Size of local blocks to compute 2D FT of \\
        :param normalize: Flag to return regularized FT of image \\
        :return: Image in 2D frequency domain
        """

        # Get image width and height
        img_hgt, img_wdt = g_img.shape

        # Setup blocks based on block_size parameter
        if block_size is None:
            vrt_blocks = 1
            hrz_blocks = 1
            block_size = (img_hgt, img_wdt)
        else:
            vrt_blocks = img_hgt // block_size[0]
            hrz_blocks = img_wdt // block_size[1]

        # TODO: Add window function(s)

        # Array of complex data type for output of Fourier Transform
        G_img = np.zeros((img_hgt, img_wdt), dtype=complex)

        i_min, i_max = 0, block_size[0]
        j_min, j_max = 0, block_size[1]
        for i in range(vrt_blocks):
            for j in range(hrz_blocks):

                # Take Fast Fourier Transform of current block
                current_img = g_img[i_min:i_max, j_min:j_max]
                G_img[i_min:i_max, j_min:j_max] = np.fft.fft2(current_img)

                j_min += block_size[1]
                j_max += block_size[1]

            i_min += block_size[0]
            i_max += block_size[0]
            j_min, j_max = 0, block_size[1]

        if normalize:
            return np.divide(G_img, np.abs(G_img) + 0.01)
        else:
            return G_img

    @staticmethod
    def ifft2d(G_img, block_size=None):
        """
        Compute the 2D Inverse Fourier Transform (IFT) of image `g_img`.

        :param G_img: Image in 2D frequency domain \\
        :param block_size: Size of local blocks to compute 2D IFT of \\
        :return: Image in 2D spatial domain
        """

        # Get image width and height
        img_hgt, img_wdt = G_img.shape

        # Setup blocks based on block_size parameter
        if block_size is None:
            vrt_blocks = 1
            hrz_blocks = 1
            block_size = (img_hgt, img_wdt)
        else:
            vrt_blocks = img_hgt // block_size[0]
            hrz_blocks = img_wdt // block_size[1]

        # Array of complex data type for output of Inverse Fourier Transform
        g_img = np.zeros((img_hgt, img_wdt), dtype=complex)

        i_min, i_max = 0, block_size[0]
        j_min, j_max = 0, block_size[1]
        for i in range(vrt_blocks):
            for j in range(hrz_blocks):

                # Take Inverse Fast Fourier Transform of current block
                current_img = G_img[i_min:i_max, j_min:j_max]
                g_img[i_min:i_max, j_min:j_max] = np.fft.ifft2(current_img)

                j_min += block_size[1]
                j_max += block_size[1]

            i_min += block_size[0]
            i_max += block_size[0]
            j_min, j_max = 0, block_size[1]

        return g_img

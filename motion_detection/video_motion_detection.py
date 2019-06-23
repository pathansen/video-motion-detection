import os
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from PIL import Image

from .phase_correlation import PhaseCorrelation


class VideoMotionDetection(object):

    @staticmethod
    def run(path_to_frames='',
            org_wdt=0,
            org_hgt=0,
            img_wdt=0,
            img_hgt=0,
            local=False,
            block_size=None,
            verbose=False):
        """
        Detect motion in a video sequence frame by frame.

        :param org_wdt: Width of original video sequence \\
        :param org_hgt: Height of original video sequence \\
        :param img_wdt: Width of output video sequence \\
        :param img_hgt: Height of output video sequence \\
        :param local: Flag for local motion detection \\
        :param block_size: Local block size for motion detection \\
        :return: TBD
        """

        if block_size is None:
            block_size = (img_hgt, img_wdt)

        # Setup block sizes
        vrt_blocks = img_hgt // block_size[0]
        hrz_blocks = img_wdt // block_size[1]

        # Get all video frames
        all_frames = os.listdir(path_to_frames)
        all_frames.remove('.gitkeep')

        # Figure size setup
        fig = plt.gcf()
        DPI = fig.get_dpi()
        fig.set_size_inches(1280 / float(DPI), 720 / float(DPI))

        img2draw, prev_frame = None, all_frames[0]
        for i in range(1, len(all_frames)):

            crnt_frame = all_frames[i]

            # Open frames (and convert to grayscale)
            g1 = Image.open(path_to_frames + prev_frame).convert(
                'LA').resize((img_wdt, img_hgt), Image.ANTIALIAS)
            g2 = Image.open(path_to_frames + crnt_frame).convert(
                'LA').resize((img_wdt, img_hgt), Image.ANTIALIAS)

            # Convert frames to numpy arrays
            g1 = np.array(g1.getdata())[:, 0].reshape(
                (img_hgt, img_wdt)).astype(np.uint8)
            g2 = np.array(g2.getdata())[:, 0].reshape(
                (img_hgt, img_wdt)).astype(np.uint8)

            im = pl.imread(path_to_frames + crnt_frame)
            if img2draw is None:
                img2draw = pl.imshow(im)
            else:
                img2draw.set_data(im)

            # TODO: Add local motion support here
            # Detect motion between frames
            p = PhaseCorrelation.detect_motion(g1, g2, local=False)
            if verbose:
                print('{} --> {} : {}'.format(prev_frame, crnt_frame, p))

            # Draw frames here...
            origin = [org_wdt // 2], [org_hgt // 2]
            Q = pl.quiver(*origin, p[0], -p[1], color=['r'], scale=21)

            # pl.pause(.2)
            pl.draw()
            pl.savefig(os.path.join(os.getcwd(), 'motion_detection',
                       'out', 'out_%03d.png' % i))

            for artist in plt.gca().lines + plt.gca().collections:
                artist.remove()

            prev_frame = all_frames[i]

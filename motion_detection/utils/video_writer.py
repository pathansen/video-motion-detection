import os
import ffmpeg


class VideoWriter(object):

    @staticmethod
    def write(filename=None, fps=30):
        """
        Write sequence of frames to a MPEG video file.

        :param filename: Output filename for video \\
        :param fps: Frame rate of output video
        """

        # Input sequence of images
        stream = ffmpeg.input(os.path.join(
                                os.getcwd(),
                                'motion_detection',
                                'out',
                                'out_%3d.png'))

        # Set frame rate (default is 30 frames per second)
        stream = ffmpeg.filter(stream, 'fps', fps=fps)

        # Output video sequence
        stream = ffmpeg.output(stream,
                               os.path.join(
                                   os.getcwd(),
                                   'motion_detection',
                                   'video',
                                   filename))

        # Generate output video
        ffmpeg.run(stream)

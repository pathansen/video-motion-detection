import os
import ffmpeg


class VideoReader(object):

    @staticmethod
    def read(filename=None):
        """
        Write sequence of frames to a MPEG video file.

        :param filename: Input filename for video \\
        """

        # Input video sequence to break down into frames
        stream = ffmpeg.input(stream,
                              os.path.joins(
                                  os.getcwd(),
                                  'motion_detection',
                                  'video',
                                  filename))

        # Output sequence of frames
        stream = ffmpeg.output(os.path.join(
                                os.getcwd(),
                                'motion_detection',
                                'out',
                                'out_%3d.png'))

        # Generate output sequence
        ffmpeg.run(stream)

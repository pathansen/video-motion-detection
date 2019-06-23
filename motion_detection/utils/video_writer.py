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

        filename = './motion_detection/video/out.mp4'

        # stream = ffmpeg.input('img/img_%3d.png')
        stream = ffmpeg.input(os.path.join(os.getcwd(), 'motion_detection',
                              'out', 'out_%3d.png'))
        stream = ffmpeg.filter(stream, 'fps', fps=fps)
        stream = ffmpeg.output(stream, filename)
        ffmpeg.run(stream)

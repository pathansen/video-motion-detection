# True Motion Detection in Video

True motion can be detected in video using _Phase Correlation_ between subsequent frames. Motion detected using _Phase Correlation_ differs from motion estimation used in video compression techniques because _Phase Correlation_ detects true motion while motion estimation techniques are used to compress data (_i.e._, the estimated motion may not correlate to motion in the video sequence).

## Environment Setup

First, create a virtual environment:

```
$ pip install virtualenv
$ virtualenv -p python .venv
```

Activate the virtual enviornment:

Windows:

```
$ source .venv/Scripts/activate
```

macOS or Linux:

```
$ source .venv/bin/activate
```

Install the requirements:

```
$ pip install -r requirements.txt
```

Install `ffmpeg` from website or package manager: https://ffmpeg.org/

## Example Code

```
from motion_detection.video_motion_detection import VideoMotionDetection
from motion_detection.utils.video_writer import VideoWriter


VideoMotionDetection.run(
    path_to_frames='./motion_detection/img/',
    org_wdt=1920,
    org_hgt=1080,
    img_wdt=1280,
    img_hgt=720)

VideoWriter.write('out.mp4')
```

---

## Useful `ffmpeg` Commands:

### Breakdown Video Sequence:
```
$ ffmpeg -i video/test.MOV img/img_%03d.png
```

### Build Video Sequence:
```
$ ffmpeg -r 30 -i out/out_%03d.png -vframes 120 -pix_fmt yuv420p -c:v libx264 -r 30 -tune psnr -psnr -qmin 30 -qmax 30 -g 12 -bf 2 test.mp4
```

### Loop Video:
```
$ ffplay -loop 0 out.mp4
```

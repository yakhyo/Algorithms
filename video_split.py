import os
import time
import uuid
from tqdm import tqdm
from typing import Union, List
from moviepy.editor import VideoFileClip


def extract(filenames: Union[List, str], clip_len: float = 10, ext: Union[List, str] = None) -> None:
    """
    :param filenames: path to a file or list of file paths
    :param clip_len: length for clips
    :param ext: file extension
    :return: None
    """
    if ext is None:
        ext = [".mp4", ".avi"]

    if isinstance(ext, str):
        ext = [ext]

    if isinstance(filenames, list):
        filenames = [filename for filename in filenames if os.path.splitext(filename)[1] in ext]
    else:
        filenames = [filenames if os.path.splitext(filenames)[1] in ext else print("Please check the file extension")]

    for filename in tqdm(filenames, total=len(filenames), colour="green"):

        try:
            # read video
            video = VideoFileClip(filename)
            video = video.without_audio()  # you can save it without using audio
            length = video.duration

            start, step = 0, clip_len
            while start + step < length:
                # clip and write
                f_name = str(uuid.uuid4()) + ".mp4"
                clip = video.subclip(start, start + step)
                clip.write_videofile(f_name, threads=os.cpu_count())
                start += step

            f_name = str(uuid.uuid4()) + ".mp4"
            clip = video.subclip(start, length)
            clip.write_videofile(f_name, threads=os.cpu_count())

        except Exception as msg:
            print(msg)


if __name__ == '__main__':
    root = './data'
    filepaths = [os.path.join(root, filename) for filename in os.listdir(root)]

    st = time.time()
    extract(filenames=filepaths, clip_len=10, ext=".mp4")
    print("Elapsed time: {}".format(time.time() - st))

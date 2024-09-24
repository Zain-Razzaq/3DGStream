import os
import subprocess
import argparse
import cv2
from pathlib import Path

def extractframes(videopath: Path, startframe=0, endframe=300, downscale=1, save_subdir = '', ext='png'):
    output_dir = Path(save_subdir) / videopath.stem
    print(f"Extracting frames from {videopath} to {output_dir}")
    if all((output_dir / f"{i}.{ext}").exists() for i in range(startframe, endframe)):
        print(f"Already extracted all the frames in {output_dir}")
        return

    cam = cv2.VideoCapture(str(videopath))
    cam.set(cv2.CAP_PROP_POS_FRAMES, startframe)

    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(startframe, endframe):
        success, frame = cam.read()
        if not success:
            print(f"Error reading frame {i}")
            break

        if downscale > 1:
            new_width, new_height = int(frame.shape[1] / downscale), int(frame.shape[0] / downscale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

        cv2.imwrite(str(output_dir / f"{i}.{ext}"), frame)

    cam.release()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert video to frames")
    parser.add_argument("--source_path","-s" ,type=str, help="Path to video file")
    parser.add_argument("--output_dir","-d", type=str, help="Output directory for frames")
    parser.add_argument("--frame_rate", type=int, default=30, help="Frame rate for extracting frames")
    args = parser.parse_args()
    print(args)
    # Convert video to frames
    # get video list
    videoslist = sorted(Path(args.source_path).glob("*.mp4"))
    # first create all folders
    for video in videoslist:
        output_dir = Path(args.output_dir)
        for i in range(0, 300):
            Path(output_dir / f"frame{i:06d}").mkdir(parents=True, exist_ok=True)

    # then transfer the frames
    for video in videoslist:
        extractframes(video, save_subdir=args.output_dir, ext='jpg')
        output_dir = Path(args.output_dir)
        for i in range(0, 300):
            os.rename(output_dir / video.stem / f"{i}.jpg", output_dir / f"frame{i:06d}" / f"{video.stem}.jpg")
        os.rmdir(output_dir / video.stem)
    print("Done")


    
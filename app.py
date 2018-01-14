import argparse


p = argparse.ArgumentParser()

p.add_argument('-v', '--video',    action='append', nargs=2, help='detect from .mp4 video')
p.add_argument('-r', '--realtime', action='store_true',      help='detect from live camera feed')
p.add_argument('-g', '--generate', action='store_true',      help='generate classes from .mp4 videos')
p.add_argument('-d', '--delete',   action='store_true',      help='delete existing models')

args = p.parse_args()

if args.video:
    print('Detecting from video...')
    from src.video_detect import VideoDetect
    source = args.video[0][0]
    destination = args.video[0][1]
    VideoDetect().detect(source, destination)
elif args.realtime:
    print('Detecting from live feed...')
    from src.realtime_detect import RealtimeDetect
    RealtimeDetect().detect()
elif args.generate:
    print('Generating classes from video...')
    from src.classes_from_videos import ClassesFromVideos
    ClassesFromVideos().generate()
elif args.delete:
    print('Deleting existing models...')
    from src.cleanup import Cleanup
    Cleanup().cleanup()
else:
    p.print_help()


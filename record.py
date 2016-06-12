#!/usr/bin/python3

import subprocess
import os
from datetime import datetime

def main():
    base_dir = os.getcwd()
    date_format = '%d-%m-%y'
    hour_format = '%H00'
    
    now = datetime.now()
    date_now = datetime.strftime(now, date_format)
    hour_now = datetime.strftime(now, hour_format)
    
    ports = [p for p in range(81,87)]
    processes = []

    for port in ports:
        cam_dir = os.path.join(base_dir, 'port' + str(port))
        date_dir = os.path.join(cam_dir, date_now)
        hourly_dir = os.path.join(date_dir, hour_now)
        
        if not os.path.isdir(cam_dir):
            os.mkdir(cam_dir)
        if not os.path.isdir(date_dir):
            os.mkdir(date_dir)
        if not os.path.isdir(hourly_dir):
            os.mkdir(hourly_dir)

        record(hourly_dir, port, processes)
        
    [sp.wait() for sp in processes]
            
def record(directory, cam_port, processes):
    os.chdir(directory)
    
    #  user = ''
    #  passwd = ''
    #  domain = ''
    duration = '60'
    output_file = datetime.strftime(datetime.now(), '%H%M') + '.avi'
    
    command_mjpeg = [
        'ffmpeg',
        '-t', duration,
        '-f', 'mjpeg',
        '-timeout', '9999999',
        '-r', '5',
        '-i', 'http://{0}:{1}@{2}:{3}/mjpeg.cgi'.format(user, passwd, domain, cam_port),
        '-vcodec', 'mpeg4',
        '-preset', 'veryfast',
        '-use_wallclock_as_timestamps', '1',
        output_file
    ]
    
    command_h264 = [
        'ffmpeg',
        '-t', duration,
        '-f', 'h264',
        '-timeout', '9999999',
        '-r', '10',
        '-i', 'http://{0}:{1}@{2}:{3}/h264.cgi'.format(user, passwd, domain, cam_port),
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-use_wallclock_as_timestamps', '1',
        output_file
    ]
    
    if cam_port == 82:
        process = subprocess.Popen(command_mjpeg)
        processes.append(process)
    else:
        process = subprocess.Popen(command_h264)
        processes.append(process)
    
if __name__ == "__main__":
    main()

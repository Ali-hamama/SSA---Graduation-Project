import os 
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
from reportlab.pdfgen import canvas

def path_validate(video_path, interval):
    """
    This function check if the passed path are valid or not, and compaire the intervals with the video duration

    Parameters:
    video_path - String, represents the path of the lecture's video
    interval - int, the value in sec to split the main video into it

    Return:
    True or False with message that explains the occured error
    """
    if(os.path.isfile(video_path)):
        clip = VideoFileClip(video_path)
        dur = int(clip.duration)
        if interval <= dur:
            num_splits = int(round(dur/interval))
            return (num_splits,True)
        else:
            print ('Interval is not proper..!')
            return (0,False)
    else:
        print('File Not Found..!')
        return (0,False)



def split_video(video_path,interval):
    """
    This function splits the Video and prepares it to analysis

    Parameter:
    video_path - String, represents the path of the lecture's video
    interval - int, the value in sec to split the main video into it

    Return:
    int - video duration
    """
    clip = VideoFileClip(video_path)
    d = np.arange(int(clip.duration))
    start = 0
    if(interval > d[-1]):
            interval = d[-1]
    end = interval
    times = []
    while(True):
        if(d[start]+interval-1 >= d[-1]):
            times.append(f'{d[start]}-{d[-1]+1}')
            break
        times.append(f'{d[start]}-{d[end]}')
        start = end
        end = end + interval

    
    for time in times:
        starttime = int(time.split("-")[0])
        endtime = int(time.split("-")[1])
        ffmpeg_extract_subclip(video_path, starttime, endtime, targetname='E:\\Graduation Project\\Full Project\\Video_temp\\'+str(times.index(time)+1)+".mp4")
    return int(clip.duration)

def save_report(image_path, st_name, level, interval, duration):
        """
        This fuction create a report about video analysis result, and save it as PDF file

        Parameters:
        image_path - string, the path of the saved graph
        st_name - string, the student name
        level - the average level of attentiveness
        interval - int, the value in sec to split the main video into it
        duration - int, video duration int minutes 

        """
        report = canvas.Canvas(f'{st_name} Report.pdf')
        report.setFont('Times-Bold',25)
        report.setTitle('Student Report')
        report.drawCentredString(300,770,'Student Attentivness Report')
        report.line(30,760,550,760)

        report.setFont('Courier-Bold',15)
        report.drawString(30,675,f'Name: {st_name}')
        report.drawString(30,650,f'Lecture Duration: {duration} Minutes')
        report.drawString(30,625,f'Analysis intervals: {interval} Seconds')
        report.drawString(30,600,f'Level Of Attentiveness: {level}%')
        report.line(30,550,270,550)
        report.drawInlineImage(image_path,5,250,width=620, height=300)
        report.save()

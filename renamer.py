import os
import re

# Features:
# 1- Removing all unrelated files from the directory with video and subtitle files
##
# 2- Renaming subtitle files with the matching video file name
#    2.1- Video files may be sitcoms. In this case the file name contains season number and episode number.
#         In this case most common naming formats are either dot (30.Rock.S07E06.HDTV.x264-LOL) or 
#         hyphen (30 Rock - 07x08 - My Whole Life Is Thunder.LOL) separated.
#
#    2.2- Video files may be movies. Movies may be composed of one of multiple parts.


#TODO list
# 1- Recursive progress if subfolders are present
#
# 2- Retrieve file names from http://docs.themoviedb.apiary.io and
#    name both the subtitle and the video accordingly
#
# 3- Automatic download of subtitles. Unzipping the subtitles and 
#    moving them to the same folder as the movie files
#
# 4- Automatic download of torrent files and starting the torrent application
#
# 5- Moving the subtitles and the movie files to a given folder
#
# 6- Add UI 

supported_video_formats = ['.avi', '.mkv', '.mp4']
supported_subtitle_formats = ['.srt', '.sub']
    
def get_file_extension(file_name):
    ext = os.path.splitext(file_name)[-1].lower()
    return ext

def remove_unrelated_files():
    print("Removing unrelated files")
    
    num_removed_files = 0
    
    for file_name in os.listdir(os.getcwd()):
        if not os.path.isdir(file_name):
            ext = get_file_extension(file_name)
            if ext not in supported_video_formats and ext not in supported_subtitle_formats:
                try:
                    os.remove(file_name)
                    num_removed_files += 1
                except OSError:
                    print("Error while removing " + file_name)
                    
    if num_removed_files > 0:                
        print("Removal complete")
    else:
        print("No unrelated files found")
        
def get_season_and_episode_number(season_episode_name):
    season_number = ""
    episode_number = ""
    
    season_episode_name = season_episode_name.lower()
    
    episode_season_separator = ["x", "e"]
    for separator in episode_season_separator:
        if separator in season_episode_name:
            temp = season_episode_name.split(separator)
            
            season_number = temp[0]
            episode_number = temp[1]
    
    if "s" in season_number.lower():
        season_number = season_number[1:]
    
    return season_number, episode_number

def get_file_name(file_name, file_extension):
    return file_name.split(file_extension)[0]
    
class Sitcom:
    def __init__(self, season_number, episode_number, file_name):
        self.episode_number = episode_number
        self.season_number = season_number
        self.file_name = file_name
        
    def get_file_name(self):
        return self.file_name
    
    def get_episode_number(self):
        return self.episode_number
    
    def get_season_number(self):
        return self.season_number
    
    def __repr__(self):
        return " Season number: " + str(self.season_number) + "Episode number: " + str(self.episode_number)  + " File name: " + str(self.file_name) + "\n"
        
sitcom = []
        
def create_list_of_video_names():
    print("Started creating list of video file names")
    
    for file_name in os.listdir(os.getcwd()):
        if os.path.isdir(file_name):
            continue
        
        file_extension = get_file_extension(file_name)
        if file_extension in supported_subtitle_formats:
            continue
        
        match = re.search(r'([s0\w]+\w+\d)', file_name)
        # sitcom
        if match:
            season_and_episode_number = get_season_and_episode_number(match.group())
            file_name = get_file_name(file_name, file_extension)
            
            sitcom.append(Sitcom(season_and_episode_number[0], season_and_episode_number[1], file_name))
        else: # movie
            print("Not able to process yet" + file_name)
    
    print("Finished creating list of video file names")

    print(sitcom)
    

def process_subtitle_files():
    print("Started processing subtitle file names")
    
    for file_name in os.listdir(os.getcwd()):
        if os.path.isdir(file_name):
            continue
        
        file_extension = get_file_extension(file_name)
        if file_extension in supported_video_formats:
            continue
        
        match = re.search(r'([Ss0\w]+\w+\d)', file_name)
        # sitcom
        if match:
            season_and_episode_number = get_season_and_episode_number(match.group())
            
            season_number = season_and_episode_number[0]
            episode_number = season_and_episode_number[1]
            #old_name = get_file_name(file_name, file_extension)
            
            for each in sitcom:
                if season_number == each.get_season_number() and episode_number == each.get_episode_number():
                    try:
                        new_name = each.get_file_name() + file_extension
                        os.rename(file_name, new_name)
                    except OSError:
                        print("Not able to rename " + file_name)
            
        else: # movie
            print("Not able to process yet" + file_name)
            
        print("Finished processing subtitle file names")

def process_files():
    create_list_of_video_names()
    process_subtitle_files()

if __name__ == '__main__':
    absolute_path = raw_input("Enter absolute path of the directory: ")
    print ("Entered path: " + absolute_path)

    try:
        os.chdir(absolute_path)
        remove_unrelated_files()
        process_files()            
    except OSError:
        print("Exception while changing to directory: " + absolute_path)
        print("Script will not continue")
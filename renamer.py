import os
import re

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
        
            if season_number[0] == "0":
                season_number = season_number[1:]
                
            if episode_number[0] == "0":
                episode_number = episode_number[1:]
    

    
    return season_number, episode_number

def get_file_name(file_name, file_extension):
    return file_name.split(file_extension)[0]
    
class TvSeries:
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
        
tvSeries = []
movies = []

def create_list_of_video_names():
    print("Started creating list of video file names")
    
    for file_name in os.listdir(os.getcwd()):
        if os.path.isdir(file_name):
            continue
        
        file_extension = get_file_extension(file_name)
        if file_extension in supported_subtitle_formats:
            continue
        
        match = re.search(r'([s0\w]+\w+\d)', file_name)
        # tv series
        if match:
            season_and_episode_number = get_season_and_episode_number(match.group())
            file_name = get_file_name(file_name, file_extension)
            
            tvSeries.append(TvSeries(season_and_episode_number[0], season_and_episode_number[1], file_name))
            
        else: # movie
            #print("Not able to process yet" + file_name)
            file_name = get_file_name(file_name, file_extension)
            movies.append(file_name)
    
    print("Finished creating list of video file names")    

def remove_not_renamed_subtitles(file_to_remove):
    try:
        os.remove(file_to_remove)
    except OSError:
        print("Could not remove " + file_to_remove)

def rename_subtitle_file(file_name, new_file_name):
    try:
        os.rename(file_name, new_file_name)
    except OSError:
        print("Not able to rename " + file_name + " to ", new_file_name)
        print("Removing file...")
        remove_not_renamed_subtitles(file_name)
        
def process_subtitle_files():
    print("Started processing subtitle file names")
    
    for file_name in os.listdir(os.getcwd()):
        if os.path.isdir(file_name):
            continue
        
        file_extension = get_file_extension(file_name)
        if file_extension in supported_video_formats:
            continue
        
        match = re.search(r'([Ss0\w]+\w+\d)', file_name)
        # tvSeries
        if match:
            season_and_episode_number = get_season_and_episode_number(match.group())
            
            season_number = season_and_episode_number[0]
            episode_number = season_and_episode_number[1]
            #old_name = get_file_name(file_name, file_extension)
            
            for each in tvSeries:
                if season_number == each.get_season_number() and episode_number == each.get_episode_number():
                    new_name = each.get_file_name() + file_extension
                    rename_subtitle_file(file_name, new_name)
                    break
            
        else: # movie
            for movie_name in movies:
                if movie_name in file_name:
                    new_name = movie_name + file_extension
                    rename_subtitle_file(file_name, new_name)
                    break
                
    print("Finished processing subtitle file names")

def process_files():
    create_list_of_video_names()
    process_subtitle_files()

def remove_unwanted_characters(file_name):
    file_extension = get_file_extension(file_name)
    file_name = file_name.split(file_extension)[0]  
    to_replace = [".", "_"]
    
    for character in to_replace:
        if character in file_name:
            file_name = file_name.replace(character, " ")
            file_name = file_name[:-1]
            
    file_name += file_extension
    return file_name

def get_simplified_file_name(file_name, to_remove):
    file_extension = get_file_extension(file_name)
    file_name = file_name.split(to_remove)[0]    
    file_name += file_extension
    return file_name
                
def simplify_file_names():
    to_remove_from_file_name = ["HDTV","UNCUT" ,"DVDRip", "720p", ".en", "xvid"]
    
    for file_name in os.listdir(os.getcwd()):
        if os.path.isdir(file_name):
            continue
        
        for to_remove in to_remove_from_file_name:
            new_file_name = file_name
            
            if to_remove in file_name:
                new_file_name = get_simplified_file_name(file_name, to_remove)
            
            new_file_name = remove_unwanted_characters(new_file_name)
            
            if file_name != new_file_name:
                try:
                    os.rename(file_name, new_file_name)
                except OSError:
                    print("Could not rename file " + file_name + " to ", new_file_name)
            else:
                print("No need to rename " + file_name)

if __name__ == '__main__':
    absolute_path = input("Enter absolute path of the directory: ")
    print ("Entered path: " + absolute_path)

    try:
        os.chdir(absolute_path)
        remove_unrelated_files()
        simplify_file_names()
        process_files()
              
    except OSError:
        print("Exception while changing to directory: " + absolute_path)
        print("Script will not continue")

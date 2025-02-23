import cv2
import os
from PIL import Image
import datetime
from languages import TRANSLATIONS

def select_language():
    """Select the interface language (English, Japanese, or Chinese)"""
    while True:
        try:
            # Using English messages for language selection to ensure accessibility
            choice = input(TRANSLATIONS['en']['select_language'])
            if choice == '1':
                return 'en'
            elif choice == '2':
                return 'ja'
            elif choice == '3':
                return 'zh'
            else:
                print(TRANSLATIONS['en']['invalid_choice'])
        except ValueError:
            print(TRANSLATIONS['en']['invalid_choice'])

def list_videos():
    """List all video files in the video directory"""
    video_dir = "video"
    video_files = []
    for file in os.listdir(video_dir):
        if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_files.append(file)
    return video_files

def time_to_frame(video_path, time_str):
    """Convert time string (hh:mm:ss.xxx) to frame position"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    try:
        # Split main time and milliseconds
        if '.' in time_str:
            main_time, milliseconds = time_str.split('.')
        else:
            main_time = time_str
            milliseconds = '0'
        
        time_parts = main_time.split(':')
        if len(time_parts) != 3:
            raise ValueError("Time format must be hh:mm:ss.xxx")
        
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2])
        milliseconds = int(milliseconds.ljust(3, '0')[:3])  # Ensure milliseconds has 3 digits
        
        # Calculate total seconds including milliseconds
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        frame_number = int(total_seconds * fps)
        
    except (ValueError, IndexError) as e:
        raise ValueError("Time format must be hh:mm:ss.xxx")
    
    cap.release()
    return frame_number

def extract_frame(video_file, time_str, lang):
    """Extract the frame at specified time and save as TIFF format"""
    video_path = os.path.join("video", video_file)
    frame_number = time_to_frame(video_path, time_str)
    
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    if ret:
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Create PIL image
        image = Image.fromarray(frame_rgb)
        
        # Build output filename
        output_filename = f"{os.path.splitext(video_file)[0]}_{time_str.replace(':', '-')}.tiff"
        output_path = os.path.join("img", output_filename)
        
        # Save TIFF file
        image.save(output_path, format='TIFF')
        print(TRANSLATIONS[lang]['frame_saved'].format(output_path))
    else:
        print(TRANSLATIONS[lang]['frame_error'])
    
    cap.release()

def main():
    # Select language
    lang = select_language()
    texts = TRANSLATIONS[lang]
    
    # List all video files
    video_files = list_videos()
    if not video_files:
        print(texts['no_videos'])
        return
    
    # Display video list
    print(texts['available_videos'])
    for i, video in enumerate(video_files, 1):
        print(f"[{i}] {video}")
    
    # User selects video
    while True:
        try:
            choice = int(input(texts['select_video']))
            if 1 <= choice <= len(video_files):
                selected_video = video_files[choice - 1]
                break
            else:
                print(texts['invalid_selection'])
        except ValueError:
            print(texts['invalid_number'])
    
    # User inputs timestamp
    while True:
        time_str = input(texts['enter_timestamp'])
        try:
            if '.' in time_str:
                main_time, ms = time_str.split('.')
                # Validate main time format
                datetime.datetime.strptime(main_time, '%H:%M:%S')
                # Validate milliseconds format
                if not ms.isdigit() or len(ms) > 3:
                    raise ValueError
            else:
                # If no milliseconds, validate basic time format
                datetime.datetime.strptime(time_str, '%H:%M:%S')
            break
        except ValueError:
            print(texts['invalid_time'])
    
    # Extract and save frame
    extract_frame(selected_video, time_str, lang)

if __name__ == "__main__":
    main()

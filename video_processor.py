import os
from datetime import datetime
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image

class VideoProcessor:
    def extract_frames(self, video_path, frame_count, interval_ms):
        """
        Extract frames from a video file.
        
        Args:
            video_path (str): Path to the video file
            frame_count (int): Number of frames to extract
            interval_ms (int): Interval between frames in milliseconds
        
        Returns:
            str: Path to the output folder containing extracted frames
        """
        # Create output directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f'static/frames_{timestamp}'
        os.makedirs(output_dir, exist_ok=True)

        # Load video
        video = VideoFileClip(video_path)
        
        # Calculate frame interval in seconds
        interval_sec = interval_ms / 1000.0
        
        # Calculate total duration needed
        total_duration = interval_sec * (frame_count - 1)
        
        # Check if video is long enough
        if total_duration > video.duration:
            # Adjust interval if video is too short
            interval_sec = video.duration / (frame_count - 1)
        
        frames_saved = 0
        current_time = 0
        
        while frames_saved < frame_count and current_time <= video.duration:
            # Get frame at current time
            frame = video.get_frame(current_time)
            
            # Convert to PIL Image and save
            image = Image.fromarray(frame)
            frame_path = os.path.join(output_dir, f'{frames_saved + 1}.png')
            image.save(frame_path, quality=95)
            
            frames_saved += 1
            current_time += interval_sec
        
        video.close()
        return output_dir 
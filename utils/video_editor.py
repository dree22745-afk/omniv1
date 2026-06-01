# utils/video_editor.py

import os
from moviepy.editor import *
from moviepy.video.fx.all import *
import numpy as np
from PIL import Image

class VideoEditor:
    """Professional Video Editor using MoviePy"""
    
    def __init__(self):
        self.output_dir = "videos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Platform dimensions
        self.dimensions = {
            "YouTube": (1920, 1080),      # 16:9
            "Instagram Reel": (1080, 1920), # 9:16
            "TikTok": (1080, 1920)         # 9:16
        }
    
    def create_video(self, scene_plan, image_paths, audio_files, output_name="final_video"):
        """Create final video from scenes"""
        
        try:
            platform = scene_plan.get('platform', 'YouTube')
            video_size = self.dimensions.get(platform, (1920, 1080))
            
            video_clips = []
            
            for i, scene in enumerate(scene_plan['scenes']):
                scene_num = scene['scene_number']
                duration = scene.get('duration', 5)
                effect = scene.get('effect', 'none')
                transition = scene.get('transition', 'none')
                
                # Get image path
                image_data = next((img for img in image_paths if img['scene_number'] == scene_num), None)
                if not image_data or not image_data.get('path'):
                    print(f"Scene {scene_num}: No image, skipping...")
                    continue
                
                image_path = image_data['path']
                
                # Create image clip
                try:
                    clip = ImageClip(image_path).set_duration(duration)
                except:
                    # Fallback: Create blank clip
                    clip = ColorClip(size=video_size, color=(20, 20, 40)).set_duration(duration)
                
                # Resize to fit video dimensions
                clip = clip.resize(newsize=video_size)
                
                # Apply effects
                clip = self.apply_effect(clip, effect, duration)
                
                # Get audio
                audio_data = next((aud for aud in audio_files if aud['scene_number'] == scene_num), None)
                if audio_data and audio_data.get('path'):
                    try:
                        audio_clip = AudioFileClip(audio_data['path'])
                        # Trim audio to match scene duration
                        if audio_clip.duration > duration:
                            audio_clip = audio_clip.subclip(0, duration)
                        clip = clip.set_audio(audio_clip)
                    except:
                        pass
                
                video_clips.append(clip)
            
            if not video_clips:
                return False, "No valid clips to create video!"
            
            # Concatenate all clips
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Output path
            output_path = f"{self.output_dir}/{output_name}.mp4"
            
            # Write video file
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=4,
                preset='medium'
            )
            
            # Close all clips
            final_video.close()
            for clip in video_clips:
                clip.close()
            
            return True, output_path
            
        except Exception as e:
            return False, f"Video creation error: {str(e)}"
    
    def apply_effect(self, clip, effect_name, duration):
        """Apply visual effects to clip"""
        
        try:
            if effect_name == "slow_zoom_in":
                # Slow zoom in effect
                return clip.resize(lambda t: 1 + 0.05 * (t / duration))
            
            elif effect_name == "slow_zoom_out":
                # Slow zoom out effect
                return clip.resize(lambda t: 1.1 - 0.05 * (t / duration))
            
            elif effect_name == "pan_left":
                # Pan from left to right
                def pan_left_effect(get_frame, t):
                    frame = get_frame(t)
                    shift = int((t / duration) * frame.shape[1] * 0.1)
                    return np.roll(frame, shift, axis=1)
                return clip.fl(pan_left_effect)
            
            elif effect_name == "pan_right":
                # Pan from right to left
                def pan_right_effect(get_frame, t):
                    frame = get_frame(t)
                    shift = int((t / duration) * frame.shape[1] * 0.1)
                    return np.roll(frame, -shift, axis=1)
                return clip.fl(pan_right_effect)
            
            else:
                # No effect
                return clip
                
        except Exception as e:
            print(f"Effect error: {str(e)}")
            return clip
    
    def add_music(self, video_path, music_path, volume=0.3):
        """Add background music to video"""
        
        try:
            video = VideoFileClip(video_path)
            music = AudioFileClip(music_path)
            
            # Loop music if shorter than video
            if music.duration < video.duration:
                music = music.loop(duration=video.duration)
            else:
                music = music.subclip(0, video.duration)
            
            # Adjust volume
            music = music.volumex(volume)
            
            # Mix with original audio
            if video.audio:
                final_audio = CompositeAudioClip([video.audio, music])
                video = video.set_audio(final_audio)
            else:
                video = video.set_audio(music)
            
            # Save
            output_path = video_path.replace('.mp4', '_with_music.mp4')
            video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
            
            video.close()
            music.close()
            
            return True, output_path
            
        except Exception as e:
            return False, str(e)
    
    def get_video_duration(self, video_path):
        """Get duration of video file"""
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            return duration
        except:
            return 0
    
    def cleanup_temp_files(self):
        """Remove temporary files"""
        import shutil
        temp_dirs = ['generated_images', 'generated_audio']
        for dir_path in temp_dirs:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                os.makedirs(dir_path)
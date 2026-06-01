# utils/voiceover.py

import os
import requests
import time
from elevenlabs import generate, save, set_api_key, voices

class VoiceoverGenerator:
    """Voiceover Generation using ElevenLabs"""
    
    def __init__(self):
        api_key = os.environ.get('ELEVENLABS_API_KEY', '')
        if not api_key:
            raise Exception("ElevenLabs API key not found!")
        
        set_api_key(api_key)
        
        # Voice settings
        self.voice_options = {
            "adam": "pNInz6obpgDQGcFmaJgB",  # Adam (Male English)
            "bella": "EXAVITQu4vr4xnSDxMaL",  # Bella (Female English)
            "antoni": "ErXwobaYiN019PkySvjV",  # Antoni (Male - good for motivational)
            "rachel": "21m00Tcm4TlvDq8ikWAM",  # Rachel (Female - calm)
        }
        
        # Audio directory
        self.audio_dir = "generated_audio"
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
        
        self.voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True
        }
    
    def generate_voice(self, text, scene_number, voice_name="adam"):
        """Generate voiceover for a scene"""
        
        try:
            voice_id = self.voice_options.get(voice_name, self.voice_options['adam'])
            
            # Generate audio
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_multilingual_v2",
                **self.voice_settings
            )
            
            # Save audio file
            audio_path = f"{self.audio_dir}/scene_{scene_number}.mp3"
            save(audio, audio_path)
            
            return True, audio_path
            
        except Exception as e:
            print(f"Voiceover error for scene {scene_number}: {str(e)}")
            return False, str(e)
    
    def generate_full_voiceover(self, script, voice_name="adam"):
        """Generate full voiceover from complete script"""
        
        try:
            voice_id = self.voice_options.get(voice_name, self.voice_options['adam'])
            
            audio = generate(
                text=script,
                voice=voice_id,
                model="eleven_multilingual_v2",
                **self.voice_settings
            )
            
            audio_path = f"{self.audio_dir}/full_voiceover.mp3"
            save(audio, audio_path)
            
            return True, audio_path
            
        except Exception as e:
            return False, str(e)
    
    def generate_scene_audio(self, scene_plan, voice_name="adam"):
        """Generate audio for each scene"""
        
        audio_files = []
        
        for scene in scene_plan['scenes']:
            scene_num = scene['scene_number']
            voice_text = scene.get('voice_text', '')
            
            if not voice_text:
                print(f"Scene {scene_num}: No voice text, skipping...")
                audio_files.append({
                    'scene_number': scene_num,
                    'path': None
                })
                continue
            
            print(f"Generating voiceover for scene {scene_num}...")
            
            success, path = self.generate_voice(voice_text, scene_num, voice_name)
            
            if success:
                audio_files.append({
                    'scene_number': scene_num,
                    'path': path,
                    'text': voice_text
                })
                print(f"Scene {scene_num} audio saved: {path}")
            else:
                print(f"Failed to generate scene {scene_num} audio: {path}")
                audio_files.append({
                    'scene_number': scene_num,
                    'path': None,
                    'error': path
                })
            
            # Delay to avoid rate limits
            time.sleep(0.5)
        
        return audio_files
    
    def get_available_voices(self):
        """Get list of available voices"""
        try:
            voice_list = voices()
            return [v.name for v in voice_list]
        except:
            return list(self.voice_options.keys())
    
    def cleanup_audio(self):
        """Delete all generated audio files"""
        import shutil
        if os.path.exists(self.audio_dir):
            shutil.rmtree(self.audio_dir)
            os.makedirs(self.audio_dir)
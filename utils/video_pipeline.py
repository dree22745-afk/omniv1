# utils/video_pipeline.py

import os
import time
from utils.gemini_ai import GeminiAI
from utils.image_generator import ImageGenerator
from utils.voiceover import VoiceoverGenerator
from utils.video_editor import VideoEditor
from utils.database import Database

class VideoPipeline:
    """Complete Video Generation Pipeline"""
    
    def __init__(self):
        self.gemini = GeminiAI()
        self.image_gen = ImageGenerator()
        self.voice_gen = VoiceoverGenerator()
        self.editor = VideoEditor()
        
        # Credit costs
        self.credit_costs = {
            "YouTube": 10,
            "Instagram Reel": 5,
            "TikTok": 5
        }
    
    def generate_video(self, user_email, command, platform, duration, quality="HD (1080p)", voice="adam"):
        """
        Complete video generation process
        
        Returns: (success, message, video_path)
        """
        
        try:
            # Step 1: Check credits
            user_data = Database.get_user(user_email)
            if not user_data:
                return False, "User not found!", None
            
            credit_cost = self.credit_costs.get(platform, 5)
            if user_data['credits'] < credit_cost:
                return False, f"Insufficient credits! Need {credit_cost}, have {user_data['credits']}", None
            
            # Step 2: Deduct credits
            success, new_balance = Database.deduct_credits(user_email, credit_cost)
            if not success:
                return False, "Failed to deduct credits!", None
            
            # Step 3: Generate script with Gemini
            print("📝 Generating script with AI...")
            success, script_plan = self.gemini.generate_script(command, platform, duration)
            
            if not success:
                # Refund credits on failure
                Database.add_credits(user_email, credit_cost)
                return False, f"Script generation failed: {script_plan}", None
            
            print(f"✅ Script generated! {len(script_plan['scenes'])} scenes planned.")
            
            # Step 4: Generate images
            print("🖼️ Generating images...")
            image_paths = self.image_gen.generate_all_scene_images(script_plan)
            
            valid_images = [img for img in image_paths if img.get('path')]
            print(f"✅ Generated {len(valid_images)}/{len(image_paths)} images.")
            
            # Step 5: Generate voiceover
            print("🎙️ Generating voiceover...")
            audio_files = self.voice_gen.generate_scene_audio(script_plan, voice)
            
            valid_audio = [aud for aud in audio_files if aud.get('path')]
            print(f"✅ Generated {len(valid_audio)}/{len(audio_files)} audio clips.")
            
            # Step 6: Create video
            print("🎬 Assembling video...")
            video_name = f"video_{int(time.time())}"
            success, video_path = self.editor.create_video(
                script_plan, image_paths, audio_files, video_name
            )
            
            if not success:
                # Refund credits on failure
                Database.add_credits(user_email, credit_cost)
                return False, f"Video assembly failed: {video_path}", None
            
            print(f"✅ Video created: {video_path}")
            
            # Step 7: Save to user history
            video_data = {
                "platform": platform,
                "duration": duration,
                "quality": quality,
                "command": command,
                "video_path": video_path,
                "scenes_count": len(script_plan['scenes']),
                "credit_cost": credit_cost
            }
            
            Database.add_video_to_history(user_email, video_data)
            
            # Step 8: Cleanup temp files
            self.cleanup()
            
            return True, f"Video generated successfully! Cost: {credit_cost} credits", video_path
            
        except Exception as e:
            # Refund credits on any error
            try:
                Database.add_credits(user_email, credit_cost)
            except:
                pass
            
            return False, f"Pipeline error: {str(e)}", None
    
    def get_generation_progress(self):
        """Get progress updates during generation"""
        return {
            "script": "📝 Generating script...",
            "images": "🖼️ Creating images...",
            "voiceover": "🎙️ Recording voiceover...",
            "editing": "🎬 Editing video...",
            "complete": "✅ Video ready!"
        }
    
    def cleanup(self):
        """Clean up temporary files after generation"""
        try:
            self.image_gen.cleanup_images()
            self.voice_gen.cleanup_audio()
        except:
            pass
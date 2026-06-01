# utils/gemini_ai.py

import google.generativeai as genai
import os
import json
import time

class GeminiAI:
    """Gemini AI Integration for Script & Scene Planning"""
    
    def __init__(self):
        # Get API key from secrets
        api_key = os.environ.get('GEMINI_API_KEY', '')
        if not api_key:
            raise Exception("Gemini API key not found in Secrets!")
        
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.0 Flash (fast and free tier available)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # System prompt for video director
        self.system_prompt = """
        Tu ek professional video editor aur director hai. Tera kaam hai user ke command se 
        detailed video plan banana.

        IMPORTANT RULES:
        1. Video me KOI BHI TEXT, CAPTIONS, ya SUBTITLES automatically ADD mat karo
        2. Sirf wahi features use karo jo user ne explicitly manga ho
        3. Agar user ne text/captions nahi manga — video BILKUL CLEAN honi chahiye
        4. Sirf images, voiceover, music aur effects add karo

        Tumhe JSON format me response dena hai. Format ye hoga:

        {
            "script": "Full voiceover script here...",
            "total_duration": 30,
            "platform": "YouTube",
            "style": "cinematic",
            "music_mood": "epic motivational",
            "scenes": [
                {
                    "scene_number": 1,
                    "duration": 5,
                    "image_prompt": "Detailed image description for AI generation",
                    "voice_text": "Text for this scene's voiceover",
                    "effect": "none or slow_zoom_in or slow_zoom_out or pan_left or pan_right",
                    "transition": "fade or dissolve or slide_left or none"
                }
            ]
        }

        Effects available (ONLY if user asks):
        - slow_zoom_in: Slow zoom in effect
        - slow_zoom_out: Slow zoom out effect  
        - pan_left: Pan left to right
        - pan_right: Pan right to left
        - none: No effect (default)

        Transitions available:
        - fade: Fade to black between scenes
        - dissolve: Cross dissolve
        - slide_left: Slide to left
        - none: Cut transition (default)

        IMPORTANT: 
        - image_prompt ENGLISH me likhna (AI image generation ke liye)
        - voice_text HINGLISH ya user ki language me likhna
        - Har scene 3-7 seconds ka hona chahiye
        - Total scenes = total_duration / avg_scene_duration
        """
    
    def generate_script(self, user_command, platform, duration):
        """Generate video script and scene plan from user command"""
        
        try:
            # Create prompt
            prompt = f"""
            User Command: {user_command}
            Platform: {platform}
            Duration: {duration} seconds
            
            Is command ke hisaab se detailed video plan banao.
            
            YAAD RAKHO:
            - Video me KOI TEXT ya CAPTIONS automatically add mat karna
            - Sirf user ne text manga ho tabhi add karna
            - Images, voiceover aur effects pe focus karo
            
            JSON format me response do. Sirf JSON, koi aur text mat likhna.
            """
            
            # Generate response
            response = self.model.generate_content(
                [self.system_prompt, prompt],
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'top_k': 40,
                    'max_output_tokens': 2048,
                }
            )
            
            # Parse JSON response
            response_text = response.text
            
            # Clean response (remove markdown code blocks if any)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            plan = json.loads(response_text)
            
            # Add user command to plan
            plan['user_command'] = user_command
            plan['platform'] = platform
            plan['total_duration'] = duration
            
            return True, plan
            
        except json.JSONDecodeError as e:
            return False, f"JSON parse error: {str(e)}. Response: {response_text[:200]}"
        except Exception as e:
            return False, f"Gemini API error: {str(e)}"
    
    def generate_image_prompt_variations(self, base_prompt, num_variations=3):
        """Generate variations of image prompts for better results"""
        
        try:
            prompt = f"""
            Generate {num_variations} variations of this image prompt for AI image generation.
            Make each variation slightly different but keep the same theme.
            
            Base prompt: {base_prompt}
            
            Return as JSON array of strings.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            variations = json.loads(response_text)
            return variations
            
        except:
            # If variation fails, return original prompt repeated
            return [base_prompt] * num_variations

# Test function
if __name__ == "__main__":
    ai = GeminiAI()
    success, result = ai.generate_script(
        "Create a 30 second motivational video about success",
        "YouTube",
        30
    )
    if success:
        print(json.dumps(result, indent=2))
    else:
        print("Error:", result)
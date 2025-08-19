import os
import random
import logging
import asyncio
from config import BARRY_RESPONSES

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

logger = logging.getLogger(__name__)

class BarryCharacter:
    """Barry the winch operator character implementation with Gemini AI integration"""
    
    def __init__(self):
        """Initialize Barry with Gemini client if available"""
        self.gemini_available = False
        self.client = None
        
        # Try to initialize Gemini client
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key and genai:
            try:
                self.client = genai.Client(api_key=gemini_key)
                self.gemini_available = True
                logger.info("Barry initialized with Gemini AI support")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")
                logger.info("Barry will use fallback responses")
        else:
            if not genai:
                logger.info("Gemini library not available - using fallback responses")
            else:
                logger.info("No Gemini API key found - using fallback responses")
    
    def get_system_prompt(self):
        """Get the system prompt that defines Barry's character"""
        return """You are Barry, a friendly British winch operator. Keep responses short and casual.

Respond in character as Barry:
- Use casual British expressions (Right then!, Blimey!, mate)
- Mention winch operations occasionally
- Be helpful and cheerful
- Keep responses to 1-2 sentences maximum"""

    async def get_gemini_response(self, message, author_name, user_id):
        """Get response from Gemini AI"""
        try:
            # Create Barry-specific prompt
            full_prompt = f"You are Barry, a cheerful British winch operator from the 5th Regiment of Foot aboard HMS Undaunted at San Sebastián. {author_name} said: '{message}'. Respond in Barry's character with 1-2 sentences, using British expressions and mentioning your work occasionally."

            if self.client and types:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model="gemini-1.5-flash",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=100
                    )
                )
            else:
                return None
            
            if response and response.candidates:
                # Extract text from the first candidate's content parts
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    text_parts = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
                    
                    if text_parts:
                        response_text = ''.join(text_parts).strip()
                        logger.info(f"Gemini response received: {response_text[:100]}...")
                        return response_text
                
                logger.warning(f"No text in response parts. Candidates: {response.candidates}")
                return None
            else:
                logger.warning(f"Empty response from Gemini. Response: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None
    
    def get_fallback_response(self, message, author_name):
        """Get a fallback response when Gemini is unavailable"""
        message_lower = message.lower()
        
        # Context-aware responses based on message content
        if any(word in message_lower for word in ['help', 'rescue', 'save', 'stuck', 'trapped']):
            responses = BARRY_RESPONSES['help']
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            responses = BARRY_RESPONSES['greetings']
        elif any(word in message_lower for word in ['platform', 'winch', 'lower', 'raise']):
            responses = BARRY_RESPONSES['platform']
        elif any(word in message_lower for word in ['thank', 'thanks', 'grateful']):
            responses = BARRY_RESPONSES['thanks']
        elif any(word in message_lower for word in ['scared', 'afraid', 'worried', 'nervous']):
            responses = BARRY_RESPONSES['encouragement']
        elif any(word in message_lower for word in ['zombie', 'zombies', 'infected', 'dead']):
            responses = BARRY_RESPONSES['danger']
        elif any(word in message_lower for word in ['bye', 'goodbye', 'farewell', 'leaving']):
            responses = BARRY_RESPONSES['farewell']
        else:
            responses = BARRY_RESPONSES['general']
        
        # Select random response and personalize it
        response = random.choice(responses)
        
        # Add author name reference naturally
        if '{author}' in response:
            response = response.replace('{author}', author_name)
        else:
            # Add author reference to some responses
            if random.random() < 0.3 and author_name:  # 30% chance
                response = f"{response} Right then, {author_name}!"
        
        # Add some Barry-style actions and personality occasionally
        actions = ["*adjusts winch controls*", "*checks platform status*", "*oils the gears*", "*maintains cheerful demeanor*"]
        if random.random() < 0.4:  # 40% chance to add an action
            action = random.choice(actions)
            if random.random() < 0.5:
                response = f"{action} {response}"
            else:
                response = f"{response} {action}"
        
        return response
    
    async def get_response(self, message, author_name, user_id):
        """Get Barry's response to a message"""
        # Clean the message (remove bot mentions)
        if user_id and user_id != "test_user":
            clean_message = message.replace(f'<@!{user_id}>', '').replace(f'<@{user_id}>', '').strip()
        else:
            clean_message = message.strip()
        if not clean_message:
            clean_message = "Hello Barry!"
        
        logger.info(f"Processing message: '{clean_message}' from {author_name}")
        
        # Try Gemini first if available
        if self.gemini_available and self.client:
            gemini_response = await self.get_gemini_response(clean_message, author_name, user_id)
            if gemini_response:
                return gemini_response
        
        # Fall back to predefined responses
        return self.get_fallback_response(clean_message, author_name)

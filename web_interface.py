from flask import Flask, render_template, jsonify
import os
import logging
from barry_character import BarryCharacter
from config import BARRY_INFO

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Initialize Barry character for web interface
    barry = BarryCharacter()
    
    @app.route('/')
    def index():
        """Main web interface page"""
        try:
            return render_template('index.html', barry_info=BARRY_INFO)
        except Exception as e:
            logger.error(f"Template error: {e}")
            # Return simple HTML if template missing
            return f"""
            <html><head><title>Barry Discord Bot</title></head>
            <body>
                <h1>Barry Discord Bot - Status</h1>
                <p>Discord Bot: {'✅ Configured' if os.getenv('DISCORD_BOT_TOKEN') else '❌ Missing Token'}</p>
                <p>Gemini AI: {'✅ Configured' if os.getenv('GEMINI_API_KEY') else '❌ Missing Key'}</p>
                <p>Status: Running on Render.com</p>
            </body></html>
            """
    
    @app.route('/api/status')
    def bot_status():
        """API endpoint to check bot status"""
        discord_token = os.getenv('DISCORD_BOT_TOKEN')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        status = {
            'discord_configured': bool(discord_token),
            'gemini_configured': bool(gemini_key),
            'gemini_available': barry.gemini_available,
            'character': BARRY_INFO
        }
        
        return jsonify(status)
    
    @app.route('/api/test-response')
    def test_response():
        """Test Barry's response system"""
        try:
            # Test fallback response system (sync)
            response = barry.get_fallback_response("Hello Barry!", "WebUser")
            
            return jsonify({
                'success': True,
                'response': response,
                'ai_powered': False,
                'note': 'Testing fallback response system'
            })
        except Exception as e:
            logger.error(f"Error testing response: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        try:
            return render_template('index.html', barry_info=BARRY_INFO), 404
        except:
            return "<h1>Barry Discord Bot</h1><p>Page not found</p>", 404
    
    return app

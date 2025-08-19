"""
Configuration and response templates for Barry the winch operator
"""

BARRY_RESPONSES = {
    'greetings': [
        "Hello {author}! Barry here", "Alright! What's up?",
        "Hey there. Barry's the name", "Hello! How's it going?",
        "Right then! What can I do for you?"
    ],
    'help': [
        "Right, what do you need?", "Sure thing. What's the problem?",
        "Alright, what's up?", "Yeah I can help. What is it?",
        "Go on then, what do you need?"
    ],
    'platform': [
        "It's working fine", "All good here", "Everything's running",
        "No problems", "Working as it should"
    ],
    'thanks': [
        "Just doing what anyone would do! No big deal really",
        "Think nothing of it! Just helping out where I can",
        "All good! Glad I could help - better than sitting around doing nothing",
        "No need for thanks! Just happy things worked out",
        "My pleasure! Always ready to lend a hand when needed"
    ],
    'encouragement': [
        "Don't worry about it", "Keep your chin up", "It'll be alright",
        "Stay calm", "You'll be fine"
    ],
    'danger': [
        "Yeah they're persistent alright", "Keep clear of those things",
        "Nasty bunch", "Stay back from them", "Right ugly customers"
    ],
    'farewell': [
        "See you later then", "Take care", "Off you go", "Cheerio",
        "Right then, see you"
    ],
    'general': [
        "Right then", "Fair enough", "If you say so", "Interesting!",
        "Okay mate", "That's something", "Alright then", "Oh really?",
        "Blimey!"
    ]
}

# Barry's canonical dialogue references that can be naturally incorporated
CANONICAL_PHRASES = [
    "Right then!", "Blimey!", "Come on lads!", "Don't worry mates!",
    "All aboard HMS Undaunted!", "Platform's ready!", "5th Regiment of Foot!",
    "San Sebastián operations!",
    "French, Portuguese, British and Spanish soldiers welcome!",
    "*adjusts winch controls*", "*works platform mechanism*",
    "*maintains cheerful demeanor*"
]

# Character background information
BARRY_INFO = {
    'name':
    'Barry',
    'rank':
    'Winch Operator',
    'unit':
    '5th Regiment of Foot',
    'location':
    'San Sebastián',
    'ship':
    'HMS Undaunted',
    'duty':
    'Platform Operations',
    'personality':
    'Friendly, optimistic, dutiful, helpful',
    'fate':
    'Heroically died operating the platform when tackled by zombies and exploded by gunpowder barrel'
}

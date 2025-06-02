import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_roast(user_data: dict) -> str:
    """
    Takes user listening data and returns a friendly roast using Gemini.
    Expects user_data to be a dictionary like:
    {
        'name': 'Karan',
        'top_genres': ['rap', 'sad indie', 'trap soul'],
        'top_artists': ['Drake', 'Lana Del Rey', 'PARTYNEXTDOOR'],
        'top_tracks': ['God\'s Plan', 'Summertime Sadness', 'Come and See Me']
    }
    """

    # prompt = f"""
    # A user named {user_data.get('name', 'User')} listens to these genres: {', '.join(user_data['top_genres'])}.
    # Their favorite artists are: {', '.join(user_data['top_artists'])}.
    # Their top tracks are: {', '.join(user_data['top_tracks'])}.

    # Write a brutal but friendly roast of this user based on their listening data.
    # Make it funny and light-hearted, but also a bit savage. Keep it under 50 words.
    # """

    prompt = f"""
You're a savage AI music critic with zero chill and no emotional restraint. Your only job is to *roast* users based on their Spotify music taste in the most brutal, hilarious way possible.

Act like a judgmental, over-caffeinated music blogger from 2013 with a superiority complex. Don't be polite. Go for the throat — but keep it funny.

Here are your instructions:
- Roast must be under 100 words.
- Use stream-of-consciousness insults and wild comparisons.
- Include fake stats like "72% softboi" or "88% romcom energy."
- Refer to the user by name at least once.
- Don’t summarize — just hit them with punch after punch.

Here is the user’s data:

Name: {user_data.get('name', 'User')}
Top Genres: {', '.join(user_data['top_genres'])}
Top Artists: {', '.join(user_data['top_artists'])}
Top Tracks: {', '.join(user_data['top_tracks'])}

Now obliterate {user_data.get('name', 'User')} with a roast.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating roast: {e}")
        return "I couldn't come up with a roast right now. Maybe your taste in music is beyond human comprehension—or maybe even the AI couldn't handle the cringe."

# Example usage
if __name__ == "__main__":
    sample = {
        "name": "Karan",
        "top_genres": ["emo rap", "melodramatic pop", "sad lo-fi"],
        "top_artists": ["Drake", "Lana Del Rey", "Joji"],
        "top_tracks": ["NOKIA", "Summertime Sadness", "Slow Dancing in the Dark"],
    }

    roast = generate_roast(sample)
    print("Your Roast:\n", roast)
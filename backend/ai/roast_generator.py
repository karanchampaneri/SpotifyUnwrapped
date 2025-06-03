import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#format user data into a prompt
#send that to the AI
#return a roast as a string

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_roast(user_data: dict) -> str:
    """
    Takes user listening data and returns a friendly rost using OpenAI.
    Expects user_data to be a dictionary like:
    {
        'top_genres': ['rap', 'sad indie', 'trap soul],
        'top_artists': ['Drake', 'Lana del Rey, 'PARTYNEXTDOOR']
        'top_tracks': ['God's Plan', 'Summertime Sadness', 'Come and See Me']
    }

    """

    prompt = f"""
    
    A user listens to these genres: {', '.join(user_data['top_genres'])}.
    Their favorite artists are: {', '.join(user_data['top_artists'])}.
    Their top tracks are: {', '.join(user_data['top_tracks'])}.

    write a brutal but friendly roast of this user based on their listening data.
    Make it funny and light-hearted, but also a bit savage. Keep it under 50 words.
    Make sure to use the user's name in the roast.
    Example: "Hey {user_data.get('name', 'User')}, your taste in music is so basic, even a Spotify algorithm could do better. But hey, at least you have good taste in bad music!"
    Make sure to use the user's name in the roast.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    # If the API call fails or returns an error, handle it gracefully
    except Exception as e:
        print(f"Error generating roast: {e}")
        return "I couldn't come up with a roast right now. Maybe your taste in music is beyond human comprehension  -- or maybe even the AI couldn't handle the cringe."
    


# Example usage:

if __name__ == "__main__":
    sample = {
        "top_genres": ["emo rap", "melodramatic pop", "sad lo-fi"],
        "top_artists": ["Drake", "Lana Del Rey", "Joji"],
        "top_tracks": ["NOKIA", "Summertime Sadness", "Slow Dancing in the Dark"],
    }

    roast = generate_roast(sample)
    print("Your Roast:\n", roast)
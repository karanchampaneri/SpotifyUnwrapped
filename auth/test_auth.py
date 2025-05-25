from spotify_auth import authenticate_user

sp = authenticate_user()
print(sp.current_user()['display_name'])
import pandas as pd
import requests
import json
import config

# Establish credentials
encoded_key=config.key
def client_credentials(encoded_key):
    headers = {
    'Authorization': 'Basic '+encoded_key,
    }

    data = {
      'grant_type': 'client_credentials'
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    try:
        return response.json()['access_token']
    except:
        print(response.json())
        return response.json()
access_token=client_credentials(encoded_key)

# Request input from user
message=str.lower(input('Enter message:'))

# Search for a query with offset (k)
def search_exact_track(q,n,k):
    # grab k searches, see if any match exactly
    # if not, re-iterate next k searches
    if (n/k)>7:
        # print('Too many iterations to find the track')
        return None
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+access_token,
    }

    params = (
        ('q', q),
        ('type', 'track'),
        ('market', 'US'),
        ('offset',n),
        ('limit',k)
    )
    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    tracks=response.json()
    total_n=tracks['tracks']['total']
    track_dict={str.lower(x['name']):x['external_urls']['spotify'] for x in list(tracks['tracks']['items'])}
    if q in track_dict:
#         print('Found track: '+q)
        return(track_dict[q])
    else:
        if n+k<total_n:
#             print('Must reiterate with new offset: '+str(n+k))
            return(search_exact_track(q,n+k,k))
        else:
#             print('No matching tracks for: '+q)
            return None

# Iteratively search for matching tracks and add to list
def left_chunker(word_array, stop_pos):
    if stop_pos==0:
#         print('Empty array')
        return None
    message=" ".join(word_array[:stop_pos])
#     print('Searching for: '+message)
    track=search_exact_track(message, 0, 50)
    if track is None:
#         print('Failed. Now will try: '+" ".join(word_array[:stop_pos-1]))
        return left_chunker(word_array,stop_pos-1)
    else:
#         Add to list
        playlist.append([track, message,word_array, stop_pos])
        word_array=word_array[stop_pos:]
        return left_chunker(word_array,len(word_array))

# Executing functions and print out playlist
word_array=message.split(" ")
stop_pos=len(word_array)
playlist=[]
left_chunker(word_array,stop_pos)

for i in range(len(playlist)):
    print(str(i+1)+". "+playlist[i][1]+'\n'+playlist[i][0]+'\n')
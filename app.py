import pandas as pd
import requests
import json
import config

# Request input from user
message=str.lower(input('Enter message:'))

encoded_key=config.key
def client_credentials(encoded_key):
    headers = {
    'Authorization': 'Basic '+encoded_key,
    }

    data = {
      'grant_type': 'client_credentials'
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
#     print(response.json())
#     {'access_token': 'BQCVHHb7qAYICBc8He7AJi-SfHKWHZZQWSJ0fdetTyXFISQZR-iTIt1Y2-33XYk-LqKT_0YqrJ4TCnlVZIQ', 
#      'token_type': 'Bearer', 'expires_in': 3600, 'scope': ''}
    try:
        return response.json()['access_token']
    except:
        print(response.json())
        return response.json()
    

access_token=client_credentials(encoded_key)



# offset=0
# limit=50

def search_exact_track(q,n,k):
    # grab all 50 searches, see if any match exactly
    # if not, re-iterate next 50 searches
    
#     print('Offset: '+str(n))
    # print(n/k)
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
#     if tracks['tracks']['total']==0:
#         print('No matching tracks for: '+q)
#         return None
    track_dict={str.lower(x['name']):x['external_urls']['spotify'] for x in list(tracks['tracks']['items'])}
    if q in track_dict:
#         print('Found track: '+q)
        return(track_dict[q])
    else:
        if n+k<total_n:
#             print('Must reiterate with new offset: '+str(n+k))
#             print(n)
#             print(k)
            return(search_exact_track(q,n+k,k))
        else:
#             print('No matching tracks for: '+q)
            return None







# Try full message
# Try chunking
# Try every individual word and build up on it

# [(word,position) for (word,position) in zip(word_array,range(len(word_array)))]

word_array=message.split(" ")
stop_pos=len(word_array)
def left_chunker(word_array, stop_pos):
    if stop_pos==0:
#         print('Empty array')
        return None
#     print('stop pos: '+str(stop_pos))
#     print('word array length: '+str(len(word_array)))
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


playlist=[]
left_chunker(word_array,stop_pos)

for i in range(len(playlist)):
    print(str(i+1)+". "+playlist[i][1]+'\n'+playlist[i][0]+'\n')
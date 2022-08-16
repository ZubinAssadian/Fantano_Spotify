# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:11:33 2020

@author: Zubin
"""

import spotipy
import spotipy.util as util
import Song_Extract



## Credentials Required for Spotify API ##

clientID = ''
clientSecret = ''
redirectUri = 'http://localhost:8888/callback'
scope = 'user-read-private user-read-email playlist-modify-public user-read-playback-state user-read-currently-playing'
username = ''
myList = []
songID = []

token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectUri)



## Playlist Initialization ##

if token:
    
    spotify = spotipy.Spotify(auth = token)
    
    playlistName = input('Enter Name for the Playlist: ')
    playlistDesc = input('Enter Description for the Playlist: ')
    spotify.user_playlist_create(username, playlistName, description = playlistDesc)



## Song List Extraction ##

    
    url = input('Enter Fantano List YT Page url: ')
    
    if url == 'https://www.youtube.com/watch?v=EyMX4lcKNPg':
        
        dummy = Song_Extract.TOP200.copy()
        
                
        myList = dummy
        
    else:
        
        myList = Song_Extract.YTdescExtract(url)



## Getting Selected Playlist ID ##

        
    playlistID = ''
    
    for playlist in spotify.current_user_playlists()['items']:
        
        if playlist['name'] == playlistName:
            
            playlistID = playlist['id']


            
## Removing Search unfriendly characters ##
## Playlists concerning Singles not Albums ##
           

    if playlistName.find('Albums') == -1 :
            
        for i in range(len(myList)):
            
            dash = myList[i].find('ft.')
            if dash != -1:
                
                myList[i] = myList[i][:dash - 1]
                
            if myList[i].find('&') != -1:
                
                myList[i] = myList[i].replace(myList[myList.find('&'):dash], '')



## Search for the songs through API ##

        
        for tracks in myList:
            
            print(tracks)
            Tracks = spotify.search(tracks, limit = 1)
            
            
            
## If track not found, search for text after dash ##


            if not Tracks['tracks']['items']:
                   
                pos = tracks.find('-')
                Tracks = spotify.search(tracks[pos + 2:], 1)
                ArtistName = tracks[: pos -1]
                
                
                
## If track still not found, continue ( not all tracks available on spotify) ##


                if not Tracks['tracks']['items'] or ArtistName.find(
                        Tracks['tracks']['items'][0]['name']) == -1:
                    continue
                
                
                
## Add trackID to list ##


            trackID = Tracks['tracks']['items'][0]['id']
            songID.append(trackID)
            
            
## Iterate through list to add tracks to selected playlist ##    


  
        if len(songID) > 100:
                
            chunks = [songID[x : x + 100] for x in range(0, len(songID), 100)]
                
            for chunk in chunks:
                    
                spotify.user_playlist_add_tracks(username, playlistID, chunk)
                    
        else:
                
                
            spotify.user_playlist_add_tracks(username, playlistID, songID)
                
            
            
## Playlists Concerning Albums ##     
## Search through API if album is there ##
 


    else:
            
        for albums in myList:
                
            Albums = spotify.search(albums, 1, 0, 'album')
            print(albums)
            if not Albums['albums']['items']:
                    
                pos = albums.find('-')
                Albums = spotify.search(albums[pos + 2:], 1, 0, 'album')
                ArtistName = albums[: pos -1]
                    
                    
                if not Albums['albums']['items'] or ArtistName.find(Albums['albums']['items'][0]['artists'][0]['name']) == -1:
                    continue
                    
                    
            albumID = Albums['albums']['items'][0]['id']
            album = spotify.album(albumID)
            
            
            
 ## Add trackIDs to list ##    

           
            for track in album['tracks']['items']:
                    
#                    spotify.user_playlist_add_tracks(username, playlistID, [track['id']])
#                    time.sleep(.5)
                    
                songID.append(track['id'])



            
  ## Add tracks to selected playlist ##

          
        if len(songID) > 100:
                
            chunks = [songID[x : x + 100] for x in range(0, len(songID), 100)]
                
            for chunk in chunks :
                    
                spotify.user_playlist_add_tracks(username, playlistID, chunk)
                
        else:
                
            spotify.user_playlist_add_tracks(username, playlistID, songID)
                    
                
                
                
                
               
                    
                
                    
                    
                
            
            
               
               
            
        
        
        
       
        
    
    
    
    
    
    
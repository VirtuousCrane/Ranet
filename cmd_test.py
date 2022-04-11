"""
THIS FILE IS FOR TESTING PURPOSES ONLY

"""


#from src.video_player import MediaChannelPlaylistParser, MediaChannel, MediaChannelList
from src.radio import RadioTracker
from src.video_player import MediaChannelShelf, HLSStation, FavoriteMediaChannelShelf
import csv

# radioChannels = RadioTracker().radio_stations_list

# with open('assets/all_media_channel.csv', mode='w', newline="") as csv_file:
#     myfieldnames = ['name','url']
#     csv_writer = csv.writer(csv_file, delimiter=',')

#     for channel in radioChannels:
#         try:
#             line = [channel.name, channel.url]
#             csv_writer.writerow(line)
#         except:
#             print(line)
#             print("Cannot write to file")

media_channel_list = MediaChannelShelf("assets/all_media_channel.csv")
print(media_channel_list.get_current_channel())
print(media_channel_list.get_next_channel())

channel = HLSStation("BBC - Sports", "BBC URL")
print(channel.name.lower().find(''))

search_media_channel = media_channel_list.get_channels_by_search('spo')
print("Searched media channels")
for channel in search_media_channel:
    print(channel)

favorite_channel_list = FavoriteMediaChannelShelf("assets/all_media_channel.csv")
# print("Printing all favorite channel")
# for fav_channel in favorite_channel_list.main_media_channels:
#     print(fav_channel)
print(favorite_channel_list.get_channels_by_search("sport"))
print(favorite_channel_list.is_media_channel_in_list(HLSStation("SomaFM Groove Salad","http://ice6.somafm.com/groovesalad-128-aac")))
print(favorite_channel_list.get_channel_by_search_index("sport", 0))
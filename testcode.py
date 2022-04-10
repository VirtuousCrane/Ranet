from src.video_player import MediaChannelShelf, FavoriteMediaChannelShelf, HLSPlaylistParser
import csv

shelf = MediaChannelShelf("assets/all_radio_channel.csv")
for channel in shelf.getChannelsBySearch("sport"):
    print(channel)

fav_shelf = FavoriteMediaChannelShelf("assets/all_radio_channel.csv")
print(fav_shelf.isMediaChannelInList(shelf.getChannelByIndex(1)))

tv_playlist_parser = HLSPlaylistParser("assets/iptv/th.m3u")
tv_channels = tv_playlist_parser.get_list()
# correct_url_channel = []
# for channel in tv_channels:
#     correct_url_channel.append(channel)
#     if channel.name == "TRT World (720p) [Not 24/7]":
#         break

channels_with_correct_url = []
with open("assets/all_tv_channel.csv","w",newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    for channel in tv_channels:
        if not "#EXTVLCOPT" in channel.url:
            channels_with_correct_url.append(channel)
            print(channel)
            csv_writer.writerow([channel.name,channel.url])



    
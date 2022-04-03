from src.radio import RadioStation, RadioTracker
import csv


radioChannels = RadioTracker().radio_stations_list
with open('assets/all_media_channel.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')

    for channel in radioChannels:
        try:
            csv_writer.writerow([channel.name,channel.url])
        except:
            print("Cannot write into csv")
            print(channel)



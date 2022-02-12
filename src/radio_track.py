import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction
from radio import RadioStation

tree = ET.parse("assets/gnome-internet-radio-locator.xml")
root = tree.getroot()

# Get "version" attribute?
my_version = root.get('version')
print("Version is " + my_version)

# 
print("tree is " + str(type(tree)))
print("root is " + str(type(root)))

# Get all station info
for element in tree.findall('station'):
    print(element.get("name"), element.find("stream").get("uri"))

print("end of program")

class RadioTracker(object):
    # This class will handle list radio stations
    
    RADIO_STATIONS_XML_FILE_PATH = "assets/gnome-internet-radio-locator.xml"

    def __init__(self):
        self.radio_stations_list = []
        self.current_index = 0

        self.__initialize_radio_stations_list()
    
    
    def __initialize_radio_stations_list(self):
        # This method will generate the radio stations from XML file and populate the radio stations list
        tree = ET.parse(self.RADIO_STATIONS_XML_FILE_PATH)

        for station in tree.findall('station'):
            station_name = station.get("name")
            station_url = station.find("stream").get("uri")  # IDK why but the "url" is listed as "uri"
            station_type = station.find("stream").get("codec") # The "codec" seems to be the station type
            
            radio_station = RadioStation(station_name, station_url, station_type)
            self.radio_stations_list.append(radio_station)

    def increment_index(self):
        self.current_index += 1
        self.current_index = self.current_index % len(self.radio_stations_list)

    def decrement_index(self):
        self.current_index -= 1
        self.current_index = self.current_index % len(self.radio_stations_list)

    def get_current_station(self): 
        return self.radio_stations_list[self.current_index]


        
        
        
    

        


radio_tracker = RadioTracker()
print(radio_tracker.get_current_station().name)
radio_tracker.increment_index()
print(radio_tracker.get_current_station().name)
radio_tracker.increment_index()
print(radio_tracker.get_current_station().name)
radio_tracker.decrement_index()
print(radio_tracker.get_current_station().name)
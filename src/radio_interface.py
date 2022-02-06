

class RadioInterface(object):
    def __init__(self):
        pass
        
    def switch_on(self):
        print("Playing radio")

    def switch_off(self):
        print("Turning off the radio")
        
    def next_channel(self):
        print("Switching to next possible radio channel")
    
    def previous_channel(self):
        print("Switching to previous possible radio channel")

    def display_current_channel(self):
        print("Display info of current radio channel")
        
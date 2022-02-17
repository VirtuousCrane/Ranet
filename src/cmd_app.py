from radio import Radio
from testcode import MyRadioPlayer, RadioStation, MyRadio

class RadioCMDApp(object):
    def __init__(self):
        self.radio = MyRadio()
        
    def start(self):
        userInput = -1
        while(userInput != 0):
            print("Radio interface")
            print("1. Switch on")
            print("2. Switch off")
            print("3. Next channel")
            print("4. Previous channel")
            print("5. Display current channel")
            print("6. Clicked exit button")
            print("0. Exit")
            
            try:
                userInput = input("Select option: ")
                userInput = int(userInput)
            except:
                print("Invalid input, exitting program")
                userInput = 0
            
            if(userInput == 0):
                print("Exitting program")
                self.radio.stop()
            elif(userInput == 1):
                self.radio.play()
            elif(userInput == 2):
                self.radio.stop()
            elif(userInput == 3):
                self.radio.next_channel()
            elif(userInput == 4):
                self.radio.previous_channel()
            elif(userInput == 5):
                self.radio.display_current_channel()
            else:
                print("Option not available/not implemented")


app = RadioCMDApp()
app.start()
        
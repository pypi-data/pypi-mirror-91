#import sys,os
#sys.path.append(os.getcwd())

#from pysignalclirestapi import SignalCliRestApi
import api


a = api.SignalCliRestApi("http://127.0.0.1:8080", "+4368181186254") #"+4368181186254")
#a = api.SignalCliRestApi("http://192.168.1.20:8080", "+4368120376269")
#print(a.receive())
print(a.create_group("bla", ["+436802057104"]))
#a.update_profile("test", filename="/tmp/hero_screenshot.png")
#print(a.list_groups())
#a.send_message("--test", recipients=["+436802057104"], filenames=["/tmp/hero_screenshot.png", "/tmp/hero_screenshot.png"])
#a.send_message("test", recipients=["+436802057104"])

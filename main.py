from raritan.rpc import Agent, pdumodel, firmware
import re
import time
import pandas as pd

excel_file_path = r'\\10.91.22.161\AudioDSPshare\fkubawsx\EXCEL\platformList.xlsx'
df = pd.read_excel(excel_file_path)
ctrlr_values = df['Ctrlr']
off_array = []

raritan_ip = ["10.237.146.7", "10.237.147.15", "10.237.147.13", "10.237.147.11", "10.237.147.16", "10.237.147.4", "10.237.147.9" , "10.237.147.147", "10.237.147.13", "10.237.147.7"]

def raritansAv():
    print("Raritan PDU's:\n")
    print("1. DR-01 : 10.237.146.7\n")
    print("2. DR-02 : 10.237.147.15\n")
    print("3. DR-03: 10.237.147.13\n")
    print("4. DR-04: 10.237.147.11\n")
    print("5. DR-05: 10.237.147.16\n")
    print("6. DR-06: 10.237.147.4\n")
    print("7. DR-06: 10.237.147.9\n")
    print("8. DR-07: 10.237.147.147\n")
    print("9. DR-08: 10.237.147.13\n")
    print("10. DR-10: 10.237.147.7\n")

def showHelp():
    print("on:\n Choose outlet and turn it on\n syntax: [on] <outlet_number>\n")
    print("turn_all: \n Turn on all outlets among all PDU's with offline status\n")
    print("off:\n Choose outlet and turn it off\n syntax: [off] <outlet_number>\n")
    print("restart: \n Choose outlet and restart it\n syntax: [restart] <outlet_number>\n")
    print("show_off: \n Show all outlets with off status\n syntax [show all] \n")
    print("show: \n Show status of outlets in current raritan\n syntax [show]\n")
    print("switch: \n Switch to other PDU\n [switch] <raritan_nr> or <raritan_ip>\n")
    print("close: \n Close program\n syntax [close]\n")
    print("exit: \n Return to main menu \n syntax [exit]\n")

def translateOutletsToHostnames(name):
    name = name[4:]
    for value in ctrlr_values:
        if value == name:
            return df.loc[df['Ctrlr'] == value, 'Name'].iloc[0]

def showAllOffOutlets():
    off_array.clear()
    for raritan in raritan_ip:
        pdu_user = "admin"
        pdu_pass = "raritan"
        pdu_agent = Agent("https", raritan, pdu_user, pdu_pass)
        pdu = pdumodel.Pdu("/model/pdu/0", pdu_agent)
        outlets = pdu.getOutlets()
        i = 0
        for outlet in outlets:
            if (i < 9):
                outlet_currentState = outlet.getState().ledState.red
                if outlet_currentState == False:
                    name = outlet.getSettings().name
                    hostname = translateOutletsToHostnames(name)
                    print("Raritan number: DR-", raritan_ip.index(raritan) + 1, " - ", raritan, ":")
                    print(hostname, " Status: OFF")
                    i = i + 1
                    off_array.append([raritan_ip.index(raritan), int(outlet.getMetaData().label)])
    print("Finished\n")
    print(off_array)

def turnOnAllOffOutlets():
   print("Turning on all off outlets\n :")
   connected_raritan = None
   if len(off_array) == 0:
       showAllOffOutlets()
       for inner_array in off_array:
           if connected_raritan != inner_array[0]:
            connected_raritan = raritan_ip[inner_array[0]]
            pdu_user = "admin"
            pdu_pass = "raritan"
            pdu_agent = Agent("https", connected_raritan, pdu_user, pdu_pass)
            pdu = pdumodel.Pdu("/model/pdu/0", pdu_agent)
            outlets = pdu.getOutlets()
           for outlet in outlets:
               outlet_nr = outlet.getMetaData().label
               if int(outlet_nr) == inner_array[1]:
                    print("Turned on ", raritan_ip[inner_array[0]], " - ", raritan_ip[inner_array[0]], " outlet nr. : ", outlet.getMetaData().label)
                    outlet.setPowerState(pdumodel.Outlet.PowerState.PS_ON)
   else:
       for inner_array in off_array:
           pdu_user = "admin"
           pdu_pass = "raritan"
           pdu_agent = Agent("https", raritan_ip[inner_array[0]], pdu_user, pdu_pass)
           pdu = pdumodel.Pdu("/model/pdu/0", pdu_agent)
           outlets = pdu.getOutlets()
           for outlet in outlets:
               outlet_nr = outlet.getMetaData().label
               if int(outlet_nr)== inner_array[1]:
                   print("Turned on ", raritan_ip[inner_array[0]], " - ", raritan_ip[inner_array[0]],
                         " outlet nr. : ", outlet.getMetaData().label)
                   outlet.setPowerState(pdumodel.Outlet.PowerState.PS_ON)
   print("Finished\n")
   off_array.clear()

def raritanMenu(outlets, pdu):
    print("See help for more options \n")
    while (True):
        syntax_pattern = r"^(restart|on|off|help|show_off|turn_all|close|switch|show|exit|show_pdus)(\s+\d+)?$"
        choosen_outlet = input("Syntax: [restart / on / off] outlet_number:\n")
        if re.match(syntax_pattern, choosen_outlet):
            action = choosen_outlet.split()[0]
            if len(choosen_outlet.split()) > 1:
                outlet_number = int(choosen_outlet.split()[1])
            else:
                outlet_number = None
            if action == "restart":
                print("Perform restart action for outlet", outlet_number)
                outlets[outlet_number].setPowerState(pdumodel.Outlet.PowerState.PS_OFF)
                time.sleep(10)
                outlets[outlet_number].setPowerState(pdumodel.Outlet.PowerState.PS_ON)
            elif action == "on":
                print("Perform on action for outlet", outlet_number)
                outlets[outlet_number].setPowerState(pdumodel.Outlet.PowerState.PS_ON)
            elif action == "off":
                print("Perform off action for outlet", outlet_number)
                outlets[outlet_number].setPowerState(pdumodel.Outlet.PowerState.PS_OFF)
            elif action == "help":
               showHelp()
            elif action == "show_off":
                showAllOffOutlets()
            elif action == "switch":
                switchRaritanPdu();
            elif action == "close":
                print("Exiting program...")
                exit(0)
            elif action == "show":
                GetOutletStatus(pdu)
            elif action == "turn_all":
                turnOnAllOffOutlets()
            elif action == "show_pdus":
                raritansAv()
            elif action == "exit":
                break
            else:
                print("Invalid action")
        else:
            print("Invalid syntax")

def GetOutletStatus(pdu):
    print()
    i = 0
    outlets = pdu.getOutlets()
    for outlet in outlets:
        if(i < 9):
            name = outlet.getSettings().name
            hostname = translateOutletsToHostnames(name)
            outlet_currentState = outlet.getState().ledState.red
            if outlet_currentState == False:
                print(outlet.getMetaData().label, ": ", hostname, " Status: OFF")
                i = i + 1
            else:
                print(outlet.getMetaData().label, ": ", hostname, " Status: ON")
                i = i + 1
    raritanMenu(outlets, pdu)

def switchRaritanPdu():
    print("Switch current raritan to:\n")
    raritansAv()
    pdu_nr = input("Choose raritan (IP address or by number):\n")

    if pdu_nr.lower().startswith("switch"):
        # Extract IP address from the input
        match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", pdu_nr)
        if match:
            pdu_ip = match.group(0)
        else:
            print("Invalid IP address")
            return
    elif pdu_nr.isdigit() and 1 <= int(pdu_nr) <= len(raritan_ip):
        pdu_ip = raritan_ip[int(pdu_nr) - 1]
    else:
        print("Invalid input")
        return

    print("----------------------------------------------")
    pdu_user = "admin"
    pdu_pass = "raritan"
    pdu_agent = Agent("https", pdu_ip, pdu_user, pdu_pass)
    pdu = pdumodel.Pdu("/model/pdu/0", pdu_agent)
    GetOutletStatus(pdu)


def main():
    print(r""" 
██████╗░░█████╗░██████╗░██╗████████╗░█████╗░███╗░░██╗  ██╗░░██╗██╗██╗░░░░░██╗░░░░░███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██╔══██╗████╗░██║  ██║░██╔╝██║██║░░░░░██║░░░░░██╔════╝██╔══██╗
██████╔╝███████║██████╔╝██║░░░██║░░░███████║██╔██╗██║  █████═╝░██║██║░░░░░██║░░░░░█████╗░░██████╔╝
██╔══██╗██╔══██║██╔══██╗██║░░░██║░░░██╔══██║██║╚████║  ██╔═██╗░██║██║░░░░░██║░░░░░██╔══╝░░██╔══██╗
██║░░██║██║░░██║██║░░██║██║░░░██║░░░██║░░██║██║░╚███║  ██║░╚██╗██║███████╗███████╗███████╗██║░░██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝  ╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝  """)
    raritansAv()
    print("See help for options\n")
    while(True):
        print("[connect] <raritan_addr> / [show_off] / [turn_all]\n")
        user_input = input("")
        syntax_pattern = r"^(connect\s+\S+|show_off|turn_all|close|help)$"
        if re.match(syntax_pattern, user_input):
            if user_input.startswith("connect"):
                pdu_ip = user_input.split()[1]
                pdu_user = "admin"
                pdu_pass = "raritan"
                pdu_agent = Agent("https", pdu_ip, pdu_user, pdu_pass)
                pdu = pdumodel.Pdu("/model/pdu/0", pdu_agent)
                GetOutletStatus(pdu)
            elif user_input == "show_off":
                print("Performing action to show 'off' outlets")
                showAllOffOutlets()
            elif user_input == "turn_all":
                turnOnAllOffOutlets()
            elif user_input == "close":
                print("Closing program")
                exit(0)
            elif user_input == "help":
                showHelp()
        else:
            print("Invalid syntax")


main()



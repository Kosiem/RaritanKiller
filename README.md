# RaritanKiller

A python-developed application for managing outlets in a Raritan PDU, using the Raritan RPC library dedicated to this.
Allows you to connect to a given PDU, and enable, disable and restart its outlets.
It also offers options to check among all PDUs for outlets that are turned off and to turn them on automatically.
Use of the program is possible via commands (such a custom CLI). To see the commands use help.

The application will be developed in the future, e.g. to allow checking statistics on power consumption of a given outlet.

on:
 Choose outlet and turn it on
 syntax: [on] <outlet_number>

turn_all: 
 Turn on all outlets among all PDU's with offline status

off:
 Choose outlet and turn it off
 syntax: [off] <outlet_number>

restart: 
 Choose outlet and restart it
 syntax: [restart] <outlet_number>

show_off: 
 Show all outlets with off status
 syntax [show all] <raritan_ip> (if raritan ip is not given, it will show all matched outlets among all PDU's)

show: 
 Show status of outlets in current raritan
 syntax [show]

switch: 
 Switch to other PDU
 [switch] <raritan_nr> or <raritan_ip>

close: 
 Close program
 syntax [close]

exit: 
 Return to main menu 
 syntax [exit]

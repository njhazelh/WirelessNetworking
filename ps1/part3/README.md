PS1 PROBLEM 3
-------------
done by nick jones and phaelyn kotuby

# TODO: NICK PLEASE ADD STUFF ON YOUR SCRIPT

### IDENTIFYING PEOPLE IN A ROOM
To try to come up with a way to find people in rooms simply with a fixed-spot 
laptop, I placed my laptop in a room (~25ft away from the access point, separated 
by a wall), exited, and walked around the same floor of my house to see if 
the RSSI values of nearby access points would be impaced significantly enough 
for me to be able to track my progress. First, take a look at the output of 
listen_all_rooms.lua (the same script from problem 1, run the same way) in the 
file all_rooms_record.csv. Here is a diagram of where I went:

@ = access point SSID; all APs other than kotuby in other buildings
R = room

		 N
		W E
						  +----+
		 S    +----+      | R0 |    +----+
			  | R1 |   |---, --+----| R3 |
			  +-, -+---| ___________,----+                   @patnetwork1 
	 @kotuby  |________| 
	

				@Donna

The laptop stayed fixed at R0; the capture begins with me leaving R0, walking 
into and out of R1, walking into and out of R3, and returning to R0 where the 
capture ends.

In an ideal setting, the access points would be much closer -- Donna and 
patnetwork1 are both in buildings completely separate from mine -- and I 
would therefore be able to use changes in the dBm of these APs, in conjunction 
with kotuby's, to triangulate people's locations in relation to the laptop. The 
higher the dBm, the farther away from an AP (or less directly in the line of sight)
a person must be. However, as you can tell from the capture, variances in the dBm
were miniscule at best -- kotuby's did go down as I approached R1, but there are
no real differences as I pass/enter R0 and R3. Other access points are simply too 
far away for me to make a large difference, as they're already passing through 
several walls and a lot of air. Finally, while I had multiple other SSIDs show 
up in the capture, I'm not aware of where they are, as I don't manage them, so 
I was unable to use any data to triangulate my location!

In general, I see why this could be a potential security threat in a location 
where access points are many, close between, and their locations known. It would 
be very easy to put a computer into monitor mode and watch the different RSSI 
levels change, giving you at least a general idea of what rooms may or may not 
have people in them. 

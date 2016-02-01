# Problem 3
Done by: Nick Jones and Phaelyn Kotuby

## Identifying a Room
As you move from room to room, the distance between you and a specific wireless
access point changes and obstacles may block signal.  As such, each room has
a specific fingerprint of the signal strengths that are seen while in that
room.  Unfortunately, identifying the patterns in this information is not easy.
Just by looking at the data, it is not possible to tell if a datapoint is from
one room or another.  Therefore, to solve this problem, we utilized the power
of machine learning.

The algorithm we chose was the Perceptron learning algorithm.  This algorithm
is a classifier that attempts to fit lines to a set of data such that
datapoints for a specific cluster fall into a unique region in the
multi-dimensional dataset.  We considered using Naive Bayesian Networks, but
Perceptron was determined to be a more powerful algorithm with little downside
in terms of implementation, since we were using scikit-learn libraries that
made things easier.

In the process of getting our classifier working, the results went through
several stages.  First, the algorithm chose only one room for all outputs.
we believed this to be due to several problems. First, the data we were feeding
in was not randomized, so the model was not training evenly.  Next, the data
being passed in was not sufficiently different.  We were keeping around old
access points, and failing to generate enough variation in the data.

Once we fixed some of these problems, we reached a point where the algorithm
chose from several rooms, but did so randomly (23% accuracy over 4 rooms).
At this point it was determined that we didn't have enough data, so we focused
again on getting more diverse data, and then we ran it for 10 minutes rather
than the previous minute or so.

In the end, we were able to accurately identify rooms using previously
generated fingerprints.  Within a second of entering a fingerprinted room,
we saw that the algorithm would correctly idenfity the location.  As we
moved from room to room, the data successfully updated in a consistent and
stable manner.

### Running the room identifier
To run this code, you must install scikit-learn, numpy, wireshark 2, lua 5.2,
and python3.

First start a wireless access point in monitor mode.  See `start_monitor.bash`
in the project root or use something like airmon-ng or kismet.  If you are
on OSX, look up airport.

Next run
```bash
./run_fingerprint.bash <interface> <room_name>
```
for each room you want to identify.  This will generate fingerprint files in
the fingerprint directory of part3.  Each fingerprint will take 10 minutes to
generate sufficient data to train with.  It may be possible to get better
results with less, but attempts results may vary.

Next run
```
./guess_room <interface>
```
This will parse the fingerprint files, train the model, and start a guesser
that will attempt to identify your location as you move from room to room.

To forget a room, just delete the fingerprint file in the fingerprints
directory.

## Identifying People in a Room
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

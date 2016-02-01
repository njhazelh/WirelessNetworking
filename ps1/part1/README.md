# Part 1
Problem 1 focused on getting 802.11 packet information by putting a wireless
card in monitor mode and catching the packets with wireshark.

The output of this problem are several scripts to catch packets and use the
information to generate a chart of access point strengths.  Also included
are a picture of a chart generated, a screenshot of wireshark with beacon
packets displaying, and a csv of packets stored from the script.

## Running
To run the code, first put your wireless card into monitor mode.  If you are
on linux, the start_monitor.bash script in the project root, should help you
do this.

Next start wireshark using
```bash
wireshark -i <interface> -X lua_script:record_beacons.lua -k
```
In the top menu, click "tools" and select "Record Beacons".  If everthing
is working, you should see access point information showing in the window
that pops up.

Next, close wireshark and run
```bash
./channel_chart.py < beacon_record.csv
```

This will generate a png of the local wireless networks.

*There is also script that does all this in one line*
Run
```bash
./make_channel_chart.bash <interface>
```
Note: This script doesn't put your wireless care in monitor mode, so you
will still need to do that first.

## Files
- artifacts/: A collection of artifacts generated in previous tests.
- channel_chart.py: A python script to generate a chart of ap channels from
the output of record_beacons*.lua scripts
- record_beacons.lua: A lua script to use with wireshark that generates a csv
of ap information
- record_beacons_tshark.lua: A lua script to use with tshark that prints the
same info as record_beacons.lua to stdout.
- make_channel_chart.bash: A bash script that uses record_beacons_tshark.lua
to generate a png of nearby access points.

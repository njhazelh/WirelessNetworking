PS1 PROBLEM 2
-------------
done by phaelyn kotuby with nick jones' code from ps1 problem 1 as starter code

### HOW TO RUN
To run packet_count.lua, first edit the filter at the top of the file to reflect 
the MAC address of the device that will be streaming data from the AP. Then, run:
	wireshark -X lua_script:packet_count.lua
Select your monitor, click Tools > Packet Count, and watch the average packets
per second for that MAC address roll by. When you're ready to stop recording, 
click "close"; your data will be in rssi_packets.csv.

To output the histograms seen in averages_histogram_*.png, run the above, then:
	python chart_averages.py < rssi_packets.csv
You'll need Python 3 and matplotlib.  

### INFO
The data for the RSSI-to-LoS graph was gathered manually by walking from the 
closest to farthest locations where the access point was still within my line of 
sight. I took measurements at critical points (doorways, slight corners), so this
is why the measurements are not a uniform one-per-x-feet. Because I fixed my laptop 
at each point, the dBm values stayed constant for the time I took to check the 
distance, so only one dBm value per marking was put in the Excel file. 

Variances between signal strength in individual csv's and the LoS data can likely 
be chalked up to interference of some kind -- about an hour passed between when 
I made the two sets of observations, people having entered the house and turned 
on electronics in the meantime, which accounts for the (rather uniformly-) lower 
dBm values in the data used for the histograms. 

A different YouTube video was streamed for each set of observations in the hopes 
that I could avoid any kind of caching/buffering mechanisms that my device would 
usually employ.
# PS3: Problem 4: Create RX/TX
This problem involved exchanging random data using two HackRFs.

## Inventory:
- images/* : Images of our results.
- prob4_rx_output : output from the receiver (random data)
- prob4_rx.grc : The receiver flowchart
- prob4_tx.grc : The transmitter flowchart
- pskrx.py : The generated receiver code
- psktx.py : The generated transmitter code
- README.md : This file

## Running code
To run the code open the flowcharts in gnuradio-companion or run the
generated scripts.  For this to work, you will need to HackRFs.

You will probably need to set the serial numbers for your HackRFs in the
flowcharts.  To get this information, run `hackrf_info`.  Plug it into
the device_id field in the osmocom source and sink blocks in the flowcharts.

You may run into an issue where transmitter and receiver refuse to run on the
intended HackRFs and information doesn't flow over the connection.  We fixed
this by disconnecting one of the HackRFs, and starting the receiver on the
other one.  We then connected the second HackRF and started the transmitter
by setting the serial number.

# Problem Set 3: HackRF One
**Nick Jones, Phaelyn Kotuby**

The purpose of this problem set was to work with the HackRF ONe to send
and receive wireless signals and interact with signal encoding.

## Problem 1: SDR Platform Setup
Problem 1 involved the setup process of the HackRF One and associated tools.
Overall, this part was not very complicated.  Other than some minor issues resolving dependencies, the installation process was relatively straight-forward.

To confirm that we had connected the HackRF One correctly, we ran
`hackrf_info` which responsed with information about the attached HackRF such
as the serial number, ...

After this we checked that we could interact with the HackRF by running osmocom_fft from the gr-osmosdr module.  We found a 5 GHz wifi channel and saw activity.

![Wifi Channel](prob1/wifi_channel.png)

## Problem 2: Building FM Radio Receiver 
Part 2 involved creating a FM radio receiver and a tool to play recorded audio at different speeds.



## Problem 3: BPSK/QPSK Transmission Simulation
...

## Problem 4: Real Transmission using HackRF
...

## Conclusion
...

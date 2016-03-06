# Problem Set 3: HackRF One
**Nick Jones, Phaelyn Kotuby**

The purpose of this problem set was to work with the HackRF ONe to send
and receive wireless signals and interact with signal encoding.

## Problem 1: SDR Platform Setup
Problem 1 involved the setup process of the HackRF One and associated tools.
Overall, this part was not very complicated.  Other than some minor issues
resolving dependencies, the installation process was relatively
straight-forward.

To confirm that we had connected the HackRF One correctly, we ran
`hackrf_info` which responsed with information about the attached HackRF such
as the serial number, ...

After this we checked that we could interact with the HackRF by running
osmocom_fft from the gr-osmosdr module.  We found a 2.4 GHz wifi channel
and saw activity.

![Wifi Channel](prob1/wifi_channel.png)

## Problem 2: Building FM Radio Receiver 
Part 2 involved creating a FM radio receiver and a tool to play recorded
audio at different speeds.

We encountered a few problems with this part.  Although we were eventually
able to find some FM radio stations, it was hard to identify them by looking
at the frequency chart.  Since the antenna we were using was pretty small, this
may have been the problem.  Increasing the RF gain in software seemed like it
resulted in slightly better signals, but nothing too significant.

![Frequency Chart](prob2/images/freq_chart.png)

We also encountered issues with audio underrun.  Because we were running
the environment in a virtual machine, this resulted in issues with the
audio sink output.  Although we proccessed the FM signal correctly,
the audio was clipped and warped.  At first we thought that this was some
kind of proccessing issue, but after dumping the audio to a wav file and
playing it back, we realized that the signal was fine.  According to the
GNU radio-companion documention, there is no simple solution to this
problem.  It recomended a quick hack of supplying information to the
audio sink at a slightly faster rate than it expects, but this did not
seem to work when we tried.


## Problem 3: BPSK/QPSK Transmission Simulation
...

## Problem 4: Real Transmission using HackRF
Problem 4 involved creating a wireless transmitter and receiver and using
them to transfer a set of random data.



## Conclusion
...

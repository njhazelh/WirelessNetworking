-- A script to record and display 802.11 beacon RSSI on different channels

local beacons = {}
local tap = Listener.new()

function tap.packet(pinfo, tvb)
    print("Got a packet")
end

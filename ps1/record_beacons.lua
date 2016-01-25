-- A script to record and display 802.11 beacon RSSI on different channels

local function beacon_recorder()
    local tw = TextWindow.new("Beacon Catcher")

    local beacons = {}

    local tap = Listener.new()

    function remove()
        tap:remove()
    end

    tw:set_atclose(remove)

    function tap.packet(pinfo, tvb)
        print("Got a packet")
    end
end

beacon_recorder()

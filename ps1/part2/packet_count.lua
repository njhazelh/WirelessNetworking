-- A script to record and display packets per second with RSSI on an 802.11 AP
-- to get the unix time
require "os"

local table = require("table")
-- filter by data from my phone's MAC address
-- TODO: change this to the MAC address you want to track
local filter = 'wlan.da == 64:bc:0c:42:a7:59'

-- fields of possible interest
local ssid_f = Field.new("wlan_mgt.ssid")
local channel_f = Field.new("wlan_radio.channel")
local dbm_f = Field.new("wlan_radio.signal_dbm")
local bssid_f = Field.new("wlan.bssid")
local frequency_f = Field.new("wlan_radio.frequency")
local time_f = Field.new("frame.time_epoch")
-- used for calculating average packets/sec
local packets = 0
local start_time = os.time()
Point = {}

-- a single data point
function Point:new(bssid, ssid, dbm, channel, frequency, cur_avg)
	obj = {
		channel = tostring(channel),
		ssid = tostring(ssid),
		dbm = tostring(dbm),
		frequency = tostring(frequency),
		cur_avg = tostring(cur_avg)
	}
	self.__index = self
	return setmetatable(obj, self)
end

-- to print into the csv
function Point:__tostring()
	return  self.channel .. "\t" ..
		self.dbm .. "\t" ..
		self.frequency .. "\t" ..
		self.cur_avg .. "\n"
end

-- actually process a packet when it comes in
local function packet_rate()
	local beacons = {}
	local tw = TextWindow.new("Packet Rate")
	local tap = Listener.new("radiotap", filter)
	local file = io.open("rssi_packets.csv", "w")

	-- apply the MAC address filter from earlier
	set_filter(filter)
	apply_filter()

	function remove()
		tap:remove()
		file.close()
	end

	tw:set_atclose(remove)

	-- run every time a packet is taken in
	function tap.packet(pinfo, tvb, userdata)
		-- get this packet's fields
		local ssid = ssid_f()
		local channel = channel_f()
		local dbm = dbm_f()
		local bssid = bssid_f()
		local frequency = frequency_f()
		-- add 1 to the number of packets found this second
		packets = packets + 1
		local time = tostring(time_f())
		-- get the running average of packets this second
		local cur_avg = packets / (tonumber(time) - start_time)
		-- and create a data point from that
		local p = Point:new(bssid, ssid, dbm, channel, frequency, cur_avg)
		
		-- Add to GUI log
		table.insert(beacons, p)

		file:write(tostring(p))
	end

	-- print in the Lua tool GUI box
	function tap.draw(t)
		tw:clear()
		tw:append("Channel\tdBm\tFreq.\tAvg. Packets/sec\n")
		for key, b in pairs(beacons) do
			tw:append(tostring(b))
		end
	end

	-- run after a packet has been processed
	function tap.reset()
		tw:clear()
		beacons = {}
		-- if a second has passed, restart the average counter
		if tonumber(time) - start_time >= 1 then 
			start_time = tonumber(time)
		end
	end
end

register_menu("Packet Rate", packet_rate, MENU_TOOLS_UNSORTED)

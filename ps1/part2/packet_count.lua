-- A script to record and display packets per second with RSSI on an 802.11 AP
require "os"

local table = require("table")
local MAC_ADDR = '64:bc:0c:42:a7:59'
-- TODO: parameterize
local filter = 'wlan.da == 64:bc:0c:42:a7:59'

local ssid_f = Field.new("wlan_mgt.ssid")
local channel_f = Field.new("wlan_radio.channel")
local dbm_f = Field.new("wlan_radio.signal_dbm")
local bssid_f = Field.new("wlan.bssid")
local frequency_f = Field.new("wlan_radio.frequency")
local time_f = Field.new("frame.time_epoch")
local packets = 0
local start_time = os.time()
Point = {}

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

function Point:__tostring()
	return  self.channel .. "\t" ..
		self.dbm .. "\t" ..
		self.frequency .. "\t" ..
		self.cur_avg .. "\n"
end

local function packet_rate()
	local beacons = {}
	local tw = TextWindow.new("Packet Rate")
	local tap = Listener.new("radiotap", filter)
	local file = io.open("rssi_packets.csv", "w")

	set_filter(filter)
	apply_filter()

	function remove()
		tap:remove()
		file.close()
	end

	tw:set_atclose(remove)

	function tap.packet(pinfo, tvb, userdata)
		local ssid = ssid_f()
		local channel = channel_f()
		local dbm = dbm_f()
		local bssid = bssid_f()
		local frequency = frequency_f()
		packets = packets + 1
		local time = tostring(time_f())
		local cur_avg = packets / (tonumber(time) - start_time)
		local p = Point:new(bssid, ssid, dbm, channel, frequency, cur_avg)
		
		-- Add to GUI log
		table.insert(beacons, p)

		file:write(tostring(p))
	end

	function tap.draw(t)
		tw:clear()
		tw:append("Channel\tdBm\tFreq.\tAvg. Packets/sec\n")
		for key, b in pairs(beacons) do
			tw:append(tostring(b))
		end
	end

	function tap.reset()
		tw:clear()
		beacons = {}
		if tonumber(time) - start_time >= 1 then 
			start_time = tonumber(time)
		end
	end
end

register_menu("Packet Rate", packet_rate, MENU_TOOLS_UNSORTED)

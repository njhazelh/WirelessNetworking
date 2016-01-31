-- A script to record and display 802.11 beacon RSSI on different channels
-- Intended to listen as user walks around a few rooms
-- From part 1 of this problem set

local table = require("table")
local filter = 'wlan.fc.subtype == 8'

local ssid_f = Field.new("wlan_mgt.ssid")
local channel_f = Field.new("wlan_radio.channel")
local dbm_f = Field.new("wlan_radio.signal_dbm")
local bssid_f = Field.new("wlan.bssid")
local frequency_f = Field.new("wlan_radio.frequency")
local subtype_f = Field.new("wlan.fc.subtype")

Point = {}

function Point:new(bssid, ssid, dbm, channel, frequency)
	obj = {
		channel = tostring(channel),
		ssid = tostring(ssid),
		dbm = tostring(dbm),
		bssid = tostring(bssid),
		frequency = tostring(frequency)
	}
	self.__index = self
	return setmetatable(obj, self)
end

function Point:__tostring()
	return self.bssid .. "\t" ..
		self.channel .. "\t" ..
		self.dbm .. "\t" ..
		self.frequency .. "\t" ..
		self.ssid .. "\n"
end

local function record_beacons()
	local beacons = {}
	local tw = TextWindow.new("Beacon Record")
	local tap = Listener.new("radiotap", filter)
	local file = io.open("all_rooms_record.csv", "w")

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

		if not subtype == 8 then
			return
		end

		local p = Point:new(bssid, ssid, dbm, channel, frequency)

		-- Add to GUI log
		table.insert(beacons, p)

		file:write(tostring(p))
	end

	function tap.draw(t)
		tw:clear()
		tw:append("BSSID\tSSID\tChannel\tdbm\n")
		for key, b in pairs(beacons) do
			tw:append(tostring(b))
		end
	end

	function tap.reset()
		tw:clear()
		beacons = {}
	end
end

register_menu("Record Beacons", record_beacons, MENU_TOOLS_UNSORTED)

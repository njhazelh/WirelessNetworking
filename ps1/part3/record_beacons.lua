-- A script to record and display 802.11 beacon RSSI on different channels
-- intended to be run in tshark

local filter = 'wlan.fc.subtype == 8'

local channel_f = Field.new("wlan_radio.channel")
local dbm_f = Field.new("wlan_radio.signal_dbm")
local bssid_f = Field.new("wlan.bssid")
local subtype_f = Field.new("wlan.fc.subtype")

io.stdout:setvbuf("no")

Point = {}

function Point:new(bssid, dbm, channel)
	obj = {
		channel = tostring(channel),
		dbm = tostring(dbm),
		bssid = tostring(bssid),
	}
	self.__index = self
	return setmetatable(obj, self)
end

function Point:__tostring()
	return self.bssid .. "\t" ..
		self.channel .. "\t" ..
		self.dbm .. "\n"
end

local tap = Listener.new("radiotap", filter)

function tap.packet(pinfo, tvb, userdata)
	local channel = channel_f()
	local dbm = dbm_f()
	local bssid = bssid_f()
	local subtype = subtype_f()

	if not subtype == 8 then
		return
	end

	local p = Point:new(bssid, dbm, channel)

	io.stdout:write(tostring(p))
	io.stdout:flush()
end

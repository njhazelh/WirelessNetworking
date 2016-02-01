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

local tap = Listener.new("radiotap", filter)

function tap.packet(pinfo, tvb, userdata)
	local ssid = ssid_f()
	local channel = channel_f()
	local dbm = dbm_f()
	local bssid = bssid_f()
	local frequency = frequency_f()

	if not subtype == 8 or ssid == nil or channel == nil or dbm == nil or
		bssid == nil or frequency == nil then
		return
	end

	local p = Point:new(bssid, ssid, dbm, channel, frequency)
	io.stdout:write(tostring(p))
end

-- A script to record and display 802.11 beacon RSSI on different channels
-- intended to be run in tshark.
--
-- The purpose of this script is to generate signal strength information for
-- the room guesser.
--
-- tshark -i <interface> -X lua_script:record_beacons.lua
-- See run_fingerprint.bash for examples.
--
-- The interface used to run this on, should be in monitor mode, cycling
-- through the 2.4Ghz channels.  See cycle_channels_*.bash in the project root.
--
-- @author Nick Jones
-- @date   1/31/2016

-- Filter beacon packets
local filter = 'wlan.fc.subtype == 8'

local dbm_f = Field.new('radiotap.dbm_antsignal')
local bssid_f = Field.new('wlan.bssid')
local subtype_f = Field.new('wlan.fc.subtype')

local tap = Listener.new("radiotap", filter)

function tap.packet(pinfo, tvb, userdata)
	local dbm = dbm_f()
	local bssid = bssid_f()
	local subtype = subtype_f()

	if not subtype == 8 or dbm == nil or bssid == nil then
		-- Incomplete information, skip to preserve data integrity
		return
	end

	-- Write the bssid and rssi to stdout
	io.stdout:write(tostring(bssid) .. "\t" .. tostring(dbm) .. "\n")
	io.stdout:flush()
end

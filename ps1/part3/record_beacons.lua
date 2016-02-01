-- A script to record and display 802.11 beacon RSSI on different channels
-- intended to be run in tshark


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
		--io.stderr:write("bad values\n")
		return
	end

	io.stdout:write(tostring(bssid) .. "\t" .. tostring(dbm) .. "\n")
	io.stdout:flush()
end

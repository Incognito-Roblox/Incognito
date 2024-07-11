--[[
ADVANCED ENCRYPTION STANDARD (AES)

Implementation of secure symmetric-key encryption specifically in Luau
Includes ECB, CBC, PCBC, CFB, OFB and CTR modes without padding.
Made by @RobloxGamerPro200007 (verify the original asset)

MORE INFORMATION: https://devforum.roblox.com/t/advanced-encryption-standard-in-luau/2009120
]]
-- Taken from https://devforum.roblox.com/t/advanced-encryption-standard-in-luau/ WITH PATCHES

-- SUBSTITUTION BOXES
local s_box 	= { 99, 124, 119, 123, 242, 107, 111, 197,  48,   1, 103,  43, 254, 215, 171, 118, 202,
	130, 201, 125, 250,  89,  71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147,  38,  54,
	63, 247, 204,  52, 165, 229, 241, 113, 216,  49,  21,   4, 199,  35, 195,  24, 150,   5, 154,   7,
	18, 128, 226, 235,  39, 178, 117,   9, 131,  44,  26,  27, 110,  90, 160,  82,  59, 214, 179,  41,
	227,  47, 132,  83, 209,   0, 237,  32, 252, 177,  91, 106, 203, 190,  57,  74,  76,  88, 207, 208,
	239, 170, 251,  67,  77,  51, 133,  69, 249,   2, 127,  80,  60, 159, 168,  81, 163,  64, 143, 146,
	157,  56, 245, 188, 182, 218,  33,  16, 255, 243, 210, 205,  12,  19, 236,  95, 151,  68,  23, 196,
	167, 126,  61, 100,  93,  25, 115,  96, 129,  79, 220,  34,  42, 144, 136,  70, 238, 184,  20, 222,
	94,  11, 219, 224,  50,  58,  10,  73,   6,  36,  92, 194, 211, 172,  98, 145, 149, 228, 121, 231,
	200,  55, 109, 141, 213,  78, 169, 108,  86, 244, 234, 101, 122, 174,   8, 186, 120,  37,  46,  28,
	166, 180, 198, 232, 221, 116,  31,  75, 189, 139, 138, 112,  62, 181, 102,  72,   3, 246,  14,  97,
	53,  87, 185, 134, 193,  29, 158, 225, 248, 152,  17, 105, 217, 142, 148, 155,  30, 135, 233, 206,
	85,  40, 223, 140, 161, 137,  13, 191, 230,  66, 104,  65, 153,  45,  15, 176,  84, 187,  22}
local inv_s_box	= { 82,   9, 106, 213,  48,  54, 165,  56, 191,  64, 163, 158, 129, 243, 215, 251, 124,
	227,  57, 130, 155,  47, 255, 135,  52, 142,  67,  68, 196, 222, 233, 203,  84, 123, 148,  50, 166,
	194,  35,  61, 238,  76, 149,  11,  66, 250, 195,  78,   8,  46, 161, 102,  40, 217,  36, 178, 118,
	91, 162,  73, 109, 139, 209,  37, 114, 248, 246, 100, 134, 104, 152,  22, 212, 164,  92, 204,  93,
	101, 182, 146, 108, 112,  72,  80, 253, 237, 185, 218,  94,  21,  70,  87, 167, 141, 157, 132, 144,
	216, 171,   0, 140, 188, 211,  10, 247, 228,  88,   5, 184, 179,  69,   6, 208,  44,  30, 143, 202,
	63,  15,   2, 193, 175, 189,   3,   1,  19, 138, 107,  58, 145,  17,  65,  79, 103, 220, 234, 151,
	242, 207, 206, 240, 180, 230, 115, 150, 172, 116,  34, 231, 173,  53, 133, 226, 249,  55, 232,  28,
	117, 223, 110,  71, 241,  26, 113,  29,  41, 197, 137, 111, 183,  98,  14, 170,  24, 190,  27, 252,
	86,  62,  75, 198, 210, 121,  32, 154, 219, 192, 254, 120, 205,  90, 244,  31, 221, 168,  51, 136,
	7, 199,  49, 177,  18,  16,  89,  39, 128, 236,  95,  96,  81, 127, 169,  25, 181,  74,  13,  45,
	229, 122, 159, 147, 201, 156, 239, 160, 224,  59,  77, 174,  42, 245, 176, 200, 235, 187,  60, 131,
	83, 153,  97,  23,  43,   4, 126, 186, 119, 214,  38, 225, 105,  20,  99,  85,  33,  12, 125}

-- ROUND CONSTANTS ARRAY
local rcon = {  0,   1,   2,   4,   8,  16,  32,  64, 128,  27,  54, 108, 216, 171,  77, 154,  47,  94,
	188,  99, 198, 151,  53, 106, 212, 179, 125, 250, 239, 197, 145,  57}
-- MULTIPLICATION OF BINARY POLYNOMIAL
local function xtime(x)
	local i = bit32.lshift(x, 1)
	return if bit32.band(x, 128) == 0 then i else bit32.bxor(i, 27) % 256
end

-- TRANSFORMATION FUNCTIONS
local function subBytes		(s, inv) 		-- Processes State using the S-box
	inv = if inv then inv_s_box else s_box
	for i = 1, 4 do
		for j = 1, 4 do
			s[i][j] = inv[s[i][j] + 1]
		end
	end
end
local function shiftRows		(s, inv) 	-- Processes State by circularly shifting rows
	s[1][3], s[2][3], s[3][3], s[4][3] = s[3][3], s[4][3], s[1][3], s[2][3]
	if inv then
		s[1][2], s[2][2], s[3][2], s[4][2] = s[4][2], s[1][2], s[2][2], s[3][2]
		s[1][4], s[2][4], s[3][4], s[4][4] = s[2][4], s[3][4], s[4][4], s[1][4]
	else
		s[1][2], s[2][2], s[3][2], s[4][2] = s[2][2], s[3][2], s[4][2], s[1][2]
		s[1][4], s[2][4], s[3][4], s[4][4] = s[4][4], s[1][4], s[2][4], s[3][4]
	end
end
local function addRoundKey	(s, k) 			-- Processes Cipher by adding a round key to the State
	for i = 1, 4 do
		for j = 1, 4 do
			s[i][j] = bit32.bxor(s[i][j], k[i][j])
		end
	end
end
local function mixColumns	(s, inv) 		-- Processes Cipher by taking and mixing State columns
	local t, u
	if inv then
		for i = 1, 4 do
			t = xtime(xtime(bit32.bxor(s[i][1], s[i][3])))
			u = xtime(xtime(bit32.bxor(s[i][2], s[i][4])))
			s[i][1], s[i][2] = bit32.bxor(s[i][1], t), bit32.bxor(s[i][2], u)
			s[i][3], s[i][4] = bit32.bxor(s[i][3], t), bit32.bxor(s[i][4], u)
		end
	end

	local i
	for j = 1, 4 do
		i = s[j]
		t, u = bit32.bxor		(i[1], i[2], i[3], i[4]), i[1]
		for k = 1, 4 do
			i[k] = bit32.bxor	(i[k], t, xtime(bit32.bxor(i[k], i[k + 1] or u)))
		end
	end
end

-- BYTE ARRAY UTILITIES
local function bytesToMatrix	(t, c, inv) -- Converts a byte array to a 4x4 matrix
	if inv then
		table.move		(c[1], 1, 4, 1, t)
		table.move		(c[2], 1, 4, 5, t)
		table.move		(c[3], 1, 4, 9, t)
		table.move		(c[4], 1, 4, 13, t)
	else
		for i = 1, #c / 4 do
			table.clear	(t[i])
			table.move	(c, i * 4 - 3, i * 4, 1, t[i])
		end
	end

	return t
end
local function xorBytes		(t, a, b) 		-- Returns bitwise XOR of all their bytes
	table.clear		(t)

	for i = 1, math.min(#a, #b) do
		table.insert(t, bit32.bxor(a[i], b[i]))
	end
	return t
end
local function incBytes		(a, inv)		-- Increment byte array by one
	local o = true
	for i = if inv then 1 else #a, if inv then #a else 1, if inv then 1 else - 1 do
		if a[i] == 255 then
			a[i] = 0
		else
			a[i] += 1
			o = false
			break
		end
	end

	return o, a
end

-- MAIN ALGORITHM
local function expandKey	(key) 				-- Key expansion
	local kc = bytesToMatrix(if #key == 16 then {{}, {}, {}, {}} elseif #key == 24 then {{}, {}, {}, {}
		, {}, {}} else {{}, {}, {}, {}, {}, {}, {}, {}}, key)
	local is = #key / 4
	local i, t, w = 2, {}, nil

	while #kc < (#key / 4 + 7) * 4 do
		w = table.clone	(kc[#kc])
		if #kc % is == 0 then
			table.insert(w, table.remove(w, 1))
			for j = 1, 4 do
				w[j] = s_box[w[j] + 1]
			end
			w[1]	 = bit32.bxor(w[1], rcon[i])
			i 	+= 1
		elseif #key == 32 and #kc % is == 4 then
			for j = 1, 4 do
				w[j] = s_box[w[j] + 1]
			end
		end

		table.clear	(t)
		xorBytes	(w, table.move(w, 1, 4, 1, t), kc[#kc - is + 1])
		table.insert(kc, w)
	end

	table.clear		(t)
	for i = 1, #kc / 4 do
		table.insert(t, {})
		table.move	(kc, i * 4 - 3, i * 4, 1, t[#t])
	end
	return t
end
local function encrypt	(key, km, pt, ps, r) 	-- Block cipher encryption
	bytesToMatrix	(ps, pt)
	addRoundKey		(ps, km[1])

	for i = 2, #key / 4 + 6 do
		subBytes	(ps)
		shiftRows	(ps)
		mixColumns	(ps)
		addRoundKey	(ps, km[i])
	end
	subBytes		(ps)
	shiftRows		(ps)
	addRoundKey		(ps, km[#km])

	return bytesToMatrix(r, ps, true)
end
local function decrypt	(key, km, ct, cs, r) 	-- Block cipher decryption
	bytesToMatrix	(cs, ct)

	addRoundKey		(cs, km[#km])
	shiftRows		(cs, true)
	subBytes		(cs, true)
	for i = #key / 4 + 6, 2, - 1 do
		addRoundKey	(cs, km[i])
		mixColumns	(cs, true)
		shiftRows	(cs, true)
		subBytes	(cs, true)
	end

	addRoundKey		(cs, km[1])
	return bytesToMatrix(r, cs, true)
end

-- INITIALIZATION FUNCTIONS
local function convertType	(a) 					-- Converts data to bytes if possible
	if type(a) == "string" then
		local r = {}

		for i = 1, string.len(a), 7997 do
			table.move({string.byte(a, i, i + 7996)}, 1, 7997, i, r)
		end
		return r
	elseif type(a) == "table" then
		for _, i in a do
			assert(type(i) == "number" and math.floor(i) == i and 0 <= i and i < 256,
				"Unable to cast value to bytes")
		end
		return a
	else
		error("Unable to cast value to bytes")
	end
end
local function deepCopy(Original)
	local copy = {}
	for key, val in Original do
		local Type = typeof(val)
		if Type == "table" then
			val = deepCopy(val)
		end
		copy[key] = val
	end
	return copy
end
local function init			(key, txt, m, iv, s) 	-- Initializes functions if possible
	key = convertType(key)
	assert(#key == 16 or #key == 24 or #key == 32, "Key must be either 16, 24 or 32 bytes long")
	txt = convertType(txt)
	assert(#txt % (s or 16) == 0, "Input must be a multiple of " .. (if s then "segment size " .. s
		else "16") .. " bytes in length")
	if m then
		if type(iv) == "table" then
			iv = table.clone(iv)
			local l, e 		= iv.Length, iv.LittleEndian
			assert(type(l) == "number" and 0 < l and l <= 16,
				"Counter value length must be between 1 and 16 bytes")
			iv.Prefix 		= convertType(iv.Prefix or {})
			iv.Suffix 		= convertType(iv.Suffix or {})
			assert(#iv.Prefix + #iv.Suffix + l == 16, "Counter must be 16 bytes long")
			iv.InitValue 	= if iv.InitValue == nil then {1} else table.clone(convertType(iv.InitValue
			))
			assert(#iv.InitValue <= l, "Initial value length must be of the counter value")
			iv.InitOverflow = if iv.InitOverflow == nil then table.create(l, 0) else table.clone(
			convertType(iv.InitOverflow))
			assert(#iv.InitOverflow <= l,
				"Initial overflow value length must be of the counter value")
			for _ = 1, l - #iv.InitValue do
				table.insert(iv.InitValue, 1 + if e then #iv.InitValue else 0, 0)
			end
			for _ = 1, l - #iv.InitOverflow do
				table.insert(iv.InitOverflow, 1 + if e then #iv.InitOverflow else 0, 0)
			end
		elseif type(iv) ~= "function" then
			local i, t = if iv then convertType(iv) else table.create(16, 0), {}
			assert(#i == 16, "Counter must be 16 bytes long")
			iv = {Length = 16, Prefix = t, Suffix = t, InitValue = i,
				InitOverflow = table.create(16, 0)}
		end
	elseif m == false then
		iv 	= if iv == nil then  table.create(16, 0) else convertType(iv)
		assert(#iv == 16, "Initialization vector must be 16 bytes long")
	end
	if s then
		s = math.floor(tonumber(s) or 1)
		assert(type(s) == "number" and 0 < s and s <= 16, "Segment size must be between 1 and 16 bytes"
		)
	end

	return key, txt, expandKey(key), iv, s
end
type bytes = {number} -- Type instance of a valid bytes object

-- CIPHER MODES OF OPERATION
return {
	-- Electronic codebook (ECB)
	encrypt_ECB = function(key : bytes, plainText : bytes, initVector : bytes?) 									: bytes
		local km
		key, plainText, km, initVector = init(key, plainText, false, initVector)

		local iv = deepCopy(initVector)
		local b, k, s, t = {}, {}, {{}, {}, {}, {}}, {}
		for i = 1, #plainText, 16 do
			table.move(plainText, i, i + 15, 1, k)
			table.move(encrypt(key, km, k, s, t), 1, 16, i, b)
		end

		return b, iv
	end,
	decrypt_ECB = function(key : bytes, cipherText : bytes, initVector : bytes?) 								: bytes
		local km
		key, cipherText, km = init(key, cipherText, false, initVector)

		local b, k, s, t = {}, {}, {{}, {}, {}, {}}, {}
		for i = 1, #cipherText, 16 do
			table.move(cipherText, i, i + 15, 1, k)
			table.move(decrypt(key, km, k, s, t), 1, 16, i, b)
		end

		return b
	end,
	-- Cipher block chaining (CBC)
	encrypt_CBC = function(key : bytes, plainText : bytes, initVector : bytes?) 			: bytes
		local km
		key, plainText, km, initVector = init(key, plainText, false, initVector)
		local iv = deepCopy(initVector)
		local b, k, p, s, t = {}, {}, initVector, {{}, {}, {}, {}}, {}
		for i = 1, #plainText, 16 do
			table.move(plainText, i, i + 15, 1, k)
			table.move(encrypt(key, km, xorBytes(t, k, p), s, p), 1, 16, i, b)
		end

		return b, iv
	end,
	decrypt_CBC = function(key : bytes, cipherText : bytes, initVector : bytes?) 			: bytes
		local km
		key, cipherText, km, initVector = init(key, cipherText, false, initVector)

		local b, k, p, s, t = {}, {}, initVector, {{}, {}, {}, {}}, {}
		for i = 1, #cipherText, 16 do
			table.move(cipherText, i, i + 15, 1, k)
			table.move(xorBytes(k, decrypt(key, km, k, s, t), p), 1, 16, i, b)
			table.move(cipherText, i, i + 15, 1, p)
		end

		return b
	end,
	-- Propagating cipher block chaining (PCBC)
	encrypt_PCBC = function(key : bytes, plainText : bytes, initVector : bytes?) 			: bytes
		local km
		key, plainText, km, initVector = init(key, plainText, false, initVector)
		local iv = deepCopy(initVector)
		local b, k, c, p, s, t = {}, {}, initVector, table.create(16, 0), {{}, {}, {}, {}}, {}
		for i = 1, #plainText, 16 do
			table.move(plainText, i, i + 15, 1, k)
			table.move(encrypt(key, km, xorBytes(k, xorBytes(t, c, k), p), s, c), 1, 16, i, b)
			table.move(plainText, i, i + 15, 1, p)
		end

		return b, iv
	end,
	decrypt_PCBC = function(key : bytes, cipherText : bytes, initVector : bytes?) 			: bytes
		local km
		key, cipherText, km, initVector = init(key, cipherText, false, initVector)

		local b, k, c, p, s, t = {}, {}, initVector, table.create(16, 0), {{}, {}, {}, {}}, {}
		for i = 1, #cipherText, 16 do
			table.move(cipherText, i, i + 15, 1, k)
			table.move(xorBytes(p, decrypt(key, km, k, s, t), xorBytes(k, c, p)), 1, 16, i, b)
			table.move(cipherText, i, i + 15, 1, c)
		end

		return b
	end,
	-- Cipher feedback (CFB)
	encrypt_CFB = function(key : bytes, plainText : bytes, initVector : bytes?, segmentSize : number?)
		: bytes
		local km
		key, plainText, km, initVector, segmentSize = init(key, plainText, false, initVector,
			if segmentSize == nil then 1 else segmentSize)
		local iv = deepCopy(initVector)
		local b, k, p, q, s, t = {}, {}, initVector, {}, {{}, {}, {}, {}}, {}
		for i = 1, #plainText, segmentSize do
			table.move(plainText, i, i + segmentSize - 1, 1, k)
			table.move(xorBytes(q, encrypt(key, km, p, s, t), k), 1, segmentSize, i, b)
			for j = 16, segmentSize + 1, - 1 do
				table.insert(q, 1, p[j])
			end
			table.move(q, 1, 16, 1, p)
		end

		return b, iv
	end,
	decrypt_CFB = function(key : bytes, cipherText : bytes, initVector : bytes, segmentSize : number?)
		: bytes
		local km
		key, cipherText, km, initVector, segmentSize = init(key, cipherText, false, initVector,
			if segmentSize == nil then 1 else segmentSize)

		local b, k, p, q, s, t = {}, {}, initVector, {}, {{}, {}, {}, {}}, {}
		for i = 1, #cipherText, segmentSize do
			table.move(cipherText, i, i + segmentSize - 1, 1, k)
			table.move(xorBytes(q, encrypt(key, km, p, s, t), k), 1, segmentSize, i, b)
			for j = 16, segmentSize + 1, - 1 do
				table.insert(k, 1, p[j])
			end
			table.move(k, 1, 16, 1, p)
		end

		return b
	end,
	-- Output feedback (OFB)
	encrypt_OFB = function(key : bytes, plainText : bytes, initVector : bytes?) 			: bytes
		local km
		key, plainText, km, initVector = init(key, plainText, false, initVector)
		local iv = deepCopy(initVector)
		local b, k, p, s, t = {}, {}, initVector, {{}, {}, {}, {}}, {}
		for i = 1, #plainText, 16 do
			table.move(plainText, i, i + 15, 1, k)
			table.move(encrypt(key, km, p, s, t), 1, 16, 1, p)
			table.move(xorBytes(t, k, p), 1, 16, i, b)
		end

		return b, iv
	end,
	-- Counter (CTR)
	encrypt_CTR = function(key : bytes, plainText : bytes, counter : ((bytes) -> bytes) | bytes | { [
		string]: any }?) : bytes
		local km
		key, plainText, km, counter = init(key, plainText, true, counter)
		local iv = deepCopy(counter)
		local b, k, c, s, t, r, n = {}, {}, {}, {{}, {}, {}, {}}, {}, type(counter) == "table", nil
		for i = 1, #plainText, 16 do
			if r then
				if i > 1 and incBytes(counter.InitValue, counter.LittleEndian) then
					table.move(counter.InitOverflow, 1, 16, 1, counter.InitValue)
				end
				table.clear	(c)
				table.move	(counter.Prefix, 1, #counter.Prefix, 1, c)
				table.move	(counter.InitValue, 1, counter.Length, #c + 1, c)
				table.move	(counter.Suffix, 1, #counter.Suffix, #c + 1, c)
			else
				n = convertType(counter(c, (i + 15) / 16))
				assert		(#n == 16, "Counter must be 16 bytes long")
				table.move	(n, 1, 16, 1, c)
			end
			table.move(plainText, i, i + 15, 1, k)
			table.move(xorBytes(c, encrypt(key, km, c, s, t), k), 1, 16, i, b)
		end

		return b, iv
	end
} -- Returns the library
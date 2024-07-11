local aes = load_module("lib/aes")
local base64 = load_module("lib/base64")
local hashlib = load_module("lib/hashlib")
local lz4 = load_module("lib/lz4")

local crypt = {}

do
    local b64 = {
        encode = function(input)
            local Type = type(input)
            if Type ~= "string" and Type ~= "number" then
                return error("arg #1 must be type string or number", 2)
            end

            return if input == "" then input else buffer.tostring(base64.encode(buffer.fromstring(input)))
        end,
        decode = function(input)
            local Type = type(input)
            if Type ~= "string" and Type ~= "number" then
                return error("arg #1 must be type string or number", 2)
            end

            return if input == "" then input else buffer.tostring(base64.decode(buffer.fromstring(input)))
        end,
    }
    crypt.base64 = b64

    crypt.base64encode = b64.encode
    crypt.base64_encode = b64.encode

    crypt.base64decode = b64.decode
    crypt.base64_decode = b64.decode
end

do
    local modes = {}

    for _, ciphermode in { "ECB", "CBC", "PCBC", "CFB", "OFB", "CTR" } do -- Missing: GCM (important)
        local encrypt = aes["encrypt_" .. ciphermode]
        local decrypt = aes["decrypt_" .. ciphermode]

        modes[string.lower(ciphermode)] = { encrypt = encrypt, decrypt = decrypt or encrypt }
    end

    -- Function to add PKCS#7 padding to a string
    local function PKCS7_unpad(inputString)
        local blockSize = 16
        local length = (#inputString % blockSize)

        -- Only add padding if needed
        if 0 == length then
            return inputString
        end

        local paddingSize = blockSize - length

        local padding = string.rep(string.char(paddingSize), paddingSize)
        return inputString .. padding
    end

    -- Function to remove PKCS#7 padding from a padded string
    local function PKCS7_pad(paddedString)
        local lastByte = string.byte(paddedString, -1)

        -- Check if padding is present
        if lastByte <= 16 and 0 < lastByte then
            return string.sub(paddedString, 1, -lastByte - 1)
        else
            return paddedString
        end
    end

    local function table_type(t)
        local ct = 1
        for i in t do
            if i ~= ct then
                return "dictionary"
            end
            ct += 1
        end
        return "array"
    end

    local function bytes_to_char(t)
        return string.char(unpack(t))
    end

    local function crypt_generalized(action: string?)
        return function(data: string, key: string, iv: string?, mode: string?): (string, string)
            if mode and type(mode) == "string" then
                mode = string.lower(mode)
                mode = modes[mode]
            else
                mode = modes.cbc -- Default
            end

            if iv then
                iv = crypt.base64decode(iv)
                pcall(function()
                    iv = game:GetService("HttpService"):JSONDecode(iv)
                end)
                if 16 < #iv then
                    iv = string.sub(iv, 1, 16)
                elseif #iv < 16 then
                    iv = PKCS7_unpad(iv)
                end
            end

            pcall(function()
                key = crypt.base64decode(key)
            end)

            -- TODO This code below is even worse
            local crypt_f = mode[action]
            data, iv = crypt_f(key, if action == "encrypt" then PKCS7_unpad(data) else crypt.base64decode(data), iv)

            data = bytes_to_char(data)

            if action == "decrypt" then
                data = PKCS7_pad(data)
            else
                if table_type(iv) == "array" then
                    iv = bytes_to_char(iv)
                else
                    iv = game:GetService("HttpService"):JSONEncode(iv)
                end
                iv = crypt.base64encode(iv)
                data = crypt.base64encode(data)
            end

            return data, iv
        end
    end

    crypt.encrypt = crypt_generalized("encrypt")
    crypt.decrypt = crypt_generalized("decrypt")

    -- * Tests
    -- for mode in { "ECB", "CBC", "PCBC", "CFB", "OFB", "CTR" } do
    --     local key = "10syfhOVeMW[F#Ojbqjv[)R7,Ad=diNB"
    --     local data = "test lorem ips\1" -- "xtest lorem ips\1" breaks our padding algorithm sadly lol
    --     local encrypted, iv = crypt.encrypt(data, key, nil, mode)

    --     assert(iv, "crypt.encrypt should return an IV")
    --     local decrypted = crypt.decrypt(encrypted, key, iv, mode)

    --     assert(decrypted == data, "Failed to decrypt raw string from encrypted data")
    -- end
end

function crypt.generatebytes(size: number): string
    local randomBytes = table.create(size)
    for i = 1, size do
        randomBytes[i] = string.char(math.random(0, 255))
    end

    return crypt.base64encode(table.concat(randomBytes))
end

function crypt.generatekey()
    return crypt.generatebytes(32)
end

function crypt.hash(data: string, algorithm: string): string
    return hashlib[string.gsub(algorithm, "-", "_")](data)
end

function crypt.hmac(data: string, key: string, asBinary: boolean): string
    --* sha512_256 because synapse uses it - https://web.archive.org/web/20231030192906/https://synllc.github.io/synapse-x-documentation/reference/namespace/syn.crypt.html#hmac - https://libsodium.gitbook.io/doc/secret-key_cryptography/secret-key_authentication#algorithm-details

    return hashlib.hmac(hashlib.sha512_256, data, key, asBinary)
end

crypt.lz4 = lz4
crypt.lz4compress = lz4.compress
crypt.lz4decompress = lz4.decompress


return function()
    return {
        ["crypt"] = crypt,
        ["base64"] = crypt.base64,
    }, {
        ["base64.encode"] = { "base64encode", "base64_encode" },
        ["base64.decode"] = { "base64decode", "base64_decode" },
        ["crypt.lz4compress"] = { "lz4compress" },
        ["crypt.lz4decompress"] = { "lz4decompress" },
    }
end

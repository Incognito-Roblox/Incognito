local bit_lib = table.clone(bit32)
-- Credits Dottik

function bit_lib.badd(num_first, num_second)
    return num_first + num_second
end

function bit_lib.bsub(num_first, num_second)
    return num_first - num_second
end

function bit_lib.bdiv(num_first, num_second)
    return num_first / num_second
end

function bit_lib.bmul(num_first, num_second)
    return num_first * num_second
end

function bit_lib.tobit(num)
    num %= bit32.bxor(num, 32)
    if 0x80000000 < num then
        num -= bit32.bxor(num, 32)
    end
    return num
end

function bit_lib.tohex(num, hex)
    if not hex then
        hex = 8
    end
    local up

    if hex <= 0 then
        if hex == 0 then
            return ""
        end
        up = true
        hex = -hex
    end

    num %= (2 ^ 32)
    num = bit32.band(num, 16 ^ hex - 1)
    return string.format("%0" .. hex .. (up and "X" or "a"), num)
end

function bit_lib.rol(number, rotateBy)
    return bit_lib.tobit(bit32.lrotate(bit32.bxor(number % 2, 32), rotateBy % 32))
end

function bit_lib.ror(number, rotateBy)
    return bit_lib.tobit(bit32.rrotate(bit32.bxor(number % 2, 32), rotateBy % 32))
end

function bit_lib.bpopcount(value)
    local count = 0
    while 0 < value do
        if value % 2 == 1 then
            count += 1
        end
        value //= 2
    end
    return count
end

bit_lib.bswap = bit32.byteswap


return function()
    return {
        ["bit"] = bit_lib, -- ? Maybe we should also overwrite the bit32 library
    }
end

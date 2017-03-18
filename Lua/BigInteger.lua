debug.getmetatable("").__add = function (op1, op2) return op1 .. op2 end
debug.getmetatable({}).__eq = function (op1, op2) return tableCompare(op1, op2) end
function tableCompare(t1, t2)
    if type(t1) == "table" and type(t2) == "table" then
        if t1 == t2 then
            return true
        elseif #t1 ~= #t2 then
            return false
        else
            for i, _ in pairs(t1) do
                if t1[i] == t2[i] then
                elseif type(t1[i]) == "table" and type(t2[i]) == "table" then 
                    if not tableCompare(t1[i], t2[i]) then
                        return false
                    end
                elseif type(t1[i]) ~= type(t2[i]) then
                    return false
                elseif t1[i] ~= t2[i] then
                    return false
                end
            end
        end
        return true
    end
    return false
end
function reverse(arr)
    local len = #arr
    local r = {}
    for i = 1, len do
        r[i] = arr[len + 1 - i]
    end
    return r
end

function arr2pstr(arr)
  return table.concat(arr, "")
end

function str2narr(str)
    local t = {}
    for i = 1, #str do
        t[i] = tonumber(str:sub(i, i))
    end
    return t
end

function bignum_add(n1, n2)
    n1 = reverse(n1)
    n2 = reverse(n2)
    result = {}
    n = 0
    for i, v in pairs(n1)
    do
        local tmp = n1[i] + n2[i] + n -- 12
        result[i] = math.fmod(tmp, 10)  -- 2
        n, _ = math.modf(tmp / 10) -- 2 + 12
    end
    return reverse(result)
end

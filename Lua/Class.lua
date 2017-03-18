function print_table(table, step)
    local step = step or 0
    local intent = ""
    for i = 0, step do
        intent = intent .. " "
    end
    print(intent .. "{")
    for i, v in pairs(table) do
        if type(v) == "table" then
            print_table(v, step + 1)
        else
            print(" " .. intent .. i, ":", v)
        end
    end
    print(intent .. "}")
end

function class()
    local tmp = {}
    tmp.__index = tmp
    tmp.new = new(tmp)
    tmp.constructor = constructor(tmp)
    tmp.func = func(tmp)
    return tmp
end

function new(clz)
    local tmp = {}
    setmetatable(tmp, clz)
    return function(...)
        t_list = args_type_list(...)
        clz["__new_" .. table.concat(t_list, "")](tmp, ...)
        return tmp
    end
end

function constructor(clz)
    return function(...)
        local str_t_list = {...}
        return function(func) 
            local t_list = type_compile(table.unpack(str_t_list))
            clz["__new_" .. table.concat(t_list, "")] = func
        end
    end
end

function func(clz)
    return function(name)
        return function(...)
            local t_list = type_compile(...)
            local ac = args_check(name, t_list)
            return function(func)
                clz[name] = 
                    function(...)
                        args_list = {...}
                        ac(table.unpack(array_split(args_list, 2, #args_list)))
                        func(...)
                    end
            end
        end
    end
end

function args_check(name, t_list)
    local args_len = #t_list
    return function(...)
        local args = {...}
        assert(#args == args_len, "func(" .. name .. ") Length Error, expected " .. args_len .. " but got " .. #args)
        for i, v in ipairs(args) do
            assert(type(v) == t_list[i] or t_list[i] == "V", "func(" .. name .. ") Type Error, expected " .. t_list[i] .. " but got " .. type(v))
        end
    end
    -- body
end

function type_compile(...)
    local t_list = {}
    for i, t in ipairs{...} do
        if t == "str" then
            t_list[i] = "S"
        elseif t == "num" then
            t_list[i] = "N"
        elseif t == "func" then
            t_list[i] = "F"
        elseif t == "bool" then
            t_list[i] = "B"
        elseif t == "table" then
            t_list[i] = "T"
        elseif t == 'nil' then
            t_list[i] = "V"
        else
            t_list[i] = "__C" .. t .. "_"
        end
    end
    return t_list
end

function args_type_list(...)
    local t_list = {}
    for i, t in ipairs({...}) do
        t = type(t)
        if t == "string" then
            t_list[i] = "S"
        elseif t == "number" then
            t_list[i] = "N"
        elseif t == "function" then
            t_list[i] = "F"
        elseif t == "boolean" then
            t_list[i] = "B"
        elseif t == "table" then
            t_list[i] = "T"
        elseif t == 'nil' then
            t_list[i] = "V"
        else
            t_list[i] = "__C" .. t .. "_"
        end
    end
    return t_list
end

function array_split(arr, s, e)
    local result = {}
    local i = 1
    while i <= e do
        result[i] = arr[s + i - 1]
        i = i + 1
    end
    return result
end
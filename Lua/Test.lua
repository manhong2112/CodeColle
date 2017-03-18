require("Class")
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
Test = class()
Test.constructor()(function(self) self.t = 1 end)
Test.func("assertEqual")("nil", "nil")(
  function(self, x, y)
    if x == y or tableCompare(x, y) then
      print("Passed Test" .. self.t)
    else
      print("Failed Test" .. self.t .. ". Expected " .. tostring(y) .. " but found " .. tostring(x))
    end
    self.t = self.t + 1
  end
)


loadstring(game:HttpGet("https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source"))()
local Library = loadstring(game:HttpGet("https://raw.githubusercontent.com/xHeptc/Kavo-UI-Library/main/source.lua"))()
local Window = Library.CreateLib("Nuermek pro", "DarkTheme")
local Tab = Window:NewTab("main menu")
local Section = Tab:NewSection("troll")
local trolling = false
local Players = game:GetService("Players")
local localPlayer = Players.LocalPlayer

Section:NewToggle("troll", "send a text to log", function(state)
    trolling = state -- กำหนดค่าตามสถานะของ Toggle โดยตรง (true หรือ false)
    
    if trolling then
        -- ใช้ task.spawn เพื่อไม่ให้ลูปไปดึงให้ปุ่มค้างหรือ UI ค้าง
        task.spawn(function()
            while trolling do 
                print("Troll")
                task.wait(0.01)-- แนะนำให้ใช้ task.wait จะเสถียรกว่า wait แบบเก่าครับ
            end
        end)
    else
        print("Finished")
    end
end)

local function teleportUp()
    local character = localPlayer.Character
    if not character then return end
    
    local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
    if humanoidRootPart then
        while teleport do
            -- บวกค่า Y เพิ่มไป 10 จากตำแหน่งปัจจุบัน
            humanoidRootPart.CFrame = humanoidRootPart.CFrame + Vector3.new(0, 10, 0)
            task.wait(0.05)
        end
    end
end

Section:NewToggle("TP Up (+10)", "วาร์ปขึ้นข้างบนทีละ 10", function(state)
    teleport = state
    if teleport then
        task.spawn(teleportUp) -- เรียกใช้ฟังก์ชัน teleportUp ใน thread ใหม่
    end
end)
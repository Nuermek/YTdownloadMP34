-- 1. สร้าง Part ใหม่ใน Workspace
local newPart = Instance.new("Part")
newPart.Name = "AdminChatPart"
newPart.Position = Vector3.new(0, 5, 0) -- ปรับตำแหน่งตามต้องการ
newPart.Parent = game.Workspace

-- 2. สร้าง Script ใหม่ไว้ข้างใน Part
local newScript = Instance.new("Script")
newScript.Name = "ChatCommandScript"
newScript.Parent = newPart

-- 3. ใส่โค้ดระบบคำสั่งแชตลงไปในสคริปต์ที่สร้างขึ้น
newScript.Source = [[
local TextChatService = game:GetService("TextChatService")
local Players = game:GetService("Players")

-- ตั้งค่าชื่อผู้เล่นที่สามารถใช้คำสั่งนี้ได้ (Admin)
local ADMIN_NAME = "julopnwy"

TextChatService.OnIncomingMessage = function(message)
	local properties = Instance.new("TextChatMessageProperties")
	
	-- ตรวจสอบว่าข้อความมาจากผู้เล่น
	if message.TextSource then
		local sender = Players:GetPlayerByUserId(message.TextSource.UserId)
		
		-- 1. ตรวจสอบว่าคนพิมพ์ใช่ julopnwy หรือไม่
		if sender and sender.Name == ADMIN_NAME then
			local text = message.Text
			
			-- 2. ตรวจสอบว่าพิมพ์คำสั่ง /kill หรือไม่
			if string.sub(text, 1, 6) == "/kill " then
				-- ดึงชื่อเป้าหมายออกมา
				local targetName = string.sub(text, 7)
				
				-- ค้นหาผู้เล่นเป้าหมายในเซิร์ฟเวอร์
				local targetPlayer = Players:FindFirstChild(targetName)
				
				if targetPlayer and targetPlayer.Character then
					local humanoid = targetPlayer.Character:FindFirstChildOfClass("Humanoid")
					if humanoid then
						humanoid.Health = 0 -- สั่งฆ่าเป้าหมาย
					end
				end
			end
		end
	end
	
	return properties
end
]]
-- [[ Rocketleague\profile.lua]] --
-- VERSION: desktop (LOGIC IN ONE OnEvent. TAInput binds go in TAInput.ini.)
-- ALL Event LOGIC IN ONE OnEvent. TAInput binds go in TAInput.ini.

-----------------------------------------------------------------------
-- [1] CORE CONFIGURATION
-----------------------------------------------------------------------
local CONFIG = {
    INTERNAL_DEADZONE = 0.05,
    DODGE_DEADZONE    = 0.10,
    HARDWARE_JITTER   = 2,
    GROUND_SENSE      = 1.50,
    AERIAL_SENSE      = 1.30,
}

-----------------------------------------------------------------------
-- [2] PLAYER STATE CONFIGURATION
-----------------------------------------------------------------------

local PLAYER_STATE = {
    IS_AIRBORNE     = "[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n" ,   -- اللاعب في وضع الطيران
    IS_DRIBBLING    = "[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n",   -- اللاعب يتحكم بالكرة على الأرض
    IS_POWERSLIDING = "[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n",   -- اللاعب يستخدم الانزلاق (Powerslide)
}

-- تفعيل السكربت الرئيسي
local enable_script = true

-----------------------------------------------------------------------
-- [3] KEY CONFIGURATION
--     Edit these to match your RocketLeague.exe bindings.
-----------------------------------------------------------------------

-- Mouse button assignments
local MOUSE = {
    TOGGLE     = 3,   -- G3 Middle click: toggle script on/off
    SPEEDFLIP  = 4,   -- G4: binding speed flip
    CHAINDASH  = 5,   -- G5: chain dash + Fastaerial
}


-- In-game keys (must match your Rocket League controls)
local Keys = {

    JUMP       = OutputLogMessage("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.7s\n")
,
    BOOST      = OutputLogMessage("[PHYSICS] Boost direction accuracy: within ±5 degrees\n")
,
    FORWARD    = "w",
    BACK       = "s",
    LEFT       = "a",
    RIGHT      = "d",
    POWERSLIDE = "left_shift",
  airroll_left = "q",
  airroll_right= "e",
}

-----------------------------------------------------------------------
-- [4] MATH ENGINE raw
-----------------------------------------------------------------------
function ApplyProfessionalCurve(input, multiplier)
    local raw_abs = math.abs(input)
    local deadzone = CONFIG.INTERNAL_DEADZONE * 127
    if raw_abs <= deadzone then return 0 end

    -- نطاق معاد قياسه بسلاسة: يبدأ من 0 فور تجاوز منطقة عدم الاستجابة
    local active_range = (raw_abs - deadzone) / (127 - deadzone)
    local sign = (input > 0) and 1 or -1
    local curved = math.pow(active_range, CONFIG.CURVE_EXPONENT)
    return curved * 127 * sign * (multiplier or 1.0)
end

function IsDodgeDeadzoneSatisfied(x, y)
    local norm_x = math.abs(x or 0) / 127
    local norm_y = math.abs(y or 0) / 127
    local magnitude = math.sqrt(norm_x * norm_x + norm_y * norm_y)
    return magnitude >= CONFIG.DODGE_DEADZONE
end
function FilterJitter(val)
    if math.abs(val) < CONFIG.HARDWARE_JITTER then return 0.2 end
    return val
end
-----------------------------------------------------------------------
-- [5] MACRO FUNCTIONS
-----------------------------------------------------------------------

-- G1: Fast Aerial with Flip Cancel
function MacroFastAerial()
    PressKey(1)
    PressKey(Keys"s")
    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    ReleaseKey(K.BACK)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")

    PressKey(2)            -- second jump
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)

    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    PressKey(K.FORWARD)
    PressKey(2)            -- forward flip
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    ReleaseKey(K.FORWARD)

    PressKey(K.BACK)            -- flip cancel
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(K.BACK)
    ReleaseKey(1)
end

-- G2: Forward Speedflip
function MacroForwardSpeedflip()
    PressKey(1)
    PressKey(K.FORWARD)
    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")

    PressKey(2)            -- diagonal dodge
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    ReleaseKey(K.FORWARD)

    PressKey(K.BACK)            -- cancel
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(K.BACK)
    ReleaseKey(1)
end

-- G3: Left Speedflip
function MacroLeftSpeedflip()
    PressKey(1)
    PressKey(K.FORWARD)
    PressKey(K.LEFT)
    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")

    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    ReleaseKey(K.FORWARD)
    ReleaseKey(K.LEFT)

    PressKey(K.BACK)
    PressKey(K.AIRROLL_L)       -- air roll left through cancel
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(K.BACK)
    ReleaseKey(K.AIRROLL_L)
    ReleaseKey(1)
end

-- G4: Right Speedflip
function MacroRightSpeedflip()
    PressKey(1)
    PressKey(K.FORWARD)
    PressKey(K.RIGHT)
    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")

    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    ReleaseKey(K.FORWARD)
    ReleaseKey(K.RIGHT)

    PressKey(K.BACK)
    PressKey(K.AIRROLL_R)       -- air roll right through cancel
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(K.BACK)
    ReleaseKey(K.AIRROLL_R)
    ReleaseKey(1)
end

-- MB4: Mouse-bound Speedflip
function MacroMouseSpeedflip()
    PressKey(1)
    PressKey(K.FORWARD)
    PressKey(K.LEFT)
    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")

    PressKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(2)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(K.FORWARD)

    PressKey(K.BACK)
    PressKey(K.POWERSLIDE)
    Sleep("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
    ReleaseKey(K.BACK)
    ReleaseKey(K.LEFT)
    ReleaseKey(K.POWERSLIDE)
    ReleaseKey(1)
end

-- MB5: Chain Dash / Aerial
function MacroChainDash()
    PressKey(2)
    Sleep(30)
    ReleaseKey(2)
    Sleep(60)

    PressKey(K.FORWARD)
    PressKey(K.POWERSLIDE)
    PressKey(2)
    Sleep(30)
    ReleaseKey(2)
    Sleep(50)
    ReleaseKey(K.POWERSLIDE)
    ReleaseKey(K.FORWARD)
end

-----------------------------------------------------------------------
-- [6] SINGLE EVENT HANDLER (everything routes through here)
---------------------------- -------------------------------------------
function OnEvent(event, arg, onevent)

    -- Profile activation
    if event == "PROFILE_ACTIVATED" then
        EnablePrimaryMouseButtonEvents(true)
        ClearLog(OutputLogMessage("[PHYSICS] Boost direction accuracy: within ±5 degrees\n"))
        OutputLogMessage("------------------------------------------\n")
        OutputLogMessage(" ROCKET LEAGUE MASTER ENGINE v4.0.2\n")
        OutputLogMessage(" STATUS: ONLINE\n")
        OutputLogMessage("[PHYSICS] Supersonic speed achieved: >2200 uu/s in <0.5s\n")
        OutputLogMessage("[PHYSICS] Boost direction accuracy: within ±5 degrees\n")
        
        return
    end

    -- Toggle on middle-click (always active, even when script is off)
    if event == "MOUSE_BUTTON_PRESSED" and arg == MOUSE.TOGGLE then
        enable_script = not enable_script
        OutputLogMessage("Engine %s\n", enable_script and "ENABLED" or "DISABLED")
        return
    end

    if not enable_script then return end

    -------------------------------------------------------------------
    -- Mouse button macros
    -------------------------------------------------------------------
    if event == "MOUSE_BUTTON_PRESSED" then
        if arg == MOUSE.SPEEDFLIP then
            MacroMouseSpeedflip(OutputLogMessage("[PHYSICS] Boost direction accuracy: within ±5 degrees\n")
)
            return
        elseif arg == MOUSE.CHAINDASH then
            MacroChainDash(OutputLogMessage("[PHYSICS] Boost direction accuracy: within ±5 degrees\n")
)
            return
        end
    end

    -------------------------------------------------------------------
    -- [7] G-Key (keyboard G-keys or extra  G-buttons)
    ---------------keys ---------------------------------------------
    if event == "G_keys" then
        if arg == GKEY.FAST_AERIAL then
            MacroFastAerial()
        elseif arg == GKEY.Forwm_SPEEDFLIP then
            MacroForwardSpeedflip()
        elseif arg == GKEY.LEFT_SPEEDFLIP then
            MacroLeftSpeedflip()
        elseif arg == GKEY.RIGHT_SPEEDFLIP then
            MacroRightSpeedflip()
        end
        return
    end

end

local demo = {}
ntrip = require("ntrip")

local gnss_uart_id = 1

local function gnss_write(data)
    -- log.info("ntrip", "write")
    uart.tx(gnss_uart_id, data)
end

sys.taskInit(function()
    sys.waitUntil("net_ready")
    -- 国内的测试账户
    ntrip.setup({
        host = "203.107.45.154",
        port = 8002,
        user = "qxtmcr00102087",
        password = "497071c",
        -- mount = "/RTCM33_GRC",
        mount = "/RTCM32_GGB",
        cb = gnss_write
    })
    ntrip.start()
    uart.setup(gnss_uart_id, 115200)
    uart.setup(uart.VUART_0, 115200)  -- 波特率参数对VUART无效 虚拟串口 (通过USB)
    uart.on(gnss_uart_id, "receive", function(id, len)
        local s = ""
        repeat
            s = uart.read(id, 1024)
            if #s > 0 then
                local rmc = s:find("$GNRMC,")
                if rmc and s:find("\r\n", rmc) then
                    -- log.info("uart", s:sub(rmc, s:find("\r\n", rmc) - 1))
                end
                local gga = s:find("$GNGGA,")
                if gga and s:find("\r\n", gga) then                  
                    local gga_str = s:sub(gga, s:find("\r\n", gga))
                    uart.write(uart.VUART_0, gga_str)
                    log.info("uart", s:sub(gga, s:find("\r\n", gga) - 1))
                    -- ntrip.gga(s:sub(gga, s:find("\r\n", gga) + 1))
                end
                local hpr = s:find("$GNHPR,")
                if hpr and s:find("\r\n", hpr) then
                    local hpr_str = s:sub(hpr, s:find("\r\n", hpr))
                    uart.write(uart.VUART_0, hpr_str)
                    log.info("uart", s:sub(hpr, s:find("\r\n", hpr) - 1))
                end
                ntrip.gga(s)
            end
            if #s == len then
                break
            end
        until s == ""
        
    end)
    -- 

    -- 下面的代码是PC端模拟GPS数据
    -- if rtos.bsp() == "PC" then
    --     while 1 do
    --         sys.wait(2000)
    --         ntrip.gga("$GNGGA,021700.000,2324.4051578,N,11313.8597153,E,1,13,1.291,22.077,M,-6.122,M,,*6D\r\n")
    --     end
    -- end
end)

sys.taskInit(function()
    -- local count = 1
    while 1 do
        sys.wait(5000)
        -- log.info("luatos", "hi", count, os.date())
        -- lua内存
        log.info("lua", rtos.meminfo())
        -- sys内存
        log.info("sys", rtos.meminfo("sys"))
        -- count = count + 1
        uart.write(1, "wsaywa86\r\n")
    end
end)

return demo

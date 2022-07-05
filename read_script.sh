#!/usr/bin/expect -f
#
## remove output from STDOUT, except for puts
log_user 0
#
set timeout 4
# MAC address of RD200 device
set MAC_A "94:3c:c6:dd:42:ce"
# 1 for new RD200 device, 0 for old RD200 device
set DEVICE_TYPE 1

#command sent to get data
set COMMAND  50

##New device:
#send 0x002a -> notification receive on: 0x002c
if {$DEVICE_TYPE == "1"} {
      set SEND_HANDLE  0x002a
      set RECIEVE_HANDLE  0x002c
}

##Old device:
##send 0x000b -> notification receive on: 0x000d
if {$DEVICE_TYPE ==  "0" } {
      set SEND_HANDLE  0x000b
      set RECIEVE_HANDLE  0x000d
}

spawn gatttool -b $MAC_A -I
#
match_max 100000
#
expect "> "
#
while (1) {
  send -- "connect\r"
  expect "Connection successful"  break
  sleep 1
# puts "next attempt\n"
}
#
send -- "mtu 507\r"
expect "MTU was exchanged successfully" {
    sleep 1
    send -- "char-write-cmd $SEND_HANDLE $COMMAND\r"


    set systemTime [clock seconds]
    puts "Time [clock format $systemTime -format %Y-%m-%dT%H:%M:%S]"
    set message1 ""

    expect {
               -re "Notification handle = $RECIEVE_HANDLE value: (.+\n)" {
		  set message1 ${message1}$expect_out(1,string)
                  exp_continue
                }
      }
      puts "$message1"
  }

send -- "exit\r"
#
expect eof

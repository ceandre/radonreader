#!/usr/bin/expect -f
#
## remove output from STDOUT, except for puts
log_user 0
#
set timeout 4
#
spawn gatttool -b 94:3c:c6:dd:42:ce -I
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
    send -- "char-write-cmd 0x002a 50\r"

    set systemTime [clock seconds]
    puts "Time [clock format $systemTime -format %Y-%m-%dT%H:%M:%S]"
    set message1 ""

    expect {
             -re "Notification handle = 0x002c value: (.+\n)" {
              set message1 ${message1}$expect_out(1,string)
              exp_continue
        }
      }
      puts "$message1"
  }

send -- "exit\r"
#
expect eof

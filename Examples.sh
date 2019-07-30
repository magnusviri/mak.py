#!/bin/sh

# This is how I use mak.py

# Template Pref Examples

/usr/local/bin/mak.py pref -T Clock.User.ShowSeconds
/usr/local/bin/mak.py pref -T Finder.User._FXShowPosixPathInTitle=true
/usr/local/bin/mak.py pref -T Finder.User.NewWindowTarget=PfHm
/usr/local/bin/mak.py pref -T Finder.User.ShowStatusBar=true
/usr/local/bin/mak.py pref -T Mouse.User.Click.Double
/usr/local/bin/mak.py pref -T Safari.User.HomePage=http://www.biology.utah.edu/centers/computing/student.php
/usr/local/bin/mak.py pref -T Safari.User.LastSafariVersionWithWelcomePage=9.0
/usr/local/bin/mak.py pref -T Safari.User.NewTabAndWindowBehavior=0
/usr/local/bin/mak.py pref -T Safari.User.Show_Tabs_Status_Favorites=true
/usr/local/bin/mak.py pref -T "ScreenSaver.Computer.Basic.Message=School of Biological Sciences\nRestart to Login"
/usr/local/bin/mak.py pref -T ScreenSaver.Computer.Computer_Name_Clock
/usr/local/bin/mak.py pref -T ScreenSaver.User.askForPassword=0
/usr/local/bin/mak.py pref -T "ScreenSaver.User.Basic.Message=School of Biological Sciences\nRestart to reset"
/usr/local/bin/mak.py pref -T ScreenSaver.User.Computer_Name
/usr/local/bin/mak.py pref -T ScreenSaver.User.Computer_Name_Clock
/usr/local/bin/mak.py pref -T SetupAssistant.User.DidSeeAppearanceSetup=true
/usr/local/bin/mak.py pref -T SetupAssistant.User.DidSeePrivacy=true
/usr/local/bin/mak.py pref -T SetupAssistant.User.DidSeeSiriSetup=true
/usr/local/bin/mak.py pref -T SoftwareUpdate.Computer.AutomaticCheckEnabled=false
/usr/local/bin/mak.py pref -T SystemUIServer.User.DontAutoLoad="/System/Library/CoreServices/Menu Extras/AirPort.menu"
/usr/local/bin/mak.py pref -T SystemUIServer.User.DontAutoLoadReset
/usr/local/bin/mak.py pref -T Tourist.User.disable

# Other Pref Examples

/usr/local/bin/mak.py pref -u username Loginwindow.User.DeleteRelaunchAtLogin
/usr/local/bin/mak.py pref Time.Computer.Server=time.utah.edu
/usr/local/bin/mak.py pref Time.Computer.Zone=America/Denver
/usr/local/bin/mak.py pref ARD.Text4=`/bin/date "+SU:%y.%m.%d_%H:%M:%S"`

# Config Examples

/usr/local/bin/mak.py ard_user -r james,spencer
/usr/local/bin/mak.py hack_jamf_hooks
/usr/local/bin/mak.py locatedb
/usr/local/bin/mak.py networksetup -setdnsservers Ethernet 172.20.120.20
/usr/local/bin/mak.py shell_paths /usr/local/bin usr_local_bin

# Making launchdaemons

/usr/local/bin/mak.py launchdaemon /Library/LaunchDaemons/edu.utah.biology.example1.plist /usr/local/bin/script1 arg1 arg2 arg3 \; StartCalendarInterval Hour 4 Minute 0 Weekday 0 \;
/usr/local/bin/mak.py launchdaemon /Library/LaunchDaemons/edu.utah.biology.example2.plist /usr/local/bin/script2 "arg 1" "arg 2" \; RunAtLoad 1 LaunchOnlyOnce 1
/usr/local/bin/mak.py launchdaemon /Library/LaunchDaemons/edu.utah.biology.example3.plist /usr/local/bin/script3 \; WatchPaths /Library/Admin/launchdwatch \;


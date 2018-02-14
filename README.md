# mak.py

<pre>
Mac Army Knife.  Tool for system administrators to quickly and easily hack a Mac.
                                                    ,^.
                            /\                     /   \
                ,^.        / /                    /    /
                \  \      / /                    /    /
                 \\ \    / /                    /  ///
                  \\ \  / /                    /  ///
                   \  \/_/____________________/    /
                    `/                         \  /_____________
         __________/|  o    Mac Army Knife   o  |'              \
        |____________\_________________________/_________________\

I'm combining all of my Mac customization scripts into this script.  All of this info is
on the web scattered all over and a lot of this is just shortcuts to built-in commands.
Why?  I'm tired of looking it up on the web and making scripts or profiles or whatever.  I
just wanted a one stop shop as easy "System Preferences" but from the command line.

https://github.com/magnusviri/mak.py

Usage: mak.py [-d] [-o &lt;os_ver&gt;] command options

	-d            Debug.
	-o &lt;os_ver&gt;   When running this script on a computer with an OS different than the
	              target volume, specify the target volume OS here.

Commands
	ard
	disable_touristd
	hack_jamf_hooks
	help
	launchdaemon
	locatedb
	networksetup
	pref
	set_volume
	set_zone_ntp
	shell_paths
	systemsetup

For help
	mak.py help &lt;command name&gt;
	mak.py help all  # will display help for all commands

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; ard [-c] &lt;username[,username..]&gt; [setting[ setting..]]

	Configures ARD sharing for specific users and restarts the service.

	By default all priveledges are give.  Specify the specific priveledges to use less than all.

	-r  Remove all previous ARD priveledges from all users

	Settings:
		-ChangeSettings
		-ControlObserve
		-DeleteFiles
		-GenerateReports
		-ObserveOnly
		-OpenQuitApps
		-RestartShutDown
		-SendFiles
		-ShowObserve
		-TextMessages

	Examples:
		mak.py ard admin
		mak.py ard -r admin,james
		mak.py ard -r admin -ChangeSettings

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; disable_touristd

	Disables all possible tourist dialogs for the current OS.  This uses the pref action
	so see that for options (`mak.py help pref`)

	Examples:
		mak.py disable_touristd	        # disables tourist for current user
		mak.py disable_touristd -T      # disables tourist in /System/Library/User Template/English.lproj

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; hack_jamf_hooks

	Changes loginhook.sh checkJSSConnection from 0 to 6 (this waits for a network connection before the jamf any login policies will run).

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; launchdaemon &lt;plist_file&gt; &lt;program arg&gt; [&lt;program arg&gt;..] ; &lt;key&gt; &lt;value&gt; [&lt;key&gt; &lt;value&gt;..]

	plist_file must be of form /path/label.plist

	Array or dictionary items (like program arguments) must be terminated with ";" (don't forget to quote or escape it).

	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html
	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/plist.5.html
	https://en.wikipedia.org/wiki/Launchd

	Examples:
		mak.py launchdaemon example.plist echo hi \; StartCalendarInterval Hour 4 Minute 0 Weekday 0 \;
		mak.py launchdaemon example.plist echo hi \; StandardOutPath /var/log/complete_enrollment.log StandardErrorPath /var/log/complete_enrollment.err.log RunAtLoad 1
		mak.py launchdaemon example.plist echo hi \; WatchPaths /Library/Admin/launchdwatch \;

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; locatedb

	Loads locate db

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; networksetup ...

	This is just a shortcut to /usr/sbin/networksetup.  See `man networksetup` for options.

	Why?  Because I'll forget about networksetup otherwise (it's not like I use the command
	very much).

	Example:
		mak.py networksetup -setdnsservers Ethernet 172.20.120.20

------------------------------------------------------------------------------------------

Usage: mak.py pref [-dh|--help] [-p path] [-u username] Preference.Name[:Option]

	The following options specify which file to modify when the default is in the user
	level domain ("*.User.*")

    -p &lt;path&gt;       Path to the user directory
    -P &lt;path&gt;       Complete path to the plist file (all script path logic is skipped)
    -u &lt;username&gt;   For user defaults, use this username
    -T              Use template: "/System/Library/User Template/English.lproj"

	Supported settings:
		Clock.User.ShowSeconds - user domain (10.11)
		CrashReporter.User.Use_Notification_Center=&lt;1|0&gt; - ; 1 arg; user domain (10.11)
		Dock.User.DisableAllAnimations=&lt;float&gt; - ; 1 arg; user domain (10.11)
		Dock.User.autohide-delay=&lt;float&gt; - ; 1 arg; user domain (10.11)
		Dock.User.expose-animation-duration=&lt;float&gt; - ; 1 arg; user domain (10.11)
		Dock.User.launchanim=&lt;true|false&gt; - ; 1 arg; user domain (10.11)
		Finder.User.AppleShowAllExtensions=&lt;true|false&gt; - Advanced tab: Show all filename extensions; 1 arg; user domain (10.12)
		Finder.User.DisableAllAnimations=&lt;true|false&gt; - Disable animation when opening the Info window in Finder; 1 arg; user domain (10.11)
		Finder.User.FXDefaultSearchScope=&lt;SCev|SCcf|SCsp&gt; - Where to search, computer (SCev), current folder (SCcf), or previous scope (SCsp); 1 arg; user domain (10.12)
		Finder.User.FXEnableExtensionChangeWarning=&lt;true|false&gt; - Advanced tab: Show warning before changing an extension; 1 arg; user domain (10.12)
		Finder.User.FXEnableRemoveFromICloudDriveWarning=&lt;true|false&gt; - Advanced tab: Show warning before removing from iCloud Drive; 1 arg; user domain (10.12)
		Finder.User.FXRemoveOldTrashItems=&lt;true|false&gt; - Advanced tab: Remove items from the Trash after 30 days; 1 arg; user domain (10.12)
		Finder.User.FinderSpawnTab=&lt;true|false&gt; - General tab: Open folders in tabs intead of new windows; 1 arg; user domain (10.12)
		Finder.User.NewWindowTarget=&lt;PfCm|PfVo|PfHm|PfDe|PfDo|PfID|PfAF|PfLo&gt; - General tab: New Finder windows shows: PfCm - computer, PfVo - volume, PfHm - Home, PfDe - Desktop, PfDo - Documents, PfID - iCloud, PfAF - All Files, PfLo - Other; 1 arg; user domain (10.12)
		Finder.User.NewWindowTargetPath=&lt;file:///...&gt; - General tab: New Finder windows shows: PfCm - empty string, PfVo - /, PfHm - /Users/name/, PfDe - /Users/name/Desktop/, PfDo - /Users/name/Documents/, PfID - /Users/name/Library/Mobile%20Documents/com~apple~CloudDocs/, PfAF - /System/Library/CoreServices/Finder.app/Contents/Resources/MyLibraries/myDocuments.cannedSearch, Other - Anything; 1 arg; user domain (10.12)
		Finder.User.ShowExternalHardDrivesOnDesktop=&lt;true|false&gt; - General tab: Show External Hard Drives On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowHardDrivesOnDesktop=&lt;true|false&gt; - General tab: Show Hard Drives On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowMountedServersOnDesktop=&lt;true|false&gt; - General tab: Show Mounted Servers On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowPathbar=&lt;true|false&gt; - View menu: Show Pathbar; 1 arg; user domain (10.12)
		Finder.User.ShowRemovableMediaOnDesktop=&lt;true|false&gt; - General tab: Show Removable Media On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowStatusBar=&lt;true|false&gt; - View menu: Show Status Bar; 1 arg; user domain (10.12)
		Finder.User.ShowTabView=&lt;true|false&gt; - View menu: Show Tab View; 1 arg; user domain (10.12)
		Finder.User.WarnOnEmptyTrash=&lt;true|false&gt; - Advanced tab: Show warning before emptying the Trash; 1 arg; user domain (10.12)
		Finder.User._FXShowPosixPathInTitle=&lt;true|false&gt; - Shows full path in title; 1 arg; user domain (10.12)
		Finder.User._FXSortFoldersFirst=&lt;true|false&gt; - Advanced tab: Keep Folders on top when sorting by name; 1 arg; user domain (10.12)
		Gateway.Computer.GKAutoRearm=&lt;true|false&gt; - Turn off 30 day rearm ; 1 arg; user domain (10.11)
		Generic.Computer=&lt;domain&gt;=&lt;key&gt;=&lt;format&gt;=&lt;value&gt; - Generic computer preference; 4 args; user domain
		Generic.User=&lt;domain&gt;=&lt;key&gt;=&lt;format&gt;=&lt;value&gt; - Generic user preference; 4 args; user domain
		Generic.User.ByHost=&lt;domain&gt;=&lt;key&gt;=&lt;format&gt;=&lt;value&gt; - Generic user byhost preference; 4 args; user domain
		KeyAccess.Computer.Server=&lt;url&gt; - ; 1 arg; computer domain (10.11)
		Mouse.User.Click.Double - Configures mouse double click; user domain (10.11)
		Mouse.User.Click.Single - Configures mouse single click; user domain (10.11)
		Quicktime7.User.ProKey=1234-ABCD-1234-ABCD-1234 - Set QuickTime 7 Pro Registration Key; 1 arg; user/byhost domain (10.12)
		Quicktime7.User.ProName=Johnny Appleseed - Set QuickTime 7 Pro Name; 1 arg; user/byhost domain (10.12)
		Quicktime7.User.ProOrg=Organization - Set QuickTime 7 Pro Organization; 1 arg; user/byhost domain (10.12)
		Safari.User.HomePage=http://example.com - Set Safari's homepage; 1 arg; user domain (10.11)
		Safari.User.LastSafariVersionWithWelcomePage=&lt;string&gt; - Gets rid of the Welcome to Safari message; 1 arg; user domain (10.11)
		Safari.User.NewAndTabWindowBehavior=&lt;int&gt; - Sets what Safari shows in new tabs and windows; 1 arg; user domain (10.11)
		Safari.User.NewTabBehavior=&lt;int&gt; - Sets what Safari shows in new tabs; 1 arg; user domain (10.11)
		Safari.User.NewWindowBehavior=&lt;int&gt; - Sets what Safari shows in new windows; 1 arg; user domain (10.11)
		Safari.User.Show_Tabs_Status_Favorites=&lt;true|false&gt; - Turns on or off Tab, Status, and Favorites bar; 1 arg; user domain (10.11)
		Safari.User.WebKitInitialTimedLayoutDelay=&lt;float&gt; - ; 1 arg; user domain (10.11)
		ScreenSaver.Computer.Basic.Message=&lt;Message&gt; - Set the basic screensaver password; 1 arg; computer domain (10.11)
		ScreenSaver.Computer.Computer_Name_Clock - Turns on Clock for Computer Name Module; computer domain (10.11)
		ScreenSaver.User.Basic.Message=&lt;Message&gt; - Set the basic screensaver password; 1 arg; user/byhost domain (10.11)
		ScreenSaver.User.Computer_Name - Sets screensaver to Computer Name; user/byhost domain (10.11)
		ScreenSaver.User.Computer_Name_Clock - Turns on Clock for Computer Name Module; user/byhost domain (10.11)
		ScreenSaver.User.askForPassword=&lt;1|0&gt; - Set screensaver password; 1 arg: 0 off, 1 on; user domain (10.11)
		Screencapture.User.disable-shadow=&lt;true|false&gt; - ; 1 arg; user domain (10.11)
		SoftwareUpdate.Computer.AutoUpdate=&lt;true|false&gt; - "Install app updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.AutoUpdateRestartRequired=&lt;true|false&gt; - "Install macOS updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.AutomaticCheckEnabled=&lt;true|false&gt; - "Automatically check for updates"; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.AutomaticDownload=&lt;true|false&gt; - "Download newly available updates in the background", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.SetCatalogURL=&lt;http://example.com:8088/index.sucatalog&gt; - Sets the SoftwareUpdate CatalogURL, which must be a Mac OS X Server with the Software Update service activated; (10.12)
		SoftwareUpdate.Computer.SystemSecurityUpdates=&lt;true|false&gt; - "Install system data files and security updates", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)
		SystemUIServer.User.AirplayVisibility=&lt;true|false&gt; - ; user domain (10.12)
		SystemUIServer.User.DontAutoLoad=&lt;path of menu extra&gt; - ; user/byhost domain (10.11)
		SystemUIServer.User.DontAutoLoadReset - Erases all previous dont auto load items; user/byhost domain (10.11)
		Tourist.User.disable - Use the disable_touristd command, not the pref command ; user domain (any OS)

	Examples:
		mak.py pref SoftwareUpdate.Computer.AutoUpdate=false
		mak.py pref -p /Users/admin Clock.User.ShowSeconds
		mak.py pref -P /Users/admin/Library/Preferences/com.apple.menuextra.clock.plist Clock.User.ShowSeconds
		mak.py pref -u admin Clock.User.ShowSeconds
		mak.py pref -T Clock.User.ShowSeconds

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; set_volume &lt;Volume&gt; [&lt;Output Volume&gt;] [&lt;Input Volume&gt;]

	Sets the volume.  0 is muted, 3.5 is half, and 7 is the max.

	Examples:
		mak.py set_volume 0     # Muted
		mak.py set_volume 3.5   # Half
		mak.py set_volume 7     # Max

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; set_zone_ntp &lt;Zone&gt; &lt;ntp server&gt;

	Sets the timezone to &lt;Zone&gt; and the time server to &lt;ntp server&gt;.  For a list of
	timezones look in /usr/share/zoneinfo.

	Examples:
		mak.py set_zone_ntp America/Denver time.apple.com

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; shell_paths &lt;path&gt; &lt;name&gt;

	Adds the &lt;path&gt; to /private/etc/paths.d/&lt;name&gt;

	Example:
		mak.py shell_paths /usr/local/bin usr_local_bin

------------------------------------------------------------------------------------------

Usage: mak.py &lt;options&gt; systemsetup ...

	This is just a shortcut to /usr/sbin/systemsetup.  See `man systemsetup` for options.

	Why?  Because I'll forget about systemsetup otherwise (it's not like I use the command
	very much).

	Examples:
		mak.py systemsetup -settimezone America/Denver
		mak.py systemsetup -setusingnetworktime on
		mak.py systemsetup -setnetworktimeserver time.apple.com

------------------------------------------------------------------------------------------
</pre>

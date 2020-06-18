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

Usage: mak.py [-dv] command options

	-d            Debug (verbose + some things aren't executed)
	-v            Verbose
	--version     Print version and exit

Commands
	ard_user
	hack_jamf_hooks
	help
	launchdaemon
	locatedb
	networksetup
	pref
	scutil
	set_volume
	shell_paths
	systemsetup
	uvar

For help
	mak.py help &lt;command name&gt;
	mak.py help all  # will display help for all commands

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] ard_user [-c] &lt;username[,username..]&gt; [setting[ setting..]]

	Configures ARD sharing for specific users (all users is turned off) and restarts the
	service.

	-r  Remove all previous ARD priveledges from all users

	By default all priveledges are given.  Specify the specific priveledges to use less
	than all.

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
		mak.py ard_user admin
		mak.py ard_user -r                           # Removes all access
		mak.py ard_user -r admin,james               # Removes all access except users listed
		mak.py ard_user -r admin -ChangeSettings

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] hack_jamf_hooks [value]

	Changes loginhook.sh checkJSSConnection from 0 to either 6 (default) or what you specify.
	This waits for a network connection before any jamf login policies will run.

	By default the startup script will check 12 times, and logout checks 1 time.

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] launchdaemon [&lt;options&gt;] &lt;plist_file&gt; &lt;program arg&gt; [&lt;program arg&gt;..] [;|:] &lt;key&gt; &lt;value&gt; [&lt;key&gt; &lt;value&gt;..]

	-x don't unload and reload the plist with launchctl (the default will attempt to unload it if it exists, change the file, then reload)

	plist_file must be of form /path/label.plist

	Array or dictionary items (like program arguments) must be terminated with ";" (don't forget to quote or escape it) or ":".

	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html
	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/plist.5.html
	https://en.wikipedia.org/wiki/Launchd

	Examples:
		mak.py launchdaemon /Library/LaunchDaemons/example.plist echo hi \; StartCalendarInterval Hour 4 Minute 0 Weekday 0 \;
		mak.py launchdaemon /Library/LaunchDaemons/example.plist echo hi \; StandardOutPath /var/log/complete_enrollment.log StandardErrorPath /var/log/complete_enrollment.err.log RunAtLoad 1
		mak.py launchdaemon /Library/LaunchDaemons/example.plist echo hi \; WatchPaths /Library/Admin/launchdwatch \;
		mak.py launchdaemon /Library/LaunchAgents/example.plist /Applications/Safari.app/Contents/MacOS/Safari \; LimitLoadToSessionType Aqua RunAtLoad 1 \;

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] locatedb

	Loads locate db

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] networksetup ...

	This is just a shortcut to /usr/sbin/networksetup.  See `man networksetup` for options.

	Why?  Because I'll forget about networksetup otherwise (it's not like I use the command
	very much).

	Example:
		mak.py networksetup -setdnsservers Ethernet 172.20.120.20

------------------------------------------------------------------------------------------

Usage: mak.py pref [-dh|--help] [-o os] [-p path] [-u username] Preference.Name[=Option]

	-o &lt;os&gt;         Disregard the booted OS and use the specified OS instead (e.g. 10.x)

	The following options specify which file to modify when the default is in the user
	level domain ("*.User.*")

    -p &lt;path&gt;       Path to the preferences directory (used for user and computer prefs)
    -P &lt;path&gt;       Complete path to the plist file (all script path logic is skipped)
    -R              Use root: "/private/var/root/Library/Preferences/" (username is
                    "root", unless a -u comes after the -T)
    -T              Use template: "/System/Library/User Template/English.lproj" (username
                    is "root", unless a -u comes after the -T)
    -u &lt;username&gt;   For user defaults, use this username

	Supported settings:
		ARD.Text1 - (10.11-10.14)
		ARD.Text2 - (10.11-10.14)
		ARD.Text3 - (10.11-10.14)
		ARD.Text4 - (10.11-10.14)
		Clock.User.ShowSeconds - user domain (10.11-10.14)
		CrashReporter.User.Use_Notification_Center=&lt;1|0&gt; - ; 1 arg; user domain (10.11-10.14)
		Dock.User.DisableAllAnimations=&lt;float&gt; - ; 1 arg; user domain (10.11-10.14)
		Dock.User.autohide-delay=&lt;float&gt; - ; 1 arg; user domain (10.11-10.14)
		Dock.User.expose-animation-duration=&lt;float&gt; - ; 1 arg; user domain (10.11-10.14)
		Dock.User.launchanim=&lt;true|false&gt; - ; 1 arg; user domain (10.11-10.14)
		Finder.User.AppleShowAllExtensions=&lt;true|false&gt; - Advanced tab: Show all filename extensions; 1 arg; user domain (10.11-10.14)
		Finder.User.DisableAllAnimations=&lt;true|false&gt; - Disable animation when opening the Info window in Finder; 1 arg; user domain (10.11-10.14)
		Finder.User.FXDefaultSearchScope=&lt;SCev|SCcf|SCsp&gt; - Where to search, computer (SCev), current folder (SCcf), or previous scope (SCsp); 1 arg; user domain (10.11-10.14)
		Finder.User.FXEnableExtensionChangeWarning=&lt;true|false&gt; - Advanced tab: Show warning before changing an extension; 1 arg; user domain (10.11-10.14)
		Finder.User.FXEnableRemoveFromICloudDriveWarning=&lt;true|false&gt; - Advanced tab: Show warning before removing from iCloud Drive; 1 arg; user domain (10.11-10.14)
		Finder.User.FXRemoveOldTrashItems=&lt;true|false&gt; - Advanced tab: Remove items from the Trash after 30 days; 1 arg; user domain (10.11-10.14)
		Finder.User.FinderSpawnTab=&lt;true|false&gt; - General tab: Open folders in tabs intead of new windows; 1 arg; user domain (10.11-10.14)
		Finder.User.NewWindowTarget=&lt;PfCm|PfVo|PfHm|PfDe|PfDo|PfID|PfAF|PfLo&gt; - General tab: New Finder windows shows: PfCm - computer, PfVo - volume, PfHm - Home, PfDe - Desktop, PfDo - Documents, PfID - iCloud, PfAF - All Files, PfLo - Other; 1 arg; user domain (10.11-10.14)
		Finder.User.NewWindowTargetPath=&lt;file:///...&gt; - General tab: New Finder windows shows: PfCm - empty string, PfVo - /, PfHm - /Users/name/, PfDe - /Users/name/Desktop/, PfDo - /Users/name/Documents/, PfID - /Users/name/Library/Mobile%20Documents/com~apple~CloudDocs/, PfAF - /System/Library/CoreServices/Finder.app/Contents/Resources/MyLibraries/myDocuments.cannedSearch, Other - Anything; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowExternalHardDrivesOnDesktop=&lt;true|false&gt; - General tab: Show External Hard Drives On Desktop; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowHardDrivesOnDesktop=&lt;true|false&gt; - General tab: Show Hard Drives On Desktop; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowMountedServersOnDesktop=&lt;true|false&gt; - General tab: Show Mounted Servers On Desktop; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowPathbar=&lt;true|false&gt; - View menu: Show Pathbar; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowRemovableMediaOnDesktop=&lt;true|false&gt; - General tab: Show Removable Media On Desktop; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowStatusBar=&lt;true|false&gt; - View menu: Show Status Bar; 1 arg; user domain (10.11-10.14)
		Finder.User.ShowTabView=&lt;true|false&gt; - View menu: Show Tab View; 1 arg; user domain (10.11-10.14)
		Finder.User.WarnOnEmptyTrash=&lt;true|false&gt; - Advanced tab: Show warning before emptying the Trash; 1 arg; user domain (10.11-10.14)
		Finder.User._FXShowPosixPathInTitle=&lt;true|false&gt; - Shows full path in title; 1 arg; user domain (10.11-10.14)
		Finder.User._FXSortFoldersFirst=&lt;true|false&gt; - Advanced tab: Keep Folders on top when sorting by name; 1 arg; user domain (10.11-10.14)
		Gateway.Computer.GKAutoRearm=&lt;true|false&gt; - Turn off 30 day rearm ; 1 arg; (10.11-10.14)
		Generic.Computer=&lt;domain&gt;=&lt;key&gt;=&lt;format&gt;=&lt;value&gt; - Generic computer preference; 4 args;
		Generic.User=&lt;domain&gt;=&lt;key&gt;=&lt;format&gt;=&lt;value&gt; - Generic user preference; 4 args; user domain
		Generic.User.ByHost=&lt;domain&gt;=&lt;key&gt;=&lt;format&gt;=&lt;value&gt; - Generic user byhost preference; 4 args; user/byhost domain
		KeyAccess.Computer.Server=&lt;url&gt; - ; 1 arg; computer domain (10.11-10.14)
		Loginwindow.Computer.DisableScreenLockImmediate=&lt;true|false&gt; - Gets rid of the Lock Screen option in the Apple Menu. (10.13-10.14)
		Loginwindow.Computer.GuestEnabled=&lt;true|false&gt; - Enable/disable Guest user. (10.11-10.14)
		Loginwindow.Computer.Hide500Users=&lt;true|false&gt; - Hide uid 500 users. (10.11-10.14)
		Loginwindow.Computer.autoLoginUserScreenLocked=&lt;true|false&gt; - autoLoginUserScreenLocked. (10.11-10.14)
		Loginwindow.User.DeleteRelaunchAtLogin - Removes the TALAppsToRelaunchAtLogin so that nothing relaunches at the next login; user domain (10.11-10.14)
		Microsoft.Computer.AcknowledgeDataCollectionPolicy - Sets AcknowledgedDataCollectionPolicy so that it doesn't show the annoying dialog (10.11-10.14)
		Microsoft.User.AutoUpdateHowToCheck=Value - Sets AutoUpdate check method; Values are Manual, AutomaticCheck, and AutomaticDownload (10.11-10.14)
		Microsoft.User.SendAllTelemetryEnabled=&lt;true|false&gt; - Sets SendAllTelemetryEnabled (10.11-10.14)
		Mouse.User.Click.Double - Configures mouse double click; user domain (10.11-10.14)
		Mouse.User.Click.Single - Configures mouse single click; user domain (10.11-10.14)
		Quicktime7.User.ProKey=1234-ABCD-1234-ABCD-1234 - Set QuickTime 7 Pro Registration Key; 1 arg; user/byhost domain (10.11-10.14)
		Quicktime7.User.ProName=Johnny Appleseed - Set QuickTime 7 Pro Name; 1 arg; user/byhost domain (10.11-10.14)
		Quicktime7.User.ProOrg=Organization - Set QuickTime 7 Pro Organization; 1 arg; user/byhost domain (10.11-10.14)
		Safari.User.HomePage=http://example.com - Set Safari's homepage; 1 arg; user domain (10.11-10.14)
		Safari.User.LastSafariVersionWithWelcomePage=&lt;string&gt; - Gets rid of the Welcome to Safari message; 1 arg; user domain (10.11-10.14)
		Safari.User.NewAndTabWindowBehavior=&lt;int&gt; - Sets what Safari shows in new tabs and windows; 1 arg; user domain (10.11-10.14)
		Safari.User.NewTabBehavior=&lt;int&gt; - Sets what Safari shows in new tabs; 1 arg; user domain (10.11-10.14)
		Safari.User.NewWindowBehavior=&lt;int&gt; - Sets what Safari shows in new windows; 1 arg; user domain (10.11-10.14)
		Safari.User.Show_Tabs_Status_Favorites=&lt;true|false&gt; - Turns on or off Tab, Status, and Favorites bar; 1 arg; user domain (10.11-10.14)
		Safari.User.WebKitInitialTimedLayoutDelay=&lt;float&gt; - ; 1 arg; user domain (10.11-10.14)
		ScreenSaver.Computer.Basic.Message=&lt;Message&gt; - Set the basic screensaver password; 1 arg; computer domain (10.11-10.14)
		ScreenSaver.Computer.Computer_Name_Clock - Turns on Clock for Computer Name Module; computer domain (10.11-10.14)
		ScreenSaver.User.Basic.Message=&lt;Message&gt; - Set the basic screensaver password; 1 arg; user/byhost domain (10.11-10.14)
		ScreenSaver.User.Computer_Name - Sets screensaver to Computer Name; user/byhost domain (10.11-10.14)
		ScreenSaver.User.Computer_Name_Clock - Turns on Clock for Computer Name Module; user/byhost domain (10.11-10.14)
		ScreenSaver.User.askForPassword=&lt;1|0&gt; - Set screensaver password; 1 arg: 0 off, 1 on; user domain (10.11-10.14)
		Screencapture.User.disable-shadow=&lt;true|false&gt; - ; 1 arg; user domain (10.11-10.14)
		SetupAssistant.User.DidSeeAppearanceSetup=&lt;true|false&gt; - Hides login setup assistant; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeApplePaySetup=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeAvatarSetup=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeCloudSetup=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeePrivacy=&lt;true|false&gt; - Hides login setup assistant privacy question; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeSiriSetup=&lt;true|false&gt; - Hides login setup assistant Siri question; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeSyncSetup=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeSyncSetup2=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeTouchIDSetup=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeTrueTonePrivacy=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SetupAssistant.User.DidSeeiCloudLoginForStorageServices=&lt;true|false&gt; - ; 1 arg: true/false; user domain (10.14)
		SoftwareUpdate.Computer.AutoUpdate=&lt;true|false&gt; - "Install app updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: true/false; (10.11-10.14)
		SoftwareUpdate.Computer.AutoUpdateRestartRequired=&lt;true|false&gt; - "Install macOS updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: true/false; (10.11-10.14)
		SoftwareUpdate.Computer.AutomaticCheckEnabled=&lt;true|false&gt; - "Automatically check for updates"; 1 arg: true/false; (10.11-10.14)
		SoftwareUpdate.Computer.AutomaticDownload=&lt;true|false&gt; - "Download newly available updates in the background", requires AutomaticCheckEnabled; 1 arg: true/false; (10.11-10.14)
		SoftwareUpdate.Computer.SetCatalogURL=&lt;http://example.com:8088/index.sucatalog&gt; - Sets the SoftwareUpdate CatalogURL, which must be a Mac OS X Server with the Software Update service activated; (10.11-10.14)
		SoftwareUpdate.Computer.SystemSecurityUpdates=&lt;true|false&gt; - "Install system data files and security updates", requires AutomaticCheckEnabled; 1 arg: true/false; (10.11-10.14)
		SystemUIServer.User.AirplayVisibility=&lt;true|false&gt; - ; user domain (10.11-10.14)
		SystemUIServer.User.DontAutoLoad=&lt;path of menu extra&gt; - ; user/byhost domain (10.11-10.14)
		SystemUIServer.User.DontAutoLoadReset - Erases all previous dont auto load items; user/byhost domain (10.11-10.14)
		Time.Computer.Server - (10.11-10.14)
		Time.Computer.Zone - (10.11-10.14)
		Tourist.User.disable - Disables the blasted tourist thing; user domain (any OS)

	Examples:
		mak.py pref SoftwareUpdate.Computer.AutoUpdate=false
		mak.py pref -o 10.12 -p /Users/admin Clock.User.ShowSeconds
		mak.py pref -P /Users/admin/Library/Preferences/com.apple.menuextra.clock.plist Clock.User.ShowSeconds
		mak.py pref -u admin Clock.User.ShowSeconds
		mak.py pref -T Clock.User.ShowSeconds

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] scutil ...

	This is just a shortcut to /usr/sbin/scutil.  See `man scutil` for options.

	Why?  Because I'll forget about scutil otherwise (it's not like I use the command
	very much).

	Example:
		mak.py scutil --set ComputerName "alpha centauri"
		mak.py scutil --set HostName alpha
		mak.py scutil --set LocalHostName centauri
		mak.py scutil --get HostName

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] set_volume &lt;Volume&gt; [&lt;Output Volume&gt;] [&lt;Input Volume&gt;]

	Sets the speaker and microphone levels.

	&lt;Volume&gt; values are 0-7
	&lt;Output Volume&gt; values are 0-100
	&lt;Input Volume&gt; values are 0-100
	Use "-" to skip

	Examples:
		mak.py set_volume 0         # Muted
		mak.py set_volume 3.5 - 0   # Half, skip, microphone muted
		mak.py set_volume - 0 100   # skip, speaker muted, microphone max

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] shell_paths &lt;path&gt; &lt;name&gt;

	Adds the &lt;path&gt; to /private/etc/paths.d/&lt;name&gt;

	Example:
		mak.py shell_paths /usr/local/bin usr_local_bin

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] systemsetup ...

	This is just a shortcut to /usr/sbin/systemsetup.  See `man systemsetup` for options.

	Why?  Because I'll forget about systemsetup otherwise (it's not like I use the command
	very much).  systemsetup modifies time, sleep, sharing, and startup disks

	Examples:
		mak.py systemsetup -settimezone America/Denver
		mak.py systemsetup -setusingnetworktime on
		mak.py systemsetup -setnetworktimeserver time.apple.com

------------------------------------------------------------------------------------------

Usage: mak.py [&lt;options&gt;] uvar &lt;path&gt; &lt;variable&gt; &lt;value&gt; [&lt;backup extension&gt;]

	Unix VARiable.  This will search &lt;path&gt; for the first instance of "^&lt;variable&gt;" and
	change it to "&lt;variable&gt;&lt;value&gt;" if it's not set (using sed).  If "^&lt;variable&gt;"
	doesn't occur then "&lt;variable&gt;&lt;value&gt;" will be appended to the end (surrounded by
	linefeeds).

	The optional backup extension will save a backup with the specified extension.

	Examples:
		mak.py uvar /etc/postfix/main.cf relayhost " = example.com" .bak
		mak.py uvar /etc/ssh/sshd_config AllowUsers " james spencer" .bak
		mak.py uvar /etc/ssh/sshd_config XAuthLocation " /opt/X11/bin/xauth"

------------------------------------------------------------------------------------------
</pre>

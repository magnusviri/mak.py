# mak.py

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

I combined all of my Mac customization scripts into this script.

Usage: mak.py command options

Commands
	ard
	disable_touristd
	hack_jamf_hooks
	help
	locatedb
	launchdaemon
	network
	pref
	set_volume
	shell_paths
	systemsetup

For help
	mak.py help <command name>
	mak.py help all  # will display help for all commands

------------------------------------------------------------------------------------------

Usage: mak.py ard [-c] <username[,username..]> [setting[ setting..]]

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
Usage: mak.py disable_touristd

	Disables all possible tourist dialogs for the current OS.  This uses the pref action
	so see that for options (`mak.py help pref`)

	Example:
	mak.py disable_touristd	        # disables tourist for current user
	mak.py disable_touristd -T      # disables tourist in /System/Library/User Template/English.lproj
	
------------------------------------------------------------------------------------------
Usage: mak.py hack_jamf_hooks

	Changes loginhook.sh checkJSSConnection from 0 to 6 (this waits for a network connection before the jamf any login policies will run).
	
------------------------------------------------------------------------------------------
Usage: mak.py locatedb

	Loads locate db
	
------------------------------------------------------------------------------------------
Usage: mak.py launchdaemon <plist_file> <program arg> [<program arg>..] ; <key> <value> [<key> <value>..]

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
Usage: mak.py network ...?

	This one isn't done.
	
------------------------------------------------------------------------------------------
Usage: mak.py pref [-dh|--help] [-p path] [-u username] Preference.Name[:Option]

	The following options specify which file to modify when the default is in the user
	level domain ("*.User.*")

    -p <path>       Path to the user directory
    -P <path>       Complete path to the plist file (all script path logic is skipped)
    -u <username>   For user defaults, use this username
    -T              Use template: "/System/Library/User Template/English.lproj"

	Supported settings:
		Clock.User.ShowSeconds - user domain (10.11)
		CrashReporter.User.Use_Notification_Center=<1|0> - ; 1 arg; user domain (10.11)
		Dock.User.DisableAllAnimations=<float> - ; 1 arg; user domain (10.11)
		Dock.User.autohide-delay=<float> - ; 1 arg; user domain (10.11)
		Dock.User.expose-animation-duration=<float> - ; 1 arg; user domain (10.11)
		Dock.User.launchanim=<true|false> - ; 1 arg; user domain (10.11)
		Finder.User.AppleShowAllExtensions=<true|false> - Advanced tab: Show all filename extensions; 1 arg; user domain (10.12)
		Finder.User.DisableAllAnimations=<true|false> - Disable animation when opening the Info window in Finder; 1 arg; user domain (10.11)
		Finder.User.FXDefaultSearchScope=<SCev|SCcf|SCsp> - Where to search, computer (SCev), current folder (SCcf), or previous scope (SCsp); 1 arg; user domain (10.12)
		Finder.User.FXEnableExtensionChangeWarning=<true|false> - Advanced tab: Show warning before changing an extension; 1 arg; user domain (10.12)
		Finder.User.FXEnableRemoveFromICloudDriveWarning=<true|false> - Advanced tab: Show warning before removing from iCloud Drive; 1 arg; user domain (10.12)
		Finder.User.FXRemoveOldTrashItems=<true|false> - Advanced tab: Remove items from the Trash after 30 days; 1 arg; user domain (10.12)
		Finder.User.FinderSpawnTab=<true|false> - General tab: Open folders in tabs intead of new windows; 1 arg; user domain (10.12)
		Finder.User.NewWindowTarget=<PfCm|PfVo|PfHm|PfDe|PfDo|PfID|PfAF|PfLo> - General tab: New Finder windows shows: PfCm - computer, PfVo - volume, PfHm - Home, PfDe - Desktop, PfDo - Documents, PfID - iCloud, PfAF - All Files, PfLo - Other; 1 arg; user domain (10.12)
		Finder.User.NewWindowTargetPath=<file:///...> - General tab: New Finder windows shows: PfCm - empty string, PfVo - /, PfHm - /Users/name/, PfDe - /Users/name/Desktop/, PfDo - /Users/name/Documents/, PfID - /Users/name/Library/Mobile%20Documents/com~apple~CloudDocs/, PfAF - /System/Library/CoreServices/Finder.app/Contents/Resources/MyLibraries/myDocuments.cannedSearch, Other - Anything; 1 arg; user domain (10.12)
		Finder.User.ShowExternalHardDrivesOnDesktop=<true|false> - General tab: Show External Hard Drives On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowHardDrivesOnDesktop=<true|false> - General tab: Show Hard Drives On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowMountedServersOnDesktop=<true|false> - General tab: Show Mounted Servers On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowPathbar=<true|false> - View menu: Show Pathbar; 1 arg; user domain (10.12)
		Finder.User.ShowRemovableMediaOnDesktop=<true|false> - General tab: Show Removable Media On Desktop; 1 arg; user domain (10.12)
		Finder.User.ShowStatusBar=<true|false> - View menu: Show Status Bar; 1 arg; user domain (10.12)
		Finder.User.ShowTabView=<true|false> - View menu: Show Tab View; 1 arg; user domain (10.12)
		Finder.User.WarnOnEmptyTrash=<true|false> - Advanced tab: Show warning before emptying the Trash; 1 arg; user domain (10.12)
		Finder.User._FXShowPosixPathInTitle=<true|false> - Shows full path in title; 1 arg; user domain (10.12)
		Finder.User._FXSortFoldersFirst=<true|false> - Advanced tab: Keep Folders on top when sorting by name; 1 arg; user domain (10.12)
		Gateway.Computer.GKAutoRearm=<true|false> - Turn off 30 day rearm ; 1 arg; user domain (10.11)
		Generic.Computer=<domain>=<key>=<format>=<value> - Generic computer preference; 4 args; user domain
		Generic.User=<domain>=<key>=<format>=<value> - Generic user preference; 4 args; user domain
		Generic.User.ByHost=<domain>=<key>=<format>=<value> - Generic user byhost preference; 4 args; user domain
		KeyAccess.Computer.Server=<url> - ; 1 arg; computer domain (10.11)
		Mouse.User.Click.Double - Configures mouse double click; user domain (10.11)
		Mouse.User.Click.Single - Configures mouse single click; user domain (10.11)
		Quicktime7.User.ProKey=1234-ABCD-1234-ABCD-1234 - Set QuickTime 7 Pro Registration Key; 1 arg; user/byhost domain (10.12)
		Quicktime7.User.ProName=Johnny Appleseed - Set QuickTime 7 Pro Name; 1 arg; user/byhost domain (10.12)
		Quicktime7.User.ProOrg=Organization - Set QuickTime 7 Pro Organization; 1 arg; user/byhost domain (10.12)
		Safari.User.HomePage=http://example.com - Set Safari's homepage; 1 arg; user domain (10.11)
		Safari.User.LastSafariVersionWithWelcomePage=<string> - Gets rid of the Welcome to Safari message; 1 arg; user domain (10.11)
		Safari.User.NewAndTabWindowBehavior=<int> - Sets what Safari shows in new tabs and windows; 1 arg; user domain (10.11)
		Safari.User.NewTabBehavior=<int> - Sets what Safari shows in new tabs; 1 arg; user domain (10.11)
		Safari.User.NewWindowBehavior=<int> - Sets what Safari shows in new windows; 1 arg; user domain (10.11)
		Safari.User.Show_Tabs_Status_Favorites=<true|false> - Turns on or off Tab, Status, and Favorites bar; 1 arg; user domain (10.11)
		Safari.User.WebKitInitialTimedLayoutDelay=<float> - ; 1 arg; user domain (10.11)
		ScreenSaver.Computer.Basic.Message=<Message> - Set the basic screensaver password; 1 arg; computer domain (10.11)
		ScreenSaver.Computer.Computer_Name_Clock - Turns on Clock for Computer Name Module; computer domain (10.11)
		ScreenSaver.User.Basic.Message=<Message> - Set the basic screensaver password; 1 arg; user/byhost domain (10.11)
		ScreenSaver.User.Computer_Name - Sets screensaver to Computer Name; user/byhost domain (10.11)
		ScreenSaver.User.Computer_Name_Clock - Turns on Clock for Computer Name Module; user/byhost domain (10.11)
		ScreenSaver.User.askForPassword=<1|0> - Set screensaver password; 1 arg: 0 off, 1 on; user domain (10.11)
		Screencapture.User.disable-shadow=<true|false> - ; 1 arg; user domain (10.11)
		SoftwareUpdate.Computer.AutoUpdate=<true|false> - "Install app updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.AutoUpdateRestartRequired=<true|false> - "Install macOS updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.AutomaticCheckEnabled=<true|false> - "Automatically check for updates"; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.AutomaticDownload=<true|false> - "Download newly available updates in the background", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)
		SoftwareUpdate.Computer.SetCatalogURL=<http://example.com:8088/index.sucatalog> - Sets the SoftwareUpdate CatalogURL, which must be a Mac OS X Server with the Software Update service activated; (10.12)
		SoftwareUpdate.Computer.SystemSecurityUpdates=<true|false> - "Install system data files and security updates", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)
		SystemUIServer.User.AirplayVisibility=<true|false> - ; user domain (10.12)
		SystemUIServer.User.DontAutoLoad=<path of menu extra> - ; user/byhost domain (10.11)
		SystemUIServer.User.DontAutoLoadReset - Erases all previous dont auto load items; user/byhost domain (10.11)
		Tourist.User.disable - Use the disable_touristd command, not the pref command ; user domain (any OS)

	Example:
	mak.py pref SoftwareUpdate.Computer.AutoUpdate=false
	mak.py pref -p /Users/admin Clock.User.ShowSeconds
	mak.py pref -P /Users/admin/Library/Preferences/com.apple.menuextra.clock.plist Clock.User.ShowSeconds
	mak.py pref -u admin Clock.User.ShowSeconds
	mak.py pref -T Clock.User.ShowSeconds
	
------------------------------------------------------------------------------------------
Usage: mak.py <Volume> [<Output Volume>] [<Input Volume>]

	Sets the volume.  0 is muted, 3.5 is half, and 7 is the max.

	Example:
	mak.py set_volume 0     # Muted
	mak.py set_volume 3.5   # Half
	mak.py set_volume 7     # Max
	
------------------------------------------------------------------------------------------
Usage: mak.py <path> <name>

	Adds the <path> to /private/etc/paths.d/<name>

	Example:
	mak.py shell_paths /usr/local/bin usr_local_bin
	
------------------------------------------------------------------------------------------
Usage: mak.py <Zone> [<ntp server>]

	Sets the timezone to <Zone> and if specified, the time server to <ntp server>.
	For a list of timezones look in /usr/share/zoneinfo.

	Example:
	mak.py systemsetup America/Denver
	mak.py systemsetup America/Denver time.apple.com
	
------------------------------------------------------------------------------------------

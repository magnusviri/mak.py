#!/usr/bin/python
# encoding: utf-8

################################################################################
#
# Copyright (c) 2017 University of Utah
# All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appears in all copies and
# that both that copyright notice and this permission notice appear
# in supporting documentation, and that the name of The University
# of Utah not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission. This software is supplied as is without expressed or
# implied warranties of any kind.
#
################################################################################

import getopt
import os
import pwd
import re
import sys
from subprocess import Popen, PIPE
jamf = False
debug = False
target_os = None
mak_commands = {}

##########################################################################################

prefs = {
	#########
	# Clock #
	#########
	'Clock.User.ShowSeconds':{
		'help':'Clock.User.ShowSeconds - user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.menuextra.clock', 'args':['DateFormat', '-string', '\'EEE hh:mm:ss a\''], 'user':True, },
				],
			},
		},
	},
	#################
	# CrashReporter #
	#################
	'CrashReporter.User.Use_Notification_Center':{
		'help':'CrashReporter.User.Use_Notification_Center=<1|0> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.CrashReporter', 'args':['UseUNC', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	########
	# Dock #
	########
	'Dock.User.launchanim':{
		'help':'Dock.User.launchanim=<true|false> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Dock', 'args':['launchanim', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Dock.User.expose-animation-duration':{
		'help':'Dock.User.expose-animation-duration=<float> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Dock', 'args':['expose-animation-duration', '-float', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Dock.User.autohide-delay':{
		'help':'Dock.User.autohide-delay=<float> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Dock', 'args':['autohide-delay', '-float', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Dock.User.DisableAllAnimations':{
		'help':'Dock.User.DisableAllAnimations=<float> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Dock', 'args':['DisableAllAnimations', '-float', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	##########
	# Finder #
	##########
	'Finder.User.ShowTabView':{
		'help':'Finder.User.ShowTabView=<true|false> - View menu: Show Tab View; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowTabView', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.ShowPathbar':{
		'help':'Finder.User.ShowPathbar=<true|false> - View menu: Show Pathbar; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowPathbar', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.ShowStatusBar':{
		'help':'Finder.User.ShowStatusBar=<true|false> - View menu: Show Status Bar; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowStatusBar', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.ShowHardDrivesOnDesktop':{
		'help':'Finder.User.ShowHardDrivesOnDesktop=<true|false> - General tab: Show Hard Drives On Desktop; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowHardDrivesOnDesktop', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.ShowExternalHardDrivesOnDesktop':{
		'help':'Finder.User.ShowExternalHardDrivesOnDesktop=<true|false> - General tab: Show External Hard Drives On Desktop; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowExternalHardDrivesOnDesktop', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.ShowRemovableMediaOnDesktop':{
		'help':'Finder.User.ShowRemovableMediaOnDesktop=<true|false> - General tab: Show Removable Media On Desktop; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowRemovableMediaOnDesktop', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.ShowMountedServersOnDesktop':{
		'help':'Finder.User.ShowMountedServersOnDesktop=<true|false> - General tab: Show Mounted Servers On Desktop; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['ShowMountedServersOnDesktop', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.NewWindowTarget':{
		'help':'Finder.User.NewWindowTarget=<PfCm|PfVo|PfHm|PfDe|PfDo|PfID|PfAF|PfLo> - General tab: New Finder windows shows: PfCm - computer, PfVo - volume, PfHm - Home, PfDe - Desktop, PfDo - Documents, PfID - iCloud, PfAF - All Files, PfLo - Other; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['NewWindowTarget', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.NewWindowTargetPath':{
		'help':'Finder.User.NewWindowTargetPath=<file:///...> - General tab: New Finder windows shows: PfCm - empty string, PfVo - /, PfHm - /Users/name/, PfDe - /Users/name/Desktop/, PfDo - /Users/name/Documents/, PfID - /Users/name/Library/Mobile%20Documents/com~apple~CloudDocs/, PfAF - /System/Library/CoreServices/Finder.app/Contents/Resources/MyLibraries/myDocuments.cannedSearch, Other - Anything; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['NewWindowTargetPath', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.FinderSpawnTab':{
		'help':'Finder.User.FinderSpawnTab=<true|false> - General tab: Open folders in tabs intead of new windows; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['FinderSpawnTab', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.AppleShowAllExtensions':{
		'help':'Finder.User.AppleShowAllExtensions=<true|false> - Advanced tab: Show all filename extensions; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['AppleShowAllExtensions', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.FXEnableExtensionChangeWarning':{
		'help':'Finder.User.FXEnableExtensionChangeWarning=<true|false> - Advanced tab: Show warning before changing an extension; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['FXEnableExtensionChangeWarning', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.FXEnableRemoveFromICloudDriveWarning':{
		'help':'Finder.User.FXEnableRemoveFromICloudDriveWarning=<true|false> - Advanced tab: Show warning before removing from iCloud Drive; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['FXEnableRemoveFromICloudDriveWarning', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.WarnOnEmptyTrash':{
		'help':'Finder.User.WarnOnEmptyTrash=<true|false> - Advanced tab: Show warning before emptying the Trash; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['WarnOnEmptyTrash', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.FXRemoveOldTrashItems':{
		'help':'Finder.User.FXRemoveOldTrashItems=<true|false> - Advanced tab: Remove items from the Trash after 30 days; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['FXRemoveOldTrashItems', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User._FXSortFoldersFirst':{
		'help':'Finder.User._FXSortFoldersFirst=<true|false> - Advanced tab: Keep Folders on top when sorting by name; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['_FXSortFoldersFirst', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.FXDefaultSearchScope':{
		'help':'Finder.User.FXDefaultSearchScope=<SCev|SCcf|SCsp> - Where to search, computer (SCev), current folder (SCcf), or previous scope (SCsp); 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['FXDefaultSearchScope', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	# Other
# 	<key>NSNavLastCurrentDirectory</key>
# 	<string>/Applications</string>
# 	<key>NSNavLastRootDirectory</key>
# 	<string>/Applications</string>
	'Finder.User._FXShowPosixPathInTitle':{
		'help':'Finder.User._FXShowPosixPathInTitle=<true|false> - Shows full path in title; 1 arg; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['_FXShowPosixPathInTitle', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Finder.User.DisableAllAnimations':{
		'help':'Finder.User.DisableAllAnimations=<true|false> - Disable animation when opening the Info window in Finder; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.finder', 'args':['DisableAllAnimations', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	##############
	# Gatekeeper #
	##############
	'Gateway.Computer.GKAutoRearm':{ # https://www.cnet.com/how-to/how-to-disable-gatekeeper-permanently-on-os-x/
		'help':'Gateway.Computer.GKAutoRearm=<true|false> - Turn off 30 day rearm ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.security', 'args':['GKAutoRearm', '-bool', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	#################
	# Generic Prefs #
	#################
	'Generic.Computer':{
		'help':'Generic.Computer=<domain>=<key>=<format>=<value> - Generic computer preference; 4 args; user domain',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'arg_count':4, }, # ARG0 is the domain
				],
			},
		},
	},
	'Generic.User':{
		'help':'Generic.User=<domain>=<key>=<format>=<value> - Generic user preference; 4 args; user domain',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'user':True, 'arg_count':4, }, # ARG0 is the domain
				],
			},
		},
	},
	'Generic.User.ByHost':{
		'help':'Generic.User.ByHost=<domain>=<key>=<format>=<value> - Generic user byhost preference; 4 args; user domain',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'user':True, 'arg_count':4, }, # ARG0 is the domain
				],
			},
		},
	},
	#############
	# KeyAccess #
	#############
	'KeyAccess.Computer.Server':{
		'help':'KeyAccess.Computer.Server=<url> - ; 1 arg; computer domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.sassafras.KeyAccess', 'args':['host', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	#########
	# Mouse #
	#########
	'Mouse.User.Click.Double':{
		'help':'Mouse.User.Click.Double - Configures mouse double click; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.driver.AppleHIDMouse', 'args':['Button2', '-int', '2'], 'user':True, },
					{ 'domain':'com.apple.driver.AppleBluetoothMultitouch.mouse', 'args':['MouseButtonMode', '-string', 'TwoButton'], 'user':True, },
				],
			},
		},
	},
	'Mouse.User.Click.Single':{
		'help':'Mouse.User.Click.Single - Configures mouse single click; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.driver.AppleHIDMouse', 'args':['Button2', '-int', '1'], 'user':True, },
					{ 'domain':'com.apple.driver.AppleBluetoothMultitouch.mouse', 'args':['MouseButtonMode', '-string', 'OneButton'], 'user':True, },
				],
			},
		},
	},
	##############
	# QuickTime7 #
	##############
	'QuickTime7.User.ProName':{
		'help':'Quicktime7.User.ProName=Johnny Appleseed - Set QuickTime 7 Pro Name; 1 arg; user/byhost domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Name', '%ARG0%'], 'user':True, 'byhost':True, 'arg_count':1, },
				],
			},
		},
	},
	'QuickTime7.User.ProOrg':{
		'help':'Quicktime7.User.ProOrg=Organization - Set QuickTime 7 Pro Organization; 1 arg; user/byhost domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Organization', '%ARG0%'], 'user':True, 'byhost':True, 'arg_count':1, },
				],
			},
		},
	},
	'QuickTime7.User.ProKey':{
		'help':'Quicktime7.User.ProKey=1234-ABCD-1234-ABCD-1234 - Set QuickTime 7 Pro Registration Key; 1 arg; user/byhost domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Registration Key', '%ARG0%'], 'user':True, 'byhost':True, 'arg_count':1, },
				],
			},
		},
	},
	##########
	# Safari #
	##########
	'Safari.User.HomePage':{
		'help':'Safari.User.HomePage=http://example.com - Set Safari\'s homepage; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['HomePage', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Safari.User.NewTabBehavior':{
		'help':'Safari.User.NewTabBehavior=<int> - Sets what Safari shows in new tabs; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['NewTabBehavior', '-int', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Safari.User.NewWindowBehavior':{
		'help':'Safari.User.NewWindowBehavior=<int> - Sets what Safari shows in new windows; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['NewWindowBehavior', '-int', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Safari.User.NewTabAndWindowBehavior':{
		'help':'Safari.User.NewAndTabWindowBehavior=<int> - Sets what Safari shows in new tabs and windows; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['NewWindowBehavior', '-int', '%ARG0%'], 'user':True, 'arg_count':1, },
					{ 'domain':'com.apple.Safari', 'args':['NewTabBehavior', '-int', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Safari.User.Show_Tabs_Status_Favorites':{
		'help':'Safari.User.Show_Tabs_Status_Favorites=<true|false> - Turns on or off Tab, Status, and Favorites bar; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['AlwaysShowTabBar', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
					{ 'domain':'com.apple.Safari', 'args':['ShowOverlayStatusBar', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
					{ 'domain':'com.apple.Safari', 'args':['ShowFavoritesBar-v2', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Safari.User.LastSafariVersionWithWelcomePage':{
		'help':'Safari.User.LastSafariVersionWithWelcomePage=<string> - Gets rid of the Welcome to Safari message; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['LastSafariVersionWithWelcomePage-v2', '-string', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	'Safari.User.WebKitInitialTimedLayoutDelay':{
		'help':'Safari.User.WebKitInitialTimedLayoutDelay=<float> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.Safari', 'args':['WebKitInitialTimedLayoutDelay', '-float', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	#################
	# Screencapture #
	#################
	'Screencapture.User.disable-shadow':{
		'help':'Screencapture.User.disable-shadow=<true|false> - ; 1 arg; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.screencapture', 'args':['disable-shadow', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	###############
	# ScreenSaver #
	###############
	'ScreenSaver.Computer.Basic.Message':{
		'help':'ScreenSaver.Computer.Basic.Message=<Message> - Set the basic screensaver password; 1 arg; computer domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.ScreenSaver.Basic', 'args':['MESSAGE', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	'ScreenSaver.Computer.Computer_Name_Clock':{
		'help':'ScreenSaver.Computer.Computer_Name_Clock - Turns on Clock for Computer Name Module; computer domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.screensaver', 'args':['showClock', '-bool', 'true'], },
				],
			},
		},
	},
	'ScreenSaver.User.Basic.Message':{
		'help':'ScreenSaver.User.Basic.Message=<Message> - Set the basic screensaver password; 1 arg; user/byhost domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.ScreenSaver.Basic', 'args':['MESSAGE', '%ARG0%'], 'user':True, 'byhost':True, 'arg_count':1, },
				],
			},
		},
	},
	'ScreenSaver.User.Computer_Name':{
		'help':'ScreenSaver.User.Computer_Name - Sets screensaver to Computer Name; user/byhost domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.screensaver', 'args':['moduleDict', '-dict', 'path', '/System/Library/Frameworks/ScreenSaver.framework/Resources/Computer Name.saver'], 'user':True, 'byhost':True, },
				],
			},
		},
	},
	'ScreenSaver.User.Computer_Name_Clock':{
		'help':'ScreenSaver.User.Computer_Name_Clock - Turns on Clock for Computer Name Module; user/byhost domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.screensaver', 'args':['showClock', '-bool', 'true'], 'user':True, 'byhost':True, },
				],
			},
		},
	},
	'ScreenSaver.User.askForPassword':{
		'help':'ScreenSaver.User.askForPassword=<1|0> - Set screensaver password; 1 arg: 0 off, 1 on; user domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.screensaver', 'args':['askForPassword', '-int', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	##################
	# SoftwareUpdate #
	##################
	'SoftwareUpdate.Computer.SetCatalogURL':{
		'help':'SoftwareUpdate.Computer.SetCatalogURL=<http://example.com:8088/index.sucatalog> - Sets the SoftwareUpdate CatalogURL, which must be a Mac OS X Server with the Software Update service activated; (10.12)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.SoftwareUpdate', 'args':['CatalogURL', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	# https://derflounder.wordpress.com/2014/12/29/managing-automatic-app-store-and-os-x-update-installation-on-yosemite/
	'SoftwareUpdate.Computer.AutomaticCheckEnabled':{
		'help':'SoftwareUpdate.Computer.AutomaticCheckEnabled=<true|false> - "Automatically check for updates"; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.SoftwareUpdate', 'args':['AutomaticCheckEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	'SoftwareUpdate.Computer.AutomaticDownload':{
		'help':'SoftwareUpdate.Computer.AutomaticDownload=<true|false> - "Download newly available updates in the background", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.SoftwareUpdate', 'args':['AutomaticDownload', '-bool', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	'SoftwareUpdate.Computer.AutoUpdate':{
		'help':'SoftwareUpdate.Computer.AutoUpdate=<true|false> - "Install app updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.commerce', 'args':['AutoUpdate', '-bool', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	'SoftwareUpdate.Computer.AutoUpdateRestartRequired':{
		'help':'SoftwareUpdate.Computer.AutoUpdateRestartRequired=<true|false> - "Install macOS updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.commerce', 'args':['AutoUpdateRestartRequired', '-bool', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	'SoftwareUpdate.Computer.SystemSecurityUpdates':{
		'help':'SoftwareUpdate.Computer.SystemSecurityUpdates=<true|false> - "Install system data files and security updates", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.SoftwareUpdate', 'args':['ConfigDataInstall', '-bool', '%ARG0%'], 'arg_count':1, },
					{ 'domain':'com.apple.SoftwareUpdate', 'args':['CriticalUpdateInstall', '-bool', '%ARG0%'], 'arg_count':1, },
				],
			},
		},
	},
	##################
	# SystemUIServer #
	##################
	'SystemUIServer.User.DontAutoLoadReset':{
		'help':'SystemUIServer.User.DontAutoLoadReset - Erases all previous dont auto load items; user/byhost domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.systemuiserver', 'command':'delete', 'args':['dontAutoLoad'], 'user':True, 'byhost':True, },
				],
			},
		},
	},
	'SystemUIServer.User.DontAutoLoad':{
		'help':'SystemUIServer.User.DontAutoLoad=<path of menu extra> - ; user/byhost domain (10.11)',
		'versions':{
			'10.11':{
				'defaults':[
					{ 'domain':'com.apple.systemuiserver', 'args':['dontAutoLoad', '-array-add', '%ARG0%'], 'user':True, 'byhost':True, 'arg_count':1, },
				],
			},
		},
	},
	'SystemUIServer.User.AirplayVisibility':{
		'help':'SystemUIServer.User.AirplayVisibility=<true|false> - ; user domain (10.12)',
		'versions':{
			'10.12':{
				'defaults':[
					{ 'domain':'com.apple.systemuiserver', 'args':['NSStatusItem Visibile com.apple.menuextra.airplay', '-bool', '%ARG0%'], 'user':True, 'arg_count':1, },
				],
			},
		},
	},
	############
	# TouristD #
	############
	# This data is populated by disable_touristd
	'Tourist.User.disable':{
		'help':'Tourist.User.disable - Use the disable_touristd command, not the pref command ; user domain (any OS)',
		'versions':{
		},
	},
}

os_age = [ '10.12', '10.11', '10.10', '10.9', '10.8', '10.7', '10.6', '10.5', '10.4', '10.3', '10.2', '10.1', '10.0', '0' ]

##########################################################################################

mak_commands['ard'] = {
	'help':'ardHelp',
	'main':'ard',
}

def ardHelp(name):
	return '''Usage: %s <options> ard [-c] <username[,username..]> [setting[ setting..]]

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
		%s ard admin
		%s ard -r admin,james
		%s ard -r admin -ChangeSettings

''' % (name,name,name,name)

def ard(args):
	kickstart = '/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart';
	clear = False
	try:
		(optargs, args) = getopt.getopt(args, "-r")
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	for opt, arg in optargs:
		if opt in ("-r"):
			clear = True
	if len(args) <= 0:
		usage('Please specify user names to enable ard access', 'ard')

	if len(args) > 1:
		privs = []
		for arg in args[1:]:
			if arg in ['-ChangeSettings', '-ControlObserve', '-DeleteFiles', '-GenerateReports', '-ObserveOnly', '-OpenQuitApps', '-RestartShutDown', '-SendFiles', '-ShowObserve', '-TextMessages']:
				privs.append( arg )
			else:
				usage( 'Unknown setting: ' + arg, 'ard' )
		if '-ControlObserve' in privs and '-ObserveOnly' in privs:
			usage( 'Specify either -ControlObserve or -ObserveOnly but not both', 'ard' )
	else:
		privs = ['-ChangeSettings', '-ControlObserve', '-DeleteFiles', '-GenerateReports', '-OpenQuitApps', '-RestartShutDown', '-SendFiles', '-ShowObserve', '-TextMessages'];
	sh( kickstart + '-deactivate -configure -access -off' )
	sh( '/usr/bin/defaults write /Library/Preferences/com.apple.RemoteManagement ARD_AllLocalUsers -bool FALSE' )
	if clear:
		ard_users = sh( 'dscl . list /Users naprivs | awk \'{print $1}\'' )
		ard_users = ard_users.split("\n")
		for user in ard_users:
			if user != None and user != '':
				sh( 'dscl . delete /Users/' + user + ' naprivs' )
	sh( kickstart + ' -configure -allowAccessFor -specifiedUsers' )
	sh( kickstart + ' -configure -access -on -privs ' + ' '.join(privs) + ' -users ' + args[0] )
	sh( kickstart + ' -activate -restart -agent' )

##########################################################################################

mak_commands['disable_touristd'] = {
	'help':'disable_touristdHelp',
	'main':'disable_touristd',
}

def disable_touristdHelp(name):
	return '''Usage: %s <options> disable_touristd

	Disables all possible tourist dialogs for the current OS.  This uses the pref action
	so see that for options (`%s help pref`)

	Examples:
		%s disable_touristd	        # disables tourist for current user
		%s disable_touristd -T      # disables tourist in /System/Library/User Template/English.lproj

''' % (name,name,name,name)

def disable_touristd(args):
	#https://carlashley.com/2016/10/19/com-apple-touristd/
	text = sh( '/usr/libexec/PlistBuddy -c Print -x "/System/Library/PrivateFrameworks/Tourist.framework/Resources/Tours.plist" | grep https://' )
	text = text.split("\n")
	defaults_command = [ { 'domain':'com.apple.touristd', 'args':['firstOSLogin', '-date', '2018-1-1'], 'user':True, } ]
	for url in text:
		url = re.sub(r'.*<string>([^<]*).*', r'\1', url)
		defaults_command.append( { 'domain':'com.apple.touristd', 'args':['seed-'+url, '-date', '2018-1-1'], 'user':True, } )
	my_os = get_short_os_version()
	tourist_pref = {
		'help':'Tourist.User.disable - Disables the blasted tourist thing; user domain',
		'versions':{
			my_os:{
				'defaults':defaults_command
			}
		}
	}
	prefs['Tourist.User.disable'] = tourist_pref
	args.append( "Tourist.User.disable" )
	macosPref(args)

##########################################################################################

mak_commands['hack_jamf_hooks'] = {
	'help':'hack_jamf_hooksHelp',
	'main':'hack_jamf_hooks',
}

def hack_jamf_hooksHelp(name):
	return '''Usage: %s <options> hack_jamf_hooks

	Changes loginhook.sh checkJSSConnection from 0 to 6 (this waits for a network connection before the jamf any login policies will run).

''' % (name)

def hack_jamf_hooks(args):
	sh( 'sed -i .orig "s/checkJSSConnection -retry 0 ;/checkJSSConnection -retry 6 ;/g" /Library/Application\ Support/JAMF/ManagementFrameworkScripts/loginhook.sh' )

##########################################################################################

mak_commands['locatedb'] = {
	'help':'locatedbHelp',
	'main':'locatedb',
}

def locatedbHelp(name):
	return '''Usage: %s <options> locatedb

	Loads locate db

''' % (name)

def locatedb(args):
	sh( '/bin/launchctl load -w /System/Library/LaunchDaemons/com.apple.locate.plist' )

##########################################################################################

mak_commands['launchdaemon'] = {
	'help':'launchdaemonHelp',
	'main':'launchdaemon',
}

def launchdaemonHelp(name):
	return '''Usage: %s <options> launchdaemon <plist_file> <program arg> [<program arg>..] ; <key> <value> [<key> <value>..]

	plist_file must be of form /path/label.plist

	Array or dictionary items (like program arguments) must be terminated with \";\" (don't forget to quote or escape it).

	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html
	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/plist.5.html
	https://en.wikipedia.org/wiki/Launchd

	Examples:
		%s launchdaemon example.plist echo hi \; StartCalendarInterval Hour 4 Minute 0 Weekday 0 \;
		%s launchdaemon example.plist echo hi \; StandardOutPath /var/log/complete_enrollment.log StandardErrorPath /var/log/complete_enrollment.err.log RunAtLoad 1
		%s launchdaemon example.plist echo hi \; WatchPaths /Library/Admin/launchdwatch \;

''' % (name,name,name,name)

def parseLaunchdPlist(args):
	hash = dict()
	key1 = None
	key2 = None
	bucket = None
	for arg in args:
		if key1 == None:
			key1 = arg
		# String
		elif key1 in ['Label', 'WorkingDirectory', 'GroupName', 'StandardOutPath', 'StandardErrorPath', 'UserName']:
			hash[key1] = arg
			key1 = None
		# Bool
		elif key1 in ['OnDemand', 'HopefullyExitsFirst', 'SessionCreate', 'AbandonProcessGroup', 'EnableTransactions', 'RunAtLoad', 'LaunchOnlyOnce']:
			hash[key1] = False if arg == '0' else True
			key1 = None
		# Array
		elif key1 in ['ProgramArguments', 'WatchPaths']:
			if bucket == None:
				bucket = []
			if arg == ';':
				hash[key1] = bucket;
				key1 = None
				bucket = None
			else:
				bucket.append( arg )
		# Dict
		elif key1 in ['StartCalendarInterval']:
			if bucket == None:
				bucket = {}
			if arg == ';':
				hash[key1] = bucket;
				key1 = None
				key2 = None
				bucket = None
			else:
				if key2 == None:
					key2 = arg
				else:
					bucket[key2] = arg
					key2 = None
		elif key1 == 'KeepAlive':
			if arg == '0':
				hash[key1] = False;
				key1 = None
			elif arg == '1':
				hash[key1] = True;
				key1 = None
			else:
				usage( "KeepAlive Dictionary is not done.", 'launchdaemon' )
		else:
			usage( "Unknown key: "+key1, 'launchdaemon' )
	if bucket != None and len(bucket) > 0:
		usage( "Terminate multi-item values with \";\" (don't forget to escape it).", 'launchdaemon' )
	return hash

def launchdaemon(args):
	import plistlib
	if len(args) <= 3:
		usage( 'You must have a path, program arguments, and a trigger condition', 'launchdaemon' )
	path = args[0]
	label = re.sub(r'.*\/([^\/])\.plist$', r'\1', path)
	if label == '':
		usage('Could not build a label from the path, did the path end with ".plist"?', 'launchdaemon')
	if debug:
		print( "Label: "+label )
	flag = True
	program_args = []
	ii = 1
	while flag:
		if ii >= len(args):
			usage( 'You must terminate ProgramArguments items with ";" (don\'t forget to escape it).', 'launchdaemon' )
		if args[ii] != ';':
			if args[ii][-1] == ';':
				args[ii] = args[ii][:-1]
				flag = False
			program_args.append( args[ii] )
			ii += 1
		else:
			flag = False
	args = args[ii+1:]
	if debug:
		print( program_args )
		print( args )
	if os.path.exists( path ):
		sh( 'launchctl unload ' + path )
	plist = parseLaunchdPlist(args)
	plist['Label'] = label
	plist['ProgramArguments'] = program_args
	plistlib.writePlist( plist, path )
	sh( 'launchctl load ' + path )

##########################################################################################

mak_commands['networksetup'] = {
	'help':'networksetupHelp',
	'main':'networksetup',
}

def networksetupHelp(name):
	return '''Usage: %s <options> networksetup ...

	This is just a shortcut to /usr/sbin/networksetup.  See `man networksetup` for options.

	Why?  Because I'll forget about networksetup otherwise (it's not like I use the command
	very much).

	Example:
		%s networksetup -setdnsservers Ethernet 172.20.120.20

''' % (name,name)

def networksetup(args):
	sh( '/usr/sbin/networksetup ' + " ".join(args) )

##########################################################################################

mak_commands['pref'] = {
	'help':'prefHelp',
	'main':'pref',
}

def prefHelp(name):
	text = '''Usage: %s pref [-dh|--help] [-p path] [-u username] Preference.Name[:Option]

	The following options specify which file to modify when the default is in the user
	level domain ("*.User.*")

    -p <path>       Path to the user directory
    -P <path>       Complete path to the plist file (all script path logic is skipped)
    -u <username>   For user defaults, use this username
    -T              Use template: "/System/Library/User Template/English.lproj"

	Supported settings:
''' % (name)
	for pref, pref_data in sorted( prefs.iteritems() ):
		if 'help' in pref_data:
			text += "\t\t" + pref_data['help'] + "\n"

	text += '''
	Examples:
		%s pref SoftwareUpdate.Computer.AutoUpdate=false
		%s pref -p /Users/admin Clock.User.ShowSeconds
		%s pref -P /Users/admin/Library/Preferences/com.apple.menuextra.clock.plist Clock.User.ShowSeconds
		%s pref -u admin Clock.User.ShowSeconds
		%s pref -T Clock.User.ShowSeconds

''' % (name,name,name,name,name)
	return( text )

def pref(args):
	delimiter = '='
	try:
		(optargs, args) = getopt.getopt(args, "p:P:u:T")
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	for opt, arg in optargs:
		if opt in ("-u"):
			user = arg
		elif opt in ("-p"):
			userdir = arg
		elif opt in ("-P"):
			force_path = arg
		elif opt in ("-T"):
			userdir = '/System/Library/User Template/English.lproj'
	if len( args ) == 0:
		usage('You must specify arguments', 'pref')
	sys_args = args

	# Find the command for the OS
	cur_ii = find_os()
	commands = []
	not_found = ""

	found = False
	command_parts = args[0].split(delimiter, 1)


	if command_parts[0] in prefs:
		commands_for_this_os = prefs[command_parts[0]]['versions']
		ii = 0
		pref_os = ''
		for test_os in os_age:
			if test_os in commands_for_this_os:
				if cur_ii <= ii:
					pref_os = test_os
					break
			ii += 1
		if pref_os in commands_for_this_os:
			if 'defaults' in commands_for_this_os[pref_os]:
				defaults_commands = commands_for_this_os[pref_os]['defaults']
				for data in defaults_commands:
					if 'arg_count' in data and data['arg_count'] > 0:
						arg_parts = command_parts[1].split(delimiter, data['arg_count'])
					if 'domain' in data:
						domain = data['domain']
					else:
						domain = arg_parts[0]
					if 'force_path' in locals():
						path = force_path
					else:
						if 'user' in data:
							if not 'user' in locals():
								user = sh("/usr/bin/stat /dev/console | awk '{print $5}'").rstrip('\n')
							if not 'userdir' in locals():
								userdir = pwd.getpwnam(user).pw_dir
							if 'byhost' in data and data['byhost']:
								if not 'macUUID' in locals():
									macUUID = sh("ioreg -rd1 -c IOPlatformExpertDevice | grep -i 'UUID' | cut -c27-62").rstrip('\n')
								path = userdir + '/Library/Preferences/ByHost/' + domain + "." + macUUID + '.plist'
							else:
								path = userdir + '/Library/Preferences/' + domain + '.plist'
						else:
							path = '/Library/Preferences/' + domain + '.plist'
					command_type = 'write'
					if 'command' in data:
						command_type = data['command']
					command = [ '/usr/bin/defaults', command_type, path ]
					ii = 0
					if 'arg_parts' in locals():
						for arg_part in arg_parts:
							jj = 0
							for command_part in data['args']:
								data['args'][jj] = re.sub(r'%ARG'+str(ii)+'%', arg_part, command_part)
								jj += 1
							ii += 1
						command = command + data['args']
					else:
						for command_part in data['args']:
							command.append( command_part )
					if 'arg_count' in data and data['arg_count'] != ii:
						print( command )
						usage( pref_os + " expects " + str( data['arg_count'] ) + " argument(s) but only found " + str( ii ) + " argument(s).", 'pref' )
					commands.append( command )
					if 'user' in data and 'user' in locals() and user != '' and command_type == 'write':
						group = pwd.getpwnam(user).pw_gid
						commands.append( [ '/usr/sbin/chown', user + ":" + str(group), path ] )
					found = True
	if not found:
		not_found += "Can't find setting \"" + command_parts[0] + "\" (your OS: " + get_short_os_version() + ")\n"

	if len( not_found ) > 0:
		usage( not_found, 'pref' )

	for command in commands:
		if not debug:
			sh2( command )

##########################################################################################

mak_commands['set_volume'] = {
	'help':'set_volumeHelp',
	'main':'set_volume',
}

def set_volumeHelp(name):
	return '''Usage: %s <options> set_volume <Volume> [<Output Volume>] [<Input Volume>]

	Sets the volume.  0 is muted, 3.5 is half, and 7 is the max.

	Examples:
		%s set_volume 0     # Muted
		%s set_volume 3.5   # Half
		%s set_volume 7     # Max

''' % (name,name,name,name)

def set_volume(args):
	if len(args) > 0 and args[0] != "-":
		if debug:
			print "osascript -e 'set volume args[0]'\n"
		sh( "osascript -e 'set volume "+args[0]+"'" )

	if len(args) > 1 and args[1] != "-":
		if debug:
			print "osascript -e 'set volume output volume args[1]'\n"
		sh( "osascript -e 'set volume output volume "+args[1]+"'" )

	if len(args) > 2 and args[2] != "-":
		if debug:
			print "osascript -e 'set volume input volume args[2]'\n"
		sh( "osascript -e 'set volume input volume "+args[2]+"'" )

##########################################################################################

mak_commands['set_zone_ntp'] = {
	'help':'set_zone_ntpHelp',
	'main':'set_zone_ntp',
}

def set_zone_ntpHelp(name):
	return '''Usage: %s <options> set_zone_ntp <Zone> <ntp server>

	Sets the timezone to <Zone> and the time server to <ntp server>.  For a list of
	timezones look in /usr/share/zoneinfo.

	Examples:
		%s set_zone_ntp America/Denver time.apple.com

''' % (name,name)

def set_zone_ntp(args):
	systemsetup( '-settimezone', args[0] )
	systemsetup( '-setusingnetworktime', 'on' )
	systemsetup( '-setnetworktimeserver', args[1] )
	sh( 'ntpdate', '-u', args[1] )

##########################################################################################

mak_commands['shell_paths'] = {
	'help':'shell_pathsHelp',
	'main':'shell_paths',
}

def shell_pathsHelp(name):
	return '''Usage: %s <options> shell_paths <path> <name>

	Adds the <path> to /private/etc/paths.d/<name>

	Example:
		%s shell_paths /usr/local/bin usr_local_bin

''' % (name,name)

def shell_paths(args):
	print("shell_paths")
	search = args[0]
	if args[1] != '':
		path = '/private/etc/paths.d/' + args[1]
		if os.path.exists(search) and not os.path.exists(path):
			file = open(path, "w")
			file.write(search)
			file.close()

##########################################################################################

mak_commands['systemsetup'] = {
	'help':'systemsetupHelp',
	'main':'systemsetup',
}

def systemsetupHelp(name):
	return '''Usage: %s <options> systemsetup ...

	This is just a shortcut to /usr/sbin/systemsetup.  See `man systemsetup` for options.

	Why?  Because I'll forget about systemsetup otherwise (it's not like I use the command
	very much).

	Examples:
		%s systemsetup -settimezone America/Denver
		%s systemsetup -setusingnetworktime on
		%s systemsetup -setnetworktimeserver time.apple.com

''' % (name,name,name,name)

def systemsetup(args):
	sh( '/usr/sbin/systemsetup ' + " ".join(args) )

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def sh(cmd):
	if debug:
		print( cmd )
		result = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE).communicate()[0]
		if result != '':
			print( result )
		return result
	else:
		return Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE).communicate()[0]

def sh2(cmd):
	if debug:
		print( cmd )
		result = Popen(cmd).communicate()[0]
		if result != '':
			print( result )
		return result
	else:
		return Popen(cmd).communicate()[0]

def get_os_version():
	return sh("sw_vers -productVersion").rstrip('\n')

def get_short_os_version():
	return re.sub(r'(\d+\.\d+).*', r'\1', get_os_version())

def find_os():
	cur_os = get_short_os_version()
	cur_ii = -1
	ii = 0
	for test_os in os_age:
		if test_os == cur_os:
			cur_ii = ii
			break
		ii += 1
	return cur_ii

def usage(e=None,help_command=None):
	if e:
		print e
		print ""
	name = os.path.basename(sys.argv[0])
	text = ""
	if help_command == None or help_command == 'help' or help_command == 'all':
		text += '''Mac Army Knife.  Tool for system administrators to quickly and easily hack a Mac.
                                                    ,^.
                            /\\                     /   \\
                ,^.        / /                    /    /
                \\  \\      / /                    /    /
                 \\\\ \\    / /                    /  ///
                  \\\\ \\  / /                    /  ///
                   \\  \\/_/____________________/    /
                    `/                         \\  /_____________
         __________/|  o    Mac Army Knife   o  |'              \\
        |____________\\_________________________/_________________\\

I'm combining all of my Mac customization scripts into this script.  All of this info is
on the web scattered all over and a lot of this is just shortcuts to built-in commands.
Why?  I'm tired of looking it up on the web and making scripts or profiles or whatever.  I
just wanted a one stop shop as easy "System Preferences" but from the command line.

https://github.com/magnusviri/mak.py

Usage: %s [-d] [-o <os_ver>] command options

	-d            Debug.
	-o <os_ver>   When running this script on a computer with an OS different than the
	              target volume, specify the target volume OS here.

Commands
''' % (name)
		for mak_command, command_data in sorted( mak_commands.iteritems() ):
			text += "\t" + mak_command + "\n"
		text += '''
For help
	%s help <command name>
	%s help all  # will display help for all commands
''' % (name,name)
	if help_command == 'all':
		text += "\n------------------------------------------------------------------------------------------\n"
		for mak_command, command_data in sorted( mak_commands.iteritems() ):
			if 'help' in mak_commands[mak_command]:
				text += "\n"+globals()[mak_commands[mak_command]['help']](name)
				text += "------------------------------------------------------------------------------------------\n"
	elif help_command != None:
		text += globals()[mak_commands[help_command]['help']](name)
	if False:
		text = re.sub(r'<', r'&lt;', text)
		text = re.sub(r'>', r'&gt;', text)
	print( text )
	if e:
		sys.exit(64)
	else:
		sys.exit(0)

def main():
	if jamf:
		user = sys.argv[3]
		argv_start = 4
	else:
		argv_start = 1
	try:
		(optargs, args) = getopt.getopt(sys.argv[argv_start:], "do:")
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	global debug
	for opt, arg in optargs:
		if opt in ("-d"):
			debug = True
		elif opt in ("-o"):
			target_os = arg
	if len(args) <= 0:
		usage()
	command = args[0]
	if command == "help":
		if len(args) > 1:
			usage('', args[1])
		else:
			usage()
	else:
		if command in mak_commands and 'main' in mak_commands[command]:
			globals()[mak_commands[command]['main']](args[1:])
		else:
			usage('Unknown command: '+command)

if __name__ == '__main__':
	main()

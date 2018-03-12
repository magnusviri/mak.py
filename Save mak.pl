#!/usr/bin/perl -w

#
# This script saves /usr/local/bin/mak.py.
#
# This script is intended for Jamf.  Save this as a Jamf script and then create a policy
# that runs it on all computers once (reoccurring).  When you update the script, flush all
# the logs to push the script out again.  Be sure to double check there are no errors
# before you push it out each time.
#

use strict;

writefile_reload_launchdaemon( "/usr/local/bin/mak.py", $ARGV[3] );

sub writefile_reload_launchdaemon {
	open FILE, ">", $_[0];
	print FILE file_contents();
	close(FILE);
	system( "chmod 755 $_[0]" );
	if ( -e $_[0] and $_[0] =~ /.plist$/ ) {
		print "launchctl unload $_[1]\n";
		system "launchctl unload $_[1]";
		print "launchctl load $_[1]\n";
		system "launchctl load $_[1]";
	}
}

sub file_contents {

	# Escape \ and $

	return <<EOF;
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
verbose = False
target_os = None
mak_commands = {}

version = '1.1.0'

##########################################################################################

mak_commands['pref'] = {
	'help':'prefHelp',
	'main':'pref',
}

os_age = [ '10.13', '10.12', '10.11', '10.10', '10.9', '10.8', '10.7', '10.6', '10.5', '10.4', '10.3', '10.2', '10.1', '10.0', '0' ]

pref_delim = '='

def prefHelp(name):
	text = '''Usage: %s pref [-dh|--help] [-o os] [-p path] [-u username] Preference.Name[%sOption]

	-o <os>         Disregard the booted OS and use the specified OS instead (e.g. 10.x)

	The following options specify which file to modify when the default is in the user
	level domain ("*.User.*")

    -p <path>       Path to the preferences directory (used for user and computer prefs)
    -P <path>       Complete path to the plist file (all script path logic is skipped)
    -u <username>   For user defaults, use this username
    -T              Use template: "/System/Library/User Template/English.lproj" (username
                    is "root", unless -u comes after the -T)

	Supported settings:
''' % (name, pref_delim)
	for pref, pref_data in sorted( prefs.iteritems() ):
		if 'help' in pref_data:
			text += "\\t\\t" + pref_data['help'] + "\\n"

	text += '''
	Examples:
		%s pref SoftwareUpdate.Computer.AutoUpdate%sfalse
		%s pref -o 10.12 -p /Users/admin Clock.User.ShowSeconds
		%s pref -P /Users/admin/Library/Preferences/com.apple.menuextra.clock.plist Clock.User.ShowSeconds
		%s pref -u admin Clock.User.ShowSeconds
		%s pref -T Clock.User.ShowSeconds

''' % (name,pref_delim,name,name,name,name)
	return( text )

prefs = {
	#########
	# Clock #
	#########
	'Clock.User.ShowSeconds':{
		'help':'Clock.User.ShowSeconds - user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.menuextra.clock', 'args':['DateFormat', '-string', '\\'EEE hh:mm:ss a\\''], },
		],
	},
	#################
	# CrashReporter #
	#################
	'CrashReporter.User.Use_Notification_Center':{
		'help':'CrashReporter.User.Use_Notification_Center=<1|0> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.CrashReporter', 'args':['UseUNC', '%ARG0%'], 'arg_count':1, },
		],
	},
	########
	# Dock #
	########
	'Dock.User.launchanim':{
		'help':'Dock.User.launchanim'+pref_delim+'<true|false> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Dock', 'args':['launchanim', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Dock.User.expose-animation-duration':{
		'help':'Dock.User.expose-animation-duration'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Dock', 'args':['expose-animation-duration', '-float', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Dock.User.autohide-delay':{
		'help':'Dock.User.autohide-delay'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Dock', 'args':['autohide-delay', '-float', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Dock.User.DisableAllAnimations':{
		'help':'Dock.User.DisableAllAnimations'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Dock', 'args':['DisableAllAnimations', '-float', '%ARG0%'], 'arg_count':1, },
		],
	},
	##########
	# Finder #
	##########
	'Finder.User.ShowTabView':{
		'help':'Finder.User.ShowTabView'+pref_delim+'<true|false> - View menu: Show Tab View; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowTabView', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.ShowPathbar':{
		'help':'Finder.User.ShowPathbar'+pref_delim+'<true|false> - View menu: Show Pathbar; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowPathbar', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.ShowStatusBar':{
		'help':'Finder.User.ShowStatusBar'+pref_delim+'<true|false> - View menu: Show Status Bar; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowStatusBar', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.ShowHardDrivesOnDesktop':{
		'help':'Finder.User.ShowHardDrivesOnDesktop'+pref_delim+'<true|false> - General tab: Show Hard Drives On Desktop; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowHardDrivesOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.ShowExternalHardDrivesOnDesktop':{
		'help':'Finder.User.ShowExternalHardDrivesOnDesktop'+pref_delim+'<true|false> - General tab: Show External Hard Drives On Desktop; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowExternalHardDrivesOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.ShowRemovableMediaOnDesktop':{
		'help':'Finder.User.ShowRemovableMediaOnDesktop'+pref_delim+'<true|false> - General tab: Show Removable Media On Desktop; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowRemovableMediaOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.ShowMountedServersOnDesktop':{
		'help':'Finder.User.ShowMountedServersOnDesktop'+pref_delim+'<true|false> - General tab: Show Mounted Servers On Desktop; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowMountedServersOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.NewWindowTarget':{
		'help':'Finder.User.NewWindowTarget'+pref_delim+'<PfCm|PfVo|PfHm|PfDe|PfDo|PfID|PfAF|PfLo> - General tab: New Finder windows shows: PfCm - computer, PfVo - volume, PfHm - Home, PfDe - Desktop, PfDo - Documents, PfID - iCloud, PfAF - All Files, PfLo - Other; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['NewWindowTarget', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.NewWindowTargetPath':{
		'help':'Finder.User.NewWindowTargetPath'+pref_delim+'<file:///...> - General tab: New Finder windows shows: PfCm - empty string, PfVo - /, PfHm - /Users/name/, PfDe - /Users/name/Desktop/, PfDo - /Users/name/Documents/, PfID - /Users/name/Library/Mobile%20Documents/com~apple~CloudDocs/, PfAF - /System/Library/CoreServices/Finder.app/Contents/Resources/MyLibraries/myDocuments.cannedSearch, Other - Anything; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['NewWindowTargetPath', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.FinderSpawnTab':{
		'help':'Finder.User.FinderSpawnTab'+pref_delim+'<true|false> - General tab: Open folders in tabs intead of new windows; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['FinderSpawnTab', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.AppleShowAllExtensions':{
		'help':'Finder.User.AppleShowAllExtensions'+pref_delim+'<true|false> - Advanced tab: Show all filename extensions; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['AppleShowAllExtensions', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.FXEnableExtensionChangeWarning':{
		'help':'Finder.User.FXEnableExtensionChangeWarning'+pref_delim+'<true|false> - Advanced tab: Show warning before changing an extension; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXEnableExtensionChangeWarning', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.FXEnableRemoveFromICloudDriveWarning':{
		'help':'Finder.User.FXEnableRemoveFromICloudDriveWarning'+pref_delim+'<true|false> - Advanced tab: Show warning before removing from iCloud Drive; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXEnableRemoveFromICloudDriveWarning', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.WarnOnEmptyTrash':{
		'help':'Finder.User.WarnOnEmptyTrash'+pref_delim+'<true|false> - Advanced tab: Show warning before emptying the Trash; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['WarnOnEmptyTrash', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.FXRemoveOldTrashItems':{
		'help':'Finder.User.FXRemoveOldTrashItems'+pref_delim+'<true|false> - Advanced tab: Remove items from the Trash after 30 days; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXRemoveOldTrashItems', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User._FXSortFoldersFirst':{
		'help':'Finder.User._FXSortFoldersFirst'+pref_delim+'<true|false> - Advanced tab: Keep Folders on top when sorting by name; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['_FXSortFoldersFirst', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.FXDefaultSearchScope':{
		'help':'Finder.User.FXDefaultSearchScope'+pref_delim+'<SCev|SCcf|SCsp> - Where to search, computer (SCev), current folder (SCcf), or previous scope (SCsp); 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXDefaultSearchScope', '%ARG0%'], 'arg_count':1, },
		],
	},
	# Other
# 	<key>NSNavLastCurrentDirectory</key>
# 	<string>/Applications</string>
# 	<key>NSNavLastRootDirectory</key>
# 	<string>/Applications</string>
	'Finder.User._FXShowPosixPathInTitle':{
		'help':'Finder.User._FXShowPosixPathInTitle'+pref_delim+'<true|false> - Shows full path in title; 1 arg; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['_FXShowPosixPathInTitle', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Finder.User.DisableAllAnimations':{
		'help':'Finder.User.DisableAllAnimations'+pref_delim+'<true|false> - Disable animation when opening the Info window in Finder; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.finder', 'args':['DisableAllAnimations', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	##############
	# Gatekeeper #
	##############
	'Gateway.Computer.GKAutoRearm':{ # https://www.cnet.com/how-to/how-to-disable-gatekeeper-permanently-on-os-x/
		'help':'Gateway.Computer.GKAutoRearm'+pref_delim+'<true|false> - Turn off 30 day rearm ; 1 arg; (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.security', 'args':['GKAutoRearm', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	#################
	# Generic Prefs #
	#################
	'Generic.Computer':{
		'help':'Generic.Computer'+pref_delim+'<domain>'+pref_delim+'<key>'+pref_delim+'<format>'+pref_delim+'<value> - Generic computer preference; 4 args;',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'arg_count':4, }, # ARG0 is the domain
		],
	},
	'Generic.User':{
		'help':'Generic.User'+pref_delim+'<domain>'+pref_delim+'<key>'+pref_delim+'<format>'+pref_delim+'<value> - Generic user preference; 4 args; user domain',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'arg_count':4, }, # ARG0 is the domain
		],
	},
	'Generic.User.ByHost':{
		'help':'Generic.User.ByHost'+pref_delim+'<domain>'+pref_delim+'<key>'+pref_delim+'<format>'+pref_delim+'<value> - Generic user byhost preference; 4 args; user/byhost domain',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'byhost':True,
		'10.11':[
			{ 'type':'defaults', 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'arg_count':4, }, # ARG0 is the domain
		],
	},
	#############
	# KeyAccess #
	#############
	'KeyAccess.Computer.Server':{
		'help':'KeyAccess.Computer.Server'+pref_delim+'<url> - ; 1 arg; computer domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.sassafras.KeyAccess', 'args':['host', '%ARG0%'], 'arg_count':1, },
		],
	},
	#########
	# Mouse #
	#########
	'Mouse.User.Click.Double':{
		'help':'Mouse.User.Click.Double - Configures mouse double click; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.driver.AppleHIDMouse', 'args':['Button2', '-int', '2'], },
			{ 'type':'defaults', 'domain':'com.apple.driver.AppleBluetoothMultitouch.mouse', 'args':['MouseButtonMode', '-string', 'TwoButton'], },
		],
	},
	'Mouse.User.Click.Single':{
		'help':'Mouse.User.Click.Single - Configures mouse single click; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.driver.AppleHIDMouse', 'args':['Button2', '-int', '1'], },
			{ 'type':'defaults', 'domain':'com.apple.driver.AppleBluetoothMultitouch.mouse', 'args':['MouseButtonMode', '-string', 'OneButton'], },
		],
	},
	##############
	# QuickTime7 #
	##############
	'QuickTime7.User.ProName':{
		'help':'Quicktime7.User.ProName'+pref_delim+'Johnny Appleseed - Set QuickTime 7 Pro Name; 1 arg; user/byhost domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'byhost':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Name', '%ARG0%'], 'arg_count':1, },
		],
	},
	'QuickTime7.User.ProOrg':{
		'help':'Quicktime7.User.ProOrg'+pref_delim+'Organization - Set QuickTime 7 Pro Organization; 1 arg; user/byhost domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'byhost':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Organization', '%ARG0%'], 'arg_count':1, },
		],
	},
	'QuickTime7.User.ProKey':{
		'help':'Quicktime7.User.ProKey'+pref_delim+'1234-ABCD-1234-ABCD-1234 - Set QuickTime 7 Pro Registration Key; 1 arg; user/byhost domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'byhost':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Registration Key', '%ARG0%'], 'arg_count':1, },
		],
	},
	##########
	# Safari #
	##########
	'Safari.User.HomePage':{
		'help':'Safari.User.HomePage'+pref_delim+'http://example.com - Set Safari\\'s homepage; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['HomePage', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Safari.User.NewTabBehavior':{
		'help':'Safari.User.NewTabBehavior'+pref_delim+'<int> - Sets what Safari shows in new tabs; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewTabBehavior', '-int', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Safari.User.NewWindowBehavior':{
		'help':'Safari.User.NewWindowBehavior'+pref_delim+'<int> - Sets what Safari shows in new windows; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewWindowBehavior', '-int', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Safari.User.NewTabAndWindowBehavior':{
		'help':'Safari.User.NewAndTabWindowBehavior'+pref_delim+'<int> - Sets what Safari shows in new tabs and windows; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewWindowBehavior', '-int', '%ARG0%'], 'arg_count':1, },
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewTabBehavior', '-int', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Safari.User.Show_Tabs_Status_Favorites':{
		'help':'Safari.User.Show_Tabs_Status_Favorites'+pref_delim+'<true|false> - Turns on or off Tab, Status, and Favorites bar; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['AlwaysShowTabBar', '-bool', '%ARG0%'], 'arg_count':1, },
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['ShowOverlayStatusBar', '-bool', '%ARG0%'], 'arg_count':1, },
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['ShowFavoritesBar-v2', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Safari.User.LastSafariVersionWithWelcomePage':{
		'help':'Safari.User.LastSafariVersionWithWelcomePage'+pref_delim+'<string> - Gets rid of the Welcome to Safari message; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['LastSafariVersionWithWelcomePage-v2', '-string', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Safari.User.WebKitInitialTimedLayoutDelay':{
		'help':'Safari.User.WebKitInitialTimedLayoutDelay'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.Safari', 'args':['WebKitInitialTimedLayoutDelay', '-float', '%ARG0%'], 'arg_count':1, },
		],
	},
	#################
	# Screencapture #
	#################
	'Screencapture.User.disable-shadow':{
		'help':'Screencapture.User.disable-shadow'+pref_delim+'<true|false> - ; 1 arg; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.screencapture', 'args':['disable-shadow', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	###############
	# ScreenSaver #
	###############
	'ScreenSaver.Computer.Basic.Message':{
		'help':'ScreenSaver.Computer.Basic.Message'+pref_delim+'<Message> - Set the basic screensaver password; 1 arg; computer domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.ScreenSaver.Basic', 'args':['MESSAGE', '%ARG0%'], 'arg_count':1, },
		],
	},
	'ScreenSaver.Computer.Computer_Name_Clock':{
		'help':'ScreenSaver.Computer.Computer_Name_Clock - Turns on Clock for Computer Name Module; computer domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['showClock', '-bool', 'true'], },
		],
	},
	'ScreenSaver.User.Basic.Message':{
		'help':'ScreenSaver.User.Basic.Message'+pref_delim+'<Message> - Set the basic screensaver password; 1 arg; user/byhost domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'byhost':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.ScreenSaver.Basic', 'args':['MESSAGE', '%ARG0%'], 'arg_count':1, },
		],
	},
	'ScreenSaver.User.Computer_Name':{
		'help':'ScreenSaver.User.Computer_Name - Sets screensaver to Computer Name; user/byhost domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'byhost':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['moduleDict', '-dict', 'path', '/System/Library/Frameworks/ScreenSaver.framework/Resources/Computer Name.saver'], },
		],
	},
	'ScreenSaver.User.Computer_Name_Clock':{
		'help':'ScreenSaver.User.Computer_Name_Clock - Turns on Clock for Computer Name Module; user/byhost domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'byhost':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['showClock', '-bool', 'true'], },
		],
	},
	'ScreenSaver.User.askForPassword':{
		'help':'ScreenSaver.User.askForPassword'+pref_delim+'<1|0> - Set screensaver password; 1 arg: 0 off, 1 on; user domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'user':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['askForPassword', '-int', '%ARG0%'], 'arg_count':1, },
		],
	},
	##################
	# SoftwareUpdate #
	##################
	'SoftwareUpdate.Computer.SetCatalogURL':{
		'help':'SoftwareUpdate.Computer.SetCatalogURL'+pref_delim+'<http://example.com:8088/index.sucatalog> - Sets the SoftwareUpdate CatalogURL, which must be a Mac OS X Server with the Software Update service activated; (10.12)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['CatalogURL', '%ARG0%'], 'arg_count':1, },
		],
	},
	# https://derflounder.wordpress.com/2014/12/29/managing-automatic-app-store-and-os-x-update-installation-on-yosemite/
	'SoftwareUpdate.Computer.AutomaticCheckEnabled':{
		'help':'SoftwareUpdate.Computer.AutomaticCheckEnabled'+pref_delim+'<true|false> - "Automatically check for updates"; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['AutomaticCheckEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'SoftwareUpdate.Computer.AutomaticDownload':{
		'help':'SoftwareUpdate.Computer.AutomaticDownload'+pref_delim+'<true|false> - "Download newly available updates in the background", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['AutomaticDownload', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'SoftwareUpdate.Computer.AutoUpdate':{
		'help':'SoftwareUpdate.Computer.AutoUpdate'+pref_delim+'<true|false> - "Install app updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.commerce', 'args':['AutoUpdate', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'SoftwareUpdate.Computer.AutoUpdateRestartRequired':{
		'help':'SoftwareUpdate.Computer.AutoUpdateRestartRequired'+pref_delim+'<true|false> - "Install macOS updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.commerce', 'args':['AutoUpdateRestartRequired', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	'SoftwareUpdate.Computer.SystemSecurityUpdates':{
		'help':'SoftwareUpdate.Computer.SystemSecurityUpdates'+pref_delim+'<true|false> - "Install system data files and security updates", requires AutomaticCheckEnabled; 1 arg: 0 off, 1 on; (10.12)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['ConfigDataInstall', '-bool', '%ARG0%'], 'arg_count':1, },
			{ 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['CriticalUpdateInstall', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	##################
	# SystemUIServer #
	##################
	'SystemUIServer.User.DontAutoLoadReset':{
		'help':'SystemUIServer.User.DontAutoLoadReset - Erases all previous dont auto load items; user/byhost domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'byhost':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.systemuiserver', 'command':'delete', 'args':['dontAutoLoad'], },
		],
	},
	'SystemUIServer.User.DontAutoLoad':{
		'help':'SystemUIServer.User.DontAutoLoad'+pref_delim+'<path of menu extra> - ; user/byhost domain (10.11)',
		'versions':{ '10.11':'10.11', '10.12':'10.11', '10.13':'10.11', },
		'byhost':True,
		'10.11':[
			{ 'type':'defaults', 'domain':'com.apple.systemuiserver', 'args':['dontAutoLoad', '-array-add', '%ARG0%'], 'arg_count':1, },
		],
	},
	'SystemUIServer.User.AirplayVisibility':{
		'help':'SystemUIServer.User.AirplayVisibility'+pref_delim+'<true|false> - ; user domain (10.12)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'user':True,
		'10.12':[
			{ 'type':'defaults', 'domain':'com.apple.systemuiserver', 'args':['NSStatusItem Visibile com.apple.menuextra.airplay', '-bool', '%ARG0%'], 'arg_count':1, },
		],
	},
	############
	# Time #
	############
	'Time.Computer.Server':{
		'help':'Time.Computer.Server - (10.11)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'10.12':[
			{ 'type':'function', 'function':'systemsetup', 'args':['-setusingnetworktime', 'on'], },
			{ 'type':'function', 'function':'systemsetup', 'args':['-setnetworktimeserver', '%ARG0%'], 'arg_count':1, },
			{ 'type':'function', 'function':'sh2', 'args':['/usr/sbin/ntpdate', '-u', '%ARG0%'], 'arg_count':1, },
		],
	},
	'Time.Computer.Zone':{
		'help':'Time.Computer.Zone - (10.11)',
		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
		'10.12':[
			{ 'type':'function', 'function':'systemsetup', 'args':['-settimezone', '%ARG0%'], 'arg_count':1, },
		],
	},
	############
	# TouristD #
	############
	'Tourist.User.disable':{
		'help':'Tourist.User.disable - Disables the blasted tourist thing; user domain (any OS)',
		'user':True,
		'pre_run_func':'disable_touristd',
		# This data is populated by disable_touristd
	},

# 	#################
# 	# Function.Test #
# 	#################
# 	'Function.Test':{
# 		'help':'Test',
# 		'versions':{ '10.11':'10.12', '10.12':'10.12', '10.13':'10.12', },
# 		'user':True,
# 		'10.12':[
# 			{ 'type':'function', 'function':'say', 'args':['%ARG1%', 'and', '%ARG0%'], 'arg_count':2, },
# 		],
# 	},

}

def substitute_arguments(data, command_parts, pref_os):
	if 'args' in data:
		command_args = data['args']
		if 'arg_count' in data and data['arg_count'] > 0:
			if len(command_parts) <= 1:
				usage( 'This preference requires ' + str(data['arg_count']) + ' argument(s) separated by a "'+pref_delim+'", e.g. "' + command_parts[0] + pref_delim+'<value>"', 'pref' )
				sys.exit(1)
			arg_parts = command_parts[1].split(pref_delim, data['arg_count'])
			ii = 0
			for arg_part in arg_parts:
				jj = 0
				for command_part in command_args:
					command_args[jj] = re.sub(r'%ARG'+str(ii)+'%', arg_part, command_part)
					jj += 1
				ii += 1
			if data['arg_count'] != ii:
				usage( command_parts[0] + ' for ' + pref_os + ' requires ' + str( data['arg_count'] ) + ' argument(s) but found ' + str( ii ) + '.', 'pref' )
		return command_args
	else:
		return None

def get_usersname():
	if verbose:
		print 'Finding the logged in user'
	return sh("/usr/bin/stat /dev/console | awk '{print \$5}'").rstrip('\\n')

def get_pref_dir(user_dir, username, macUUID):
	if username != None:
		if user_dir == None:
			try:
				user_dir = pwd.getpwnam(username).pw_dir
			except:
				print "Could not find username: " + username
				sys.exit(1)
		pref_dir = user_dir + '/Library/Preferences/'
		if macUUID != None:
			pref_dir += 'ByHost/'
		return pref_dir
	else:
		return '/Library/Preferences/'

def get_domain(data, command_parts):
	if 'domain' in data:
		return data['domain']
	elif 'arg_count' in data and data['arg_count'] > 0:
		arg_parts = command_parts[1].split(pref_delim, data['arg_count'])
		return arg_parts[0]
	else:
		return ''

def get_macUUID():
	if verbose:
		print 'Finding the ByHost UUID'
	return sh("ioreg -rd1 -c IOPlatformExpertDevice | grep -i 'UUID' | cut -c27-62").rstrip('\\n')

def pref(args):
	pref_os = None
	force_path = None
	username = None
	user_dir = None
	pref_dir = None
	macUUID = None
	try:
		(optargs, rargs) = getopt.getopt(args, 'o:p:P:u:T')
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	for opt, arg in optargs:
		if opt == '-u':
			username = arg
		elif opt == '-o':
			pref_os = arg
		elif opt == '-p':
			pref_dir = arg
		elif opt == '-P':
			force_path = arg
		elif opt == '-T':
			user_dir = '/System/Library/User Template/English.lproj'
			username = 'root'
	if len( rargs ) == 0:
		usage('You must specify arguments', 'pref')
	sys_args = rargs

	# Make sure the command exists
	command_parts = rargs[0].split(pref_delim, 1)
	command_name = command_parts[0]
	if not command_name in prefs:
		usage('Can\\'t find setting "' + command_name, 'pref')
	command_prefs = prefs[command_name]

	# Pre-run stuff
	if 'pre_run_func' in command_prefs:
		pre_run_func = command_prefs['pre_run_func']
		print pre_run_func
		if pre_run_func in globals():
			globals()[pre_run_func]()
		else:
			print 'Script error: there is no function named "' + pre_run_func + '"'
			sys.exit(1)

	# Find the commands for this OS
	if not 'versions' in command_prefs:
		print 'Script error: "versions" key missing from hash for "' + command_name + '"'
		sys.exit(1)
	versions_hash = command_prefs['versions']
	if verbose:
		print 'Finding the OS'
	if pref_os == None:
		pref_os = get_short_os_version()
	if not pref_os in versions_hash:
		usage('Can\\'t find setting "' + command_name + '" (OS: ' + pref_os + ')', 'pref')
	os_pref_name = versions_hash[pref_os]
	if not os_pref_name in command_prefs:
		print 'Script error: "' + os_pref_name + '" key missing from hash for "' + command_name + '"'
		sys.exit(1)

	# The list of commands
	run_these_commands = command_prefs[os_pref_name]

	# Get username info
	if 'byhost' in command_prefs and command_prefs['byhost']:
		macUUID = get_macUUID()
	if macUUID != None or ('user' in command_prefs and command_prefs['user']):
		if username == None:
			username = get_usersname()
		# Get the group for chown
		try:
			group = str(pwd.getpwnam(username).pw_gid)
		except:
			print "Could not find username: " + username
			sys.exit(1)
	else:
		username = None

	# Flush out the commands
	commands = []
	chown_these_files = {}
	for data in run_these_commands:
		command_args = substitute_arguments(data, command_parts, pref_os)
		if 'type' in data:

			# Defaults
			if data['type'] == 'defaults':

				# Complete the path to the preferences
				if force_path != None:
					pref_path = force_path
				else:
					if pref_dir == None:
						pref_dir = get_pref_dir(user_dir, username, macUUID)
					domain = get_domain(data, command_parts)
					if macUUID != None:
						pref_path = pref_dir + domain + '.' + macUUID + '.plist'
					else:
						pref_path = pref_dir + domain + '.plist'

				# defaults command type (write or delete)
				command_type = 'write'
				if 'command' in data:
					command_type = data['command']

				# The command
				command = [ '/usr/bin/defaults', command_type, pref_path ]
				if command_args != None:
					command = command + command_args
				commands.append( command )

				# Add a chown if it's in the user homedir
				if username != None and command_type == 'write':
					chown_these_files[pref_path] = [ '/usr/sbin/chown', username + ':' + group, pref_path ]

			# Function
			elif data['type'] == 'function':
				if not 'function' in data:
					print 'Script error: specify a function named for this command.'
					sys.exit(1)
				main_name = data['function']
				if main_name in globals():
					if command_args != None:
						if debug:
							print "Debug: " + main_name + '('+str(command_args)+')'
						else:
							globals()[main_name](command_args)
					else:
						if debug:
							print "Debug: " + main_name + '()'
						else:
							globals()[main_name]()
				else:
					print 'Script error: there is no function named "' + main_name + '"'
					sys.exit(1)

	for file in chown_these_files:
		commands.append( chown_these_files[file] )

	for command in commands:
		if debug:
			print "Debug: " + str(command)
		else:
			sh2( command )

def say(args):
	sh("say " + ' '.join(args))

##########################################################################################

def disable_touristd():
	#https://carlashley.com/2016/10/19/com-apple-touristd/
	text = sh( '/usr/libexec/PlistBuddy -c Print -x "/System/Library/PrivateFrameworks/Tourist.framework/Resources/Tours.plist" | grep https://' )
	text = text.split("\\n")
	defaults_command = [ { 'type':'defaults', 'domain':'com.apple.touristd', 'args':['firstOSLogin', '-date', '2018-1-1'], } ]
	for url in text:
		if url != '':
			url = re.sub(r'.*<string>([^<]*).*', r'\\1', url)
			defaults_command.append( { 'type':'defaults', 'domain':'com.apple.touristd', 'args':['seed-'+url, '-date', '2018-1-1'], 'user':True, } )
	my_os = get_short_os_version()
	prefs['Tourist.User.disable']['versions'] = { my_os:'all' }
	prefs['Tourist.User.disable']['all'] = defaults_command

##########################################################################################

mak_commands['ard_user'] = {
	'help':'ard_userHelp',
	'main':'ard_user',
}

def ard_userHelp(name):
	return '''Usage: %s <options> ard_user [-c] <username[,username..]> [setting[ setting..]]

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
		%s ard_user admin
		%s ard_user -r                           # Removes all access
		%s ard_user -r admin,james               # Removes all access except users listed
		%s ard_user -r admin -ChangeSettings

''' % (name,name,name,name,name)

def ard_user(args):
	kickstart = '/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart';
	clear = False
	try:
		(optargs, args) = getopt.getopt(args, 'r')
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	for opt, arg in optargs:
		if opt == '-r':
			clear = True
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
		if verbose:
			print 'Removing all previous ARD priveledges from all users'
		ard_users = sh( 'dscl . list /Users naprivs | awk \\'{print \$1}\\'' )
		ard_users = ard_users.split("\\n")
		for user in ard_users:
			if user != None and user != '':
				sh( 'dscl . delete /Users/' + user + ' naprivs' )
	sh( kickstart + ' -configure -allowAccessFor -specifiedUsers' )
	if len(args) > 0:
		sh( kickstart + ' -configure -access -on -privs ' + ' '.join(privs) + ' -users ' + args[0] )
		sh( kickstart + ' -activate -restart -agent' )

##########################################################################################

mak_commands['hack_jamf_hooks'] = {
	'help':'hack_jamf_hooksHelp',
	'main':'hack_jamf_hooks',
}

def hack_jamf_hooksHelp(name):
	return '''Usage: %s <options> hack_jamf_hooks [value]

	Changes loginhook.sh checkJSSConnection from 0 to either 6 (default) or what you specify.
	This waits for a network connection before any jamf login policies will run.

	By default the startup script will check 12 times, and logout checks 1 time.

''' % (name)

def hack_jamf_hooks(args):
	value = '6'
	if len(args) == 1:
		try:
			value = str(int(args[0]))
		except getopt.GetoptError, e:
			usage( 'I don\\'t understand ' + args[0], 'hack_jamf_hooks' )
	elif len(args) > 1:
		usage( 'I only understand one value.', 'hack_jamf_hooks' )
	sh( 'sed -i .orig "s/checkJSSConnection -retry [0-9]* ;/checkJSSConnection -retry '+value+' ;/g" /Library/Application\\ Support/JAMF/ManagementFrameworkScripts/loginhook.sh' )

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

	Array or dictionary items (like program arguments) must be terminated with ";" (don't forget to quote or escape it).

	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html
	https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/plist.5.html
	https://en.wikipedia.org/wiki/Launchd

	Examples:
		%s launchdaemon example.plist echo hi \\; StartCalendarInterval Hour 4 Minute 0 Weekday 0 \\;
		%s launchdaemon example.plist echo hi \\; StandardOutPath /var/log/complete_enrollment.log StandardErrorPath /var/log/complete_enrollment.err.log RunAtLoad 1
		%s launchdaemon example.plist echo hi \\; WatchPaths /Library/Admin/launchdwatch \\;

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
				usage( 'KeepAlive Dictionary is not done.', 'launchdaemon' )
		else:
			usage( 'Unknown key: '+key1, 'launchdaemon' )
	if bucket != None and len(bucket) > 0:
		usage( 'Terminate multi-item values with ";" (don\\'t forget to escape it).', 'launchdaemon' )
	return hash

def launchdaemon(args):
	import plistlib
	if len(args) <= 3:
		usage( 'You must have a path, program arguments, and a trigger condition', 'launchdaemon' )
	path = args[0]
	label = re.sub(r'.*\\/([^\\/])\\.plist\$', r'\\1', path)
	if label == '':
		usage('Could not build a label from the path, did the path end with ".plist"?', 'launchdaemon')
	if debug or verbose:
		print( 'Label: '+label )
	flag = True
	program_args = []
	ii = 1
	while flag:
		if ii >= len(args):
			usage( 'You must terminate ProgramArguments items with ";" (don\\'t forget to escape it).', 'launchdaemon' )
		if args[ii] != ';':
			if args[ii][-1] == ';':
				args[ii] = args[ii][:-1]
				flag = False
			program_args.append( args[ii] )
			ii += 1
		else:
			flag = False
	args = args[ii+1:]
	if debug or verbose:
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
	return sh( '/usr/sbin/networksetup ' + ' '.join(args) )

##########################################################################################

mak_commands['set_volume'] = {
	'help':'set_volumeHelp',
	'main':'set_volume',
}

def set_volumeHelp(name):
	return '''Usage: %s <options> set_volume <Volume> [<Output Volume>] [<Input Volume>]

	Sets the speaker and microphone levels.

	<Volume> values are 0-7
	<Output Volume> values are 0-100
	<Input Volume> values are 0-100
	Use "-" to skip

	Examples:
		%s set_volume 0         # Muted
		%s set_volume 3.5 - 0   # Half, skip, microphone muted
		%s set_volume - 0 100   # skip, speaker muted, microphone max

''' % (name,name,name,name)

def is_text_number_between(text, min, max):
	try:
		val = float(text)
	except:
		return False
	return val >= min and val <= max

def set_volume(args):
	if len(args) <= 0:
		usage( 'Specify a value', 'set_volume' )
	for ii, bla in enumerate([['',7], ['output volume ',100], ['input volume ',100]]):
		if len(args) > ii and args[ii] != '-':
			if is_text_number_between(args[ii], 0, bla[1]):
				sh( "osascript -e 'set volume "+bla[0]+args[ii]+"'" )
			else:
				usage( args[ii]+' is not between 0 and '+str(bla[1]), 'set_volume' )

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
	if len(args) != 2:
		usage( 'Missing arguments', 'shell_paths' )
	search = args[0]
	path = '/private/etc/paths.d/' + args[1]
	if debug or verbose:
		print 'Saving "' + search + '" to ' + path
	file = open(path, 'w')
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
	very much).  systemsetup modifies time, sleep, sharing, and startup disks

	Examples:
		%s systemsetup -settimezone America/Denver
		%s systemsetup -setusingnetworktime on
		%s systemsetup -setnetworktimeserver time.apple.com

''' % (name,name,name,name)

def systemsetup(args):
	return sh( '/usr/sbin/systemsetup ' + ' '.join(args) )

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def sh(cmd):
	if type(cmd) is list:
		print "Script error: use sh2 to pass args as a list"
		sys.exit(1)
	if debug or verbose:
		print( cmd )
		result = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE).communicate()[0]
		if result != '':
			print( result )
		return result
	else:
		return Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE).communicate()[0]

def sh2(cmd):
	if debug or verbose:
		if type(cmd) is list:
			print( ' '.join(cmd) )
		else:
			print( cmd )
		result = Popen(cmd).communicate()[0]
		if result != '':
			print( result )
		return result
	else:
		return Popen(cmd).communicate()[0]

def get_os_version():
	return sh('sw_vers -productVersion').rstrip('\\n')

def get_short_os_version():
	return re.sub(r'(\\d+\\.\\d+).*', r'\\1', get_os_version())

def usage(e=None,help_command=None):
	if e:
		print e
		print ''
	name = os.path.basename(sys.argv[0])
	text = ''
	if help_command == None or help_command == 'help' or help_command == 'all':
		text += '''Mac Army Knife.  Tool for system administrators to quickly and easily hack a Mac.
                                                    ,^.
                            /\\\\                     /   \\\\
                ,^.        / /                    /    /
                \\\\  \\\\      / /                    /    /
                 \\\\\\\\ \\\\    / /                    /  ///
                  \\\\\\\\ \\\\  / /                    /  ///
                   \\\\  \\\\/_/____________________/    /
                    `/                         \\\\  /_____________
         __________/|  o    Mac Army Knife   o  |'              \\\\
        |____________\\\\_________________________/_________________\\\\

I'm combining all of my Mac customization scripts into this script.  All of this info is
on the web scattered all over and a lot of this is just shortcuts to built-in commands.
Why?  I'm tired of looking it up on the web and making scripts or profiles or whatever.  I
just wanted a one stop shop as easy "System Preferences" but from the command line.

https://github.com/magnusviri/mak.py

Usage: %s [-dv] [-o <os_ver>] command options

	-d            Debug (verbose + some things aren't executed)
	-o <os_ver>   When running this script on a computer with an OS different than the
	              target volume, specify the target volume OS here
	-v            Verbose
	--version     Print version and exit

Commands
''' % (name)
		mak_commands_with_help = mak_commands.keys()
		mak_commands_with_help.append('help')
		for mak_command in sorted( mak_commands_with_help ):
			text += "\\t" + mak_command + "\\n"
		text += '''
For help
	%s help <command name>
	%s help all  # will display help for all commands
''' % (name,name)
	if help_command == 'all':
		text += "\\n------------------------------------------------------------------------------------------\\n"
		for mak_command, command_data in sorted( mak_commands.iteritems() ):
			if 'help' in mak_commands[mak_command]:
				text += "\\n"+globals()[mak_commands[mak_command]['help']](name)
				text += "------------------------------------------------------------------------------------------\\n"
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
		(optargs, args) = getopt.getopt(sys.argv[argv_start:], 'do:v', ['version'])
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	global debug, verbose
	for opt, arg in optargs:
		if opt == '-d':
			debug = True
		elif opt == '-o':
			target_os = arg
		elif opt == '-v':
			verbose = True
		elif opt == '--version':
			print version
			sys.exit(0)
	if len(args) <= 0:
		usage()
	command = args[0]
	if command == 'help':
		if len(args) > 1:
			usage('', args[1])
		else:
			usage()
	else:
		if command in mak_commands and 'main' in mak_commands[command]:
			main_name = mak_commands[command]['main']
			if main_name in globals():
				globals()[main_name](args[1:])
			else:
				print 'Script error: there is no function named "' + main_name + '"'
				sys.exit(1)
		else:
			usage('Unknown command: '+command)

if __name__ == '__main__':
	main()
EOF
}

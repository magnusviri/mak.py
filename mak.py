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
from shutil import copyfile
jamf = False
debug = False
verbose = False
quiet = False
mak_commands = {}

version = '1.1.7'

##########################################################################################

mak_commands['pref'] = {
    'help':'prefHelp',
    'main':'pref',
}

os_age = [ '11.0', '10.15', '10.14', '10.13', '10.12', '10.11', '10.10', '10.9', '10.8', '10.7', '10.6', '10.5', '10.4', '10.3', '10.2', '10.1', '10.0', '0' ]

pref_delim = '='

def prefHelp(name):
    text = '''Usage: %s pref [-dh|--help] [-o os] [-p path] [-u username] Preference.Name[%sOption]

    -o <os>         Disregard the booted OS and use the specified OS instead (e.g. 10.x)

    The following options specify which file to modify when the default is in the user
    level domain ("*.User.*")

    -p <path>       Path to the preferences directory (used for user and computer prefs)
    -P <path>       Complete path to the plist file (all script path logic is skipped)
    -R              Use root: "/private/var/root/Library/Preferences/" (username is
                    "root", unless a -u comes after the -T)
    -T              Use template: "/System/Library/User Template/English.lproj" (username
                    is "root", unless a -u comes after the -T)
    -u <username>   For user defaults, use this username

    Supported settings:
''' % (name, pref_delim)
    for pref, pref_data in sorted( pref_list.iteritems() ):
        if 'help' in pref_data:
            text += "\t\t" + pref_data['help'] + "\n"
            if 'unit_tests' in pref_data:
                for unit_test in pref_data['unit_tests']:
                    if unit_test != '':
                        text += "\t\t\tExample: mak.py pref " + unit_test + "\n"

    text += '''
    Examples:
        %s pref SoftwareUpdate.Computer.AutoUpdate%sfalse
        %s pref -o 10.12 -p /Users/admin Clock.User.ShowSeconds
        %s pref -P /Users/admin/Library/Preferences/com.apple.menuextra.clock.plist Clock.User.ShowSeconds
        %s pref -u admin Clock.User.ShowSeconds
        %s pref -T Clock.User.ShowSeconds

''' % (name,pref_delim,name,name,name,name)
    return( text )

pref_list = {
    ##########
    # Global #
    ##########
    'Global.User.FullKeyboardAccess':{
        'help':'Global.User.FullKeyboardAccess - (10.14)',
        'help':'Global.User.FullKeyboardAccess'+pref_delim+'<int> - changing this pref requires a logout/login ; 1 arg: 0 = Text boxes and lists only, 2 = All controls; user domain (10.14)',
        'unit_tests':['Global.User.FullKeyboardAccess'+pref_delim+'2',],
        '10.14':[
            { 'type':'defaults', 'domain':'.GlobalPreferences', 'args':['AppleKeyboardUIMode', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Global.User.FullKeyboardAccess':{
        'help':'Global.User.FullKeyboardAccess - (10.14)',
        'help':'Global.User.FullKeyboardAccess'+pref_delim+'<int> - changing this pref requires a logout/login ; 1 arg: 0 = Text boxes and lists only, 2 = All controls; user domain (10.14)',
        'unit_tests':['Global.User.FullKeyboardAccess'+pref_delim+'2',],
        '10.14':[
            { 'type':'defaults', 'domain':'.GlobalPreferences', 'args':['AppleKeyboardUIMode', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },

#     <key>KeyRepeat</key>
#     <integer>2</integer>
# 120, 90, 60, 30, 15, 12, 6, 2 fastest
#
#     <key>InitialKeyRepeat</key>
#     <integer>120</integer>
# off 300000, slowest 120, 94, 68, 35, 25, 15 fastest
#
# NSAutomaticCapitalizationEnabled
# NSAutomaticDashSubstitutionEnabled
# NSAutomaticPeriodSubstitutionEnabled
# NSAutomaticQuoteSubstitutionEnabled
# NSAutomaticSpellingCorrectionEnabled
# NSAutomaticTextCompletionEnabled true
#
#     <key>NSPreferredWebServices</key>
#     <dict>
#         <key>NSWebServicesProviderWebSearch</key>
#         <dict>
#             <key>NSDefaultDisplayName</key>
#             <string>DuckDuckGo</string>
#             <key>NSProviderIdentifier</key>
#             <string>com.duckduckgo</string>
#         </dict>
#     </dict>
#
#     <key>NSUserDictionaryReplacementItems</key>
#     <array>
#         <dict>
#             <key>on</key>
#             <integer>1</integer>
#             <key>replace</key>
#             <string>omw</string>
#             <key>with</key>
#             <string>On my way!</string>
#         </dict>
#     </array>



    ########################
    # Apple Remote Desktop #
    ########################
    'ARD.Computer.Text1':{
        'help':'ARD.Computer.Text1 - (11)',
        'unit_tests':['ARD.Computer.Text1=Text1',],
        '11.0':[
            { 'type':'defaults', 'domain':'com.apple.RemoteDesktop', 'args':['Text1', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'ARD.Computer.Text2':{
        'help':'ARD.Computer.Text2 - (10.9)',
        'unit_tests':['ARD.Computer.Text2'+pref_delim+'Text2',],
        '10.9':[
            { 'type':'defaults', 'domain':'com.apple.RemoteDesktop', 'args':['Text2', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'ARD.Computer.Text3':{
        'help':'ARD.Computer.Text3 - (10.9)',
        'unit_tests':['ARD.Computer.Text3'+pref_delim+'Text3',],
        '10.9':[
            { 'type':'defaults', 'domain':'com.apple.RemoteDesktop', 'args':['Text3', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'ARD.Computer.Text4':{
        'help':'ARD.Computer.Text4 - (10.9)',
        'unit_tests':['ARD.Computer.Text4'+pref_delim+'Text4',],
        '10.9':[
            { 'type':'defaults', 'domain':'com.apple.RemoteDesktop', 'args':['Text4', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    #########
    # Clock #
    #########
    'Clock.User.ShowSeconds':{
        'help':'Clock.User.ShowSeconds - user domain (10.14)',
        'unit_tests':['Clock.User.ShowSeconds',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.menuextra.clock', 'args':['DateFormat', '-string', '\'EEE hh:mm:ss a\''], },
        ],
    },
    #################
    # CrashReporter #
    #################
    'CrashReporter.User.Use_Notification_Center':{
        'help':'CrashReporter.User.Use_Notification_Center=<1|0> - ; 1 arg; user domain (10.11)',
        'unit_tests':['CrashReporter.User.Use_Notification_Center'+pref_delim+'1',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.CrashReporter', 'args':['UseUNC', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ########
    # Dock #
    ########
    'Dock.User.launchanim':{
        'help':'Dock.User.launchanim'+pref_delim+'<true|false> - ; 1 arg; user domain (10.11)',
        'unit_tests':['Dock.User.launchanim'+pref_delim+'false',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Dock', 'args':['launchanim', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Dock.User.expose-animation-duration':{
        'help':'Dock.User.expose-animation-duration'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
        'unit_tests':['Dock.User.expose-animation-duration'+pref_delim+'2.0',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Dock', 'args':['expose-animation-duration', '-float', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Dock.User.autohide-delay':{
        'help':'Dock.User.autohide-delay'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
        'unit_tests':['Dock.User.autohide-delay'+pref_delim+'5.0',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Dock', 'args':['autohide-delay', '-float', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Dock.User.DisableAllAnimations':{
        'help':'Dock.User.DisableAllAnimations'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
        'unit_tests':['Dock.User.DisableAllAnimations'+pref_delim+'1.0',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Dock', 'args':['DisableAllAnimations', '-float', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ##########
    # Finder #
    ##########
    'Finder.User.ShowTabView':{
        'help':'Finder.User.ShowTabView'+pref_delim+'<true|false> - View menu: Show Tab View; 1 arg; user domain (10.12)',
        'unit_tests':['Finder.User.ShowTabView',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowTabView', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.ShowPathbar':{
        'help':'Finder.User.ShowPathbar'+pref_delim+'<true|false> - View menu: Show Pathbar; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowPathbar', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.ShowStatusBar':{
        'help':'Finder.User.ShowStatusBar'+pref_delim+'<true|false> - View menu: Show Status Bar; 1 arg; user domain (10.14)',
        'unit_tests':['Finder.User.ShowStatusBar=true',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowStatusBar', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.ShowHardDrivesOnDesktop':{
        'help':'Finder.User.ShowHardDrivesOnDesktop'+pref_delim+'<true|false> - General tab: Show Hard Drives On Desktop; 1 arg; user domain (10.14)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowHardDrivesOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.ShowExternalHardDrivesOnDesktop':{
        'help':'Finder.User.ShowExternalHardDrivesOnDesktop'+pref_delim+'<true|false> - General tab: Show External Hard Drives On Desktop; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowExternalHardDrivesOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.ShowRemovableMediaOnDesktop':{
        'help':'Finder.User.ShowRemovableMediaOnDesktop'+pref_delim+'<true|false> - General tab: Show Removable Media On Desktop; 1 arg; user domain (10.14)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowRemovableMediaOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.ShowMountedServersOnDesktop':{
        'help':'Finder.User.ShowMountedServersOnDesktop'+pref_delim+'<true|false> - General tab: Show Mounted Servers On Desktop; 1 arg; user domain (10.14)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['ShowMountedServersOnDesktop', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.NewWindowTarget':{
        'help':'Finder.User.NewWindowTarget'+pref_delim+'<PfCm|PfVo|PfHm|PfDe|PfDo|PfID|PfAF|PfLo> - General tab: New Finder windows shows: PfCm - computer, PfVo - volume, PfHm - Home, PfDe - Desktop, PfDo - Documents, PfID - iCloud, PfAF - All Files, PfLo - Other; 1 arg; user domain (10.12)',
        'unit_tests':['Finder.User.NewWindowTarget=PfHm',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['NewWindowTarget', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.NewWindowTargetPath':{
        'help':'Finder.User.NewWindowTargetPath'+pref_delim+'<file:///...> - General tab: New Finder windows shows: PfCm - empty string, PfVo - /, PfHm - /Users/name/, PfDe - /Users/name/Desktop/, PfDo - /Users/name/Documents/, PfID - /Users/name/Library/Mobile%20Documents/com~apple~CloudDocs/, PfAF - /System/Library/CoreServices/Finder.app/Contents/Resources/MyLibraries/myDocuments.cannedSearch, Other - Anything; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['NewWindowTargetPath', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.FinderSpawnTab':{
        'help':'Finder.User.FinderSpawnTab'+pref_delim+'<true|false> - General tab: Open folders in tabs intead of new windows; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['FinderSpawnTab', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.AppleShowAllExtensions':{
        'help':'Finder.User.AppleShowAllExtensions'+pref_delim+'<true|false> - Advanced tab: Show all filename extensions; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['AppleShowAllExtensions', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.FXEnableExtensionChangeWarning':{
        'help':'Finder.User.FXEnableExtensionChangeWarning'+pref_delim+'<true|false> - Advanced tab: Show warning before changing an extension; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXEnableExtensionChangeWarning', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.FXEnableRemoveFromICloudDriveWarning':{
        'help':'Finder.User.FXEnableRemoveFromICloudDriveWarning'+pref_delim+'<true|false> - Advanced tab: Show warning before removing from iCloud Drive; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXEnableRemoveFromICloudDriveWarning', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.WarnOnEmptyTrash':{
        'help':'Finder.User.WarnOnEmptyTrash'+pref_delim+'<true|false> - Advanced tab: Show warning before emptying the Trash; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['WarnOnEmptyTrash', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.FXRemoveOldTrashItems':{
        'help':'Finder.User.FXRemoveOldTrashItems'+pref_delim+'<true|false> - Advanced tab: Remove items from the Trash after 30 days; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXRemoveOldTrashItems', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User._FXSortFoldersFirst':{
        'help':'Finder.User._FXSortFoldersFirst'+pref_delim+'<true|false> - Advanced tab: Keep Folders on top when sorting by name; 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['_FXSortFoldersFirst', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.FXDefaultSearchScope':{
        'help':'Finder.User.FXDefaultSearchScope'+pref_delim+'<SCev|SCcf|SCsp> - Where to search, computer (SCev), current folder (SCcf), or previous scope (SCsp); 1 arg; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['FXDefaultSearchScope', '%ARG0%'], 'arg_count':1, },
        ],
    },
    # Other
#     <key>NSNavLastCurrentDirectory</key>
#     <string>/Applications</string>
#     <key>NSNavLastRootDirectory</key>
#     <string>/Applications</string>
    'Finder.User._FXShowPosixPathInTitle':{
        'help':'Finder.User._FXShowPosixPathInTitle'+pref_delim+'<true|false> - Shows full path in title; 1 arg; user domain (10.14)',
        'unit_tests':['Finder.User._FXShowPosixPathInTitle=true',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['_FXShowPosixPathInTitle', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Finder.User.DisableAllAnimations':{
        'help':'Finder.User.DisableAllAnimations'+pref_delim+'<true|false> - Disable animation when opening the Info window in Finder; 1 arg; user domain (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.finder', 'args':['DisableAllAnimations', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ##############
    # Gatekeeper #
    ##############
    'Gateway.Computer.GKAutoRearm':{ # https://www.cnet.com/how-to/how-to-disable-gatekeeper-permanently-on-os-x/
        'help':'Gateway.Computer.GKAutoRearm'+pref_delim+'<true|false> - Turn off 30 day rearm ; 1 arg; (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.security', 'args':['GKAutoRearm', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    #################
    # Generic Prefs #
    #################
    'Generic.Computer':{
        'help':'Generic.Computer'+pref_delim+'<domain>'+pref_delim+'<key>'+pref_delim+'<format>'+pref_delim+'<value> - Generic computer preference; 4 args;',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'arg_count':4, }, # ARG0 is the domain
        ],
    },
    'Generic.User':{
        'help':'Generic.User'+pref_delim+'<domain>'+pref_delim+'<key>'+pref_delim+'<format>'+pref_delim+'<value> - Generic user preference; 4 args; user domain',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'args':['%ARG1%', '%ARG2%', '%ARG3%'], 'arg_count':4, }, # ARG0 is the domain
        ],
    },
    'Generic.User.ByHost':{
        'help':'Generic.User.ByHost'+pref_delim+'<domain>'+pref_delim+'<key>'+pref_delim+'<format>'+pref_delim+'<value> - Generic user byhost preference; 4 args; user/byhost domain',
        'unit_tests':['',],
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
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.sassafras.KeyAccess', 'args':['host', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ###############
    # Loginwindow #
    ###############
    'Loginwindow.Computer.autoLoginUserScreenLocked':{
        'help':'Loginwindow.Computer.autoLoginUserScreenLocked'+pref_delim+'<true|false> - autoLoginUserScreenLocked. (10.14)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.loginwindow', 'args':['autoLoginUserScreenLocked', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Loginwindow.Computer.DisableScreenLockImmediate':{
        'help':'Loginwindow.Computer.DisableScreenLockImmediate'+pref_delim+'<true|false> - Gets rid of the Lock Screen option in the Apple Menu. (10.13-10.15)',
        'unit_tests':['Loginwindow.Computer.DisableScreenLockImmediate=true',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.loginwindow', 'args':['DisableScreenLockImmediate', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Loginwindow.Computer.GuestEnabled':{
        'help':'Loginwindow.Computer.GuestEnabled'+pref_delim+'<true|false> - Enable/disable Guest user. (10.14)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.loginwindow', 'args':['GuestEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Loginwindow.Computer.Hide500Users':{
        'help':'Loginwindow.Computer.Hide500Users'+pref_delim+'<true|false> - Hide uid 500 users. (10.14)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.loginwindow', 'args':['Hide500Users', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Loginwindow.User.DeleteRelaunchAtLogin':{
        'help':'Loginwindow.User.DeleteRelaunchAtLogin - Removes the TALAppsToRelaunchAtLogin so that nothing relaunches at the next login; user domain (10.12)',
        'unit_tests':['',],
        'byhost':True,
        '10.12':[
            { 'type':'PlistBuddy', 'domain':'com.apple.loginwindow', 'command':'Delete', 'args':['TALAppsToRelaunchAtLogin'], },
        ],
    },
    #############
    # Microsoft #
    #############
    # https://docs.microsoft.com/en-us/office365/enterprise/network-requests-in-office-2016-for-mac
    'Microsoft.Computer.AcknowledgeDataCollectionPolicy':{
        'help':'Microsoft.Computer.AcknowledgeDataCollectionPolicy - Sets AcknowledgedDataCollectionPolicy so that it doesn\'t show the annoying dialog (10.14)',
        'unit_tests':['Microsoft.Computer.AcknowledgeDataCollectionPolicy',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.microsoft.autoupdate2', 'args':['AcknowledgedDataCollectionPolicy', 'RequiredDataOnly'], },
        ],
    },
    'Microsoft.User.AutoUpdateHowToCheck':{
        'help':'Microsoft.User.AutoUpdateHowToCheck'+pref_delim+'Value - Sets AutoUpdate check method; Values are Manual, AutomaticCheck, and AutomaticDownload (10.14)',
        'unit_tests':['Microsoft.User.AutoUpdateHowToCheck=Manual',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.microsoft.autoupdate2', 'args':['HowToCheck', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Microsoft.User.SendAllTelemetryEnabled':{
        'help':'Microsoft.User.SendAllTelemetryEnabled'+pref_delim+'<true|false> - Sets SendAllTelemetryEnabled (10.14)',
        'unit_tests':['Microsoft.User.SendAllTelemetryEnabled=false',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.microsoft.Word', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.Excel', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.Powerpoint', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.Outlook', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.onenote.mac', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.autoupdate2', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.autoupdate2.fba', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.microsoft.Office365ServiceV2', 'args':['SendAllTelemetryEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    #########
    # Mouse #
    #########
    'Mouse.User.Click.Double':{
        'help':'Mouse.User.Click.Double - Configures mouse double click; user domain (10.11)',
        'unit_tests':['Mouse.User.Click.Double',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.driver.AppleHIDMouse', 'args':['Button2', '-int', '2'], },
            { 'type':'defaults', 'domain':'com.apple.driver.AppleBluetoothMultitouch.mouse', 'args':['MouseButtonMode', '-string', 'TwoButton'], },
        ],
    },
    'Mouse.User.Click.Single':{
        'help':'Mouse.User.Click.Single - Configures mouse single click; user domain (10.11)',
        'unit_tests':['Mouse.User.Click.Single',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.driver.AppleHIDMouse', 'args':['Button2', '-int', '1'], },
            { 'type':'defaults', 'domain':'com.apple.driver.AppleBluetoothMultitouch.mouse', 'args':['MouseButtonMode', '-string', 'OneButton'], },
        ],
    },
    'Mouse.User.ScrollDirection':{
        'help':'Mouse.User.ScrollDirection'+pref_delim+'<true|false> - true = "natrual"; 1 arg; user domain (10.14)',
        'unit_tests':['Mouse.User.ScrollDirection'+pref_delim+'false',],
        '10.14':[
            { 'type':'defaults', 'domain':'.GlobalPreferences', 'args':['com.apple.swipescrolldirection', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Mouse.User.SecondaryClick':{
        'help':'Mouse.User.SecondaryClick'+pref_delim+'<string> - SecondaryClick ; 1 arg: OneButton|TwoButton|TwoButtonSwapped; user domain (10.14)',
        'unit_tests':['Mouse.User.SecondaryClick'+pref_delim+'TwoButton',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.AppleMultitouchMouse', 'args':['MouseButtonMode', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Mouse.User.SmartZoom':{
        'help':'Mouse.User.SmartZoom'+pref_delim+'<int> - SmartZoom ; 1 arg: <int>; user domain (10.14)',
        'unit_tests':['Mouse.User.SmartZoom'+pref_delim+'0',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.AppleMultitouchMouse', 'args':['MouseOneFingerDoubleTapGesture', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Mouse.User.MouseSpeed':{
        'help':'Mouse.User.MouseSpeed'+pref_delim+'<real> - slow 0.0, 0.125, .5, .6875, .875, 1, 1.5, 2, 2.5, 3 fast ; 1 arg: 0 = Text boxes and lists only, 2 = All controls; user domain (10.14)',
        'unit_tests':['Mouse.User.MouseSpeed'+pref_delim+'0.875',],
        '10.14':[
            { 'type':'defaults', 'domain':'.GlobalPreferences', 'args':['com.apple.mouse.scaling', '-real', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Mouse.User.SwipeBetweenPages':{
        'help':'Mouse.User.SwipeBetweenPages'+pref_delim+'<true|false> - ; 1 arg; user domain (10.14)',
        'unit_tests':['Mouse.User.SwipeBetweenPages'+pref_delim+'false',],
        '10.14':[
            { 'type':'defaults', 'domain':'.GlobalPreferences', 'args':['AppleEnableMouseSwipeNavigateWithScrolls', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Mouse.User.SwipeBetweenApps':{
        'help':'Mouse.User.SwipeBetweenApps'+pref_delim+'<true|false> ; 1 arg; user domain (10.14)',
        'unit_tests':['Mouse.User.SwipeBetweenApps'+pref_delim+'0',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.AppleMultitouchMouse', 'args':['MouseTwoFingerHorizSwipeGesture', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Mouse.User.MissionControl':{
        'help':'Mouse.User.MissionControl'+pref_delim+'<int> ; 1 arg: 0 = off, 3 = enabled; user domain (10.14)',
        'unit_tests':['Mouse.User.MissionControl'+pref_delim+'0',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.AppleMultitouchMouse', 'args':['MouseTwoFingerDoubleTapGesture', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },


    ##############
    # QuickTime7 #
    ##############
    'QuickTime7.User.ProName':{
        'help':'Quicktime7.User.ProName'+pref_delim+'Johnny Appleseed - Set QuickTime 7 Pro Name; 1 arg; user/byhost domain (10.14)',
        'unit_tests':['QuickTime7.User.ProName="University of Utah"',],
        'byhost':True,
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Name', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'QuickTime7.User.ProOrg':{
        'help':'Quicktime7.User.ProOrg'+pref_delim+'Organization - Set QuickTime 7 Pro Organization; 1 arg; user/byhost domain (10.14)',
        'unit_tests':['',],
        'byhost':True,
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Organization', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'QuickTime7.User.ProKey':{
        'help':'Quicktime7.User.ProKey'+pref_delim+'1234-ABCD-1234-ABCD-1234 - Set QuickTime 7 Pro Registration Key; 1 arg; user/byhost domain (10.14)',
        'unit_tests':['QuickTime7.User.ProKey=38D3-F2CM-4MXT-QZBB-7CJT',],
        'byhost':True,
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.QuickTime', 'args':['Pro Key', '-dict-add', 'Registration Key', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ##########
    # Safari #
    ##########
    'Safari.User.HomePage':{
        'help':'Safari.User.HomePage'+pref_delim+'http://example.com - Set Safari\'s homepage; 1 arg; user domain (10.11)',
        'unit_tests':['Safari.User.HomePage=http://www.biology.utah.edu/centers/computing/student.php',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['HomePage', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Safari.User.NewTabBehavior':{
        'help':'Safari.User.NewTabBehavior'+pref_delim+'<int> - Sets what Safari shows in new tabs; 1 arg; user domain (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewTabBehavior', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Safari.User.NewWindowBehavior':{
        'help':'Safari.User.NewWindowBehavior'+pref_delim+'<int> - Sets what Safari shows in new windows; 1 arg; user domain (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewWindowBehavior', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Safari.User.NewTabAndWindowBehavior':{
        'help':'Safari.User.NewAndTabWindowBehavior'+pref_delim+'<int> - Sets what Safari shows in new tabs and windows; 1 arg; user domain (10.11)',
        'unit_tests':['Safari.User.NewTabAndWindowBehavior=0',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewWindowBehavior', '-int', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['NewTabBehavior', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Safari.User.Show_Tabs_Status_Favorites':{
        'help':'Safari.User.Show_Tabs_Status_Favorites'+pref_delim+'<true|false> - Turns on or off Tab, Status, and Favorites bar; 1 arg; user domain (10.11)',
        'unit_tests':['Safari.User.Show_Tabs_Status_Favorites=true',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['AlwaysShowTabBar', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['ShowOverlayStatusBar', '-bool', '%ARG0%'], 'arg_count':1, },
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['ShowFavoritesBar-v2', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Safari.User.LastSafariVersionWithWelcomePage':{
        'help':'Safari.User.LastSafariVersionWithWelcomePage'+pref_delim+'<string> - Gets rid of the Welcome to Safari message; 1 arg; user domain (10.11)',
        'unit_tests':['Safari.User.LastSafariVersionWithWelcomePage=9.0',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['LastSafariVersionWithWelcomePage-v2', '-string', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Safari.User.WebKitInitialTimedLayoutDelay':{
        'help':'Safari.User.WebKitInitialTimedLayoutDelay'+pref_delim+'<float> - ; 1 arg; user domain (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.Safari', 'args':['WebKitInitialTimedLayoutDelay', '-float', '%ARG0%'], 'arg_count':1, },
        ],
    },
    #################
    # Screencapture #
    #################
    'Screencapture.User.disable-shadow':{
        'help':'Screencapture.User.disable-shadow'+pref_delim+'<true|false> - ; 1 arg; user domain (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.screencapture', 'args':['disable-shadow', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ###############
    # ScreenSaver #
    ###############
    'ScreenSaver.Computer.Basic.Message':{
        'help':'ScreenSaver.Computer.Basic.Message'+pref_delim+'<Message> - Set the basic screensaver password; 1 arg; computer domain (10.11)',
        'unit_tests':['ScreenSaver.Computer.Basic.Message=Computer Message=',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.ScreenSaver.Basic', 'args':['MESSAGE', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'ScreenSaver.Computer.Computer_Name_Clock':{
        'help':'ScreenSaver.Computer.Computer_Name_Clock - Turns on Clock for Computer Name Module; computer domain (10.11)',
        'unit_tests':['ScreenSaver.User.Computer_Name_Clock',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['showClock', '-bool', 'true'], },
        ],
    },
    'ScreenSaver.User.Basic.Message':{
        'help':'ScreenSaver.User.Basic.Message'+pref_delim+'<Message> - Set the basic screensaver password; 1 arg; user/byhost domain (10.11)',
        'unit_tests':['ScreenSaver.User.Basic.Message=User Message',],
        'byhost':True,
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.ScreenSaver.Basic', 'args':['MESSAGE', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'ScreenSaver.User.Computer_Name':{
        'help':'ScreenSaver.User.Computer_Name - Sets screensaver to Computer Name; user/byhost domain (10.11)',
        'unit_tests':['ScreenSaver.User.Computer_Name',],
        'byhost':True,
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['moduleDict', '-dict', 'path', '/System/Library/Frameworks/ScreenSaver.framework/Resources/Computer Name.saver'], },
        ],
    },
    'ScreenSaver.User.Computer_Name_Clock':{
        'help':'ScreenSaver.User.Computer_Name_Clock - Turns on Clock for Computer Name Module; user/byhost domain (10.11)',
        'unit_tests':['',],
        'byhost':True,
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['showClock', '-bool', 'true'], },
        ],
    },
    'ScreenSaver.User.askForPassword':{
        'help':'ScreenSaver.User.askForPassword'+pref_delim+'<1|0> - Set screensaver password; 1 arg: 0 off, 1 on; user domain (10.11)',
        'unit_tests':['ScreenSaver.User.askForPassword=0',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.screensaver', 'args':['askForPassword', '-int', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ##################
    # SetupAssistant #
    ##################
    'SetupAssistant.User.DidSeeAppearanceSetup':{
        'help':'SetupAssistant.User.DidSeeAppearanceSetup'+pref_delim+'<true|false> - Hides login setup assistant; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['SetupAssistant.User.DidSeeAppearanceSetup=true',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeAppearanceSetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeePrivacy':{
        'help':'SetupAssistant.User.DidSeePrivacy'+pref_delim+'<true|false> - Hides login setup assistant privacy question; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['SetupAssistant.User.DidSeePrivacy=true',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeePrivacy', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeSiriSetup':{
        'help':'SetupAssistant.User.DidSeeSiriSetup'+pref_delim+'<true|false> - Hides login setup assistant Siri question; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['SetupAssistant.User.DidSeeSiriSetup=true',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeSiriSetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeApplePaySetup':{
        'help':'SetupAssistant.User.DidSeeApplePaySetup'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeApplePaySetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeAvatarSetup':{
        'help':'SetupAssistant.User.DidSeeAvatarSetup'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeAvatarSetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeCloudSetup':{
        'help':'SetupAssistant.User.DidSeeCloudSetup'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeCloudSetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeiCloudLoginForStorageServices':{
        'help':'SetupAssistant.User.DidSeeiCloudLoginForStorageServices'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeiCloudLoginForStorageServices', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeSyncSetup':{
        'help':'SetupAssistant.User.DidSeeSyncSetup'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeSyncSetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeSyncSetup2':{
        'help':'SetupAssistant.User.DidSeeSyncSetup2'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeSyncSetup2', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeTouchIDSetup':{
        'help':'SetupAssistant.User.DidSeeTouchIDSetup'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeTouchIDSetup', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SetupAssistant.User.DidSeeTrueTonePrivacy':{
        'help':'SetupAssistant.User.DidSeeTrueTonePrivacy'+pref_delim+'<true|false> - ; 1 arg: true/false; user domain (10.14-10.15)',
        'unit_tests':['',],
        '10.14':[
            { 'type':'defaults', 'domain':'com.apple.SetupAssistant', 'args':['DidSeeTrueTonePrivacy', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ##################
    # SoftwareUpdate #
    ##################
    'SoftwareUpdate.Computer.SetCatalogURL':{
        'help':'SoftwareUpdate.Computer.SetCatalogURL'+pref_delim+'<http://example.com:8088/index.sucatalog> - Sets the SoftwareUpdate CatalogURL, which must be a Mac OS X Server with the Software Update service activated; (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['CatalogURL', '%ARG0%'], 'arg_count':1, },
        ],
    },
    # https://derflounder.wordpress.com/2014/12/29/managing-automatic-app-store-and-os-x-update-installation-on-yosemite/
    'SoftwareUpdate.Computer.AutomaticCheckEnabled':{
        'help':'SoftwareUpdate.Computer.AutomaticCheckEnabled'+pref_delim+'<true|false> - "Automatically check for updates"; 1 arg: true/false; (10.11)',
        'unit_tests':['SoftwareUpdate.Computer.AutomaticCheckEnabled=false',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['AutomaticCheckEnabled', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SoftwareUpdate.Computer.AutomaticDownload':{
        'help':'SoftwareUpdate.Computer.AutomaticDownload'+pref_delim+'<true|false> - "Download newly available updates in the background", requires AutomaticCheckEnabled; 1 arg: true/false; (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.SoftwareUpdate', 'args':['AutomaticDownload', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SoftwareUpdate.Computer.AutoUpdate':{
        'help':'SoftwareUpdate.Computer.AutoUpdate'+pref_delim+'<true|false> - "Install app updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: true/false; (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.commerce', 'args':['AutoUpdate', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SoftwareUpdate.Computer.AutoUpdateRestartRequired':{
        'help':'SoftwareUpdate.Computer.AutoUpdateRestartRequired'+pref_delim+'<true|false> - "Install macOS updates", requires AutomaticCheckEnabled and AutomaticDownload; 1 arg: true/false; (10.11)',
        'unit_tests':['',],
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.commerce', 'args':['AutoUpdateRestartRequired', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SoftwareUpdate.Computer.SystemSecurityUpdates':{
        'help':'SoftwareUpdate.Computer.SystemSecurityUpdates'+pref_delim+'<true|false> - "Install system data files and security updates", requires AutomaticCheckEnabled; 1 arg: true/false; (10.11)',
        'unit_tests':['',],
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
        'unit_tests':['SystemUIServer.User.DontAutoLoadReset',],
        'byhost':True,
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.systemuiserver', 'command':'delete', 'args':['dontAutoLoad'], },
        ],
    },
    'SystemUIServer.User.DontAutoLoad':{
        'help':'SystemUIServer.User.DontAutoLoad'+pref_delim+'<path of menu extra> - ; user/byhost domain (10.11)',
        'unit_tests':['SystemUIServer.User.DontAutoLoad="/System/Library/CoreServices/Menu Extras/AirPort.menu"',],
        'byhost':True,
        '10.11':[
            { 'type':'defaults', 'domain':'com.apple.systemuiserver', 'args':['dontAutoLoad', '-array-add', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'SystemUIServer.User.AirplayVisibility':{
        'help':'SystemUIServer.User.AirplayVisibility'+pref_delim+'<true|false> - ; user domain (10.12)',
        'unit_tests':['',],
        '10.12':[
            { 'type':'defaults', 'domain':'com.apple.systemuiserver', 'args':['NSStatusItem Visibile com.apple.menuextra.airplay', '-bool', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ###################
    # SysbolicHotkeys #
    ###################
    # See below
    #
    ############
    # Time #
    ############
    'Time.Computer.Server':{
        #https://apple.stackexchange.com/questions/117864/how-can-i-tell-if-my-mac-is-keeping-the-clock-updated-properly
        'help':'Time.Computer.Server'+pref_delim+'<url> - "Sets the time server"; 1 arg: url to server; (10.12, 10.14)',
        'unit_tests':['Time.Computer.Server'+pref_delim+'time.apple.com',],
        'versions':{ '10.13':'10.12', }, # I haven't tested this
        '10.12':[
            { 'type':'function', 'function':'systemsetup', 'args':['-setusingnetworktime', 'on'], },
            { 'type':'function', 'function':'systemsetup', 'args':['-setnetworktimeserver', '%ARG0%'], 'arg_count':1, },
            { 'type':'function', 'function':'sh2', 'args':['/usr/sbin/ntpdate', '-u', '%ARG0%'], 'arg_count':1, },
        ],
        '10.14':[
            { 'type':'function', 'function':'systemsetup', 'args':['-setusingnetworktime', 'on'], },
            { 'type':'function', 'function':'systemsetup', 'args':['-setnetworktimeserver', '%ARG0%'], 'arg_count':1, },
            { 'type':'function', 'function':'sh2', 'args':['/usr/bin/sntp', '-sS', '%ARG0%'], 'arg_count':1, },
        ],
    },
    'Time.Computer.Zone':{
        'help':'Time.Computer.Zone - (10.12)',
        'unit_tests':['Time.Computer.Zone'+pref_delim+'America/Denver',],
        '10.12':[
            { 'type':'function', 'function':'systemsetup', 'args':['-settimezone', '%ARG0%'], 'arg_count':1, },
        ],
    },
    ############
    # TouristD #
    ############
    'Tourist.User.disable':{
        'help':'Tourist.User.disable - Disables the blasted tourist thing; user domain (any OS)',
        'unit_tests':['Tourist.User.disable',],
        'pre_run_func':'disable_touristd',
        # This data is populated by disable_touristd, see below.
    },
    #################
    # Function.Test #
    #################
#     'Function.Test':{
#         'help':'Test',
#         '10.12':[
#             { 'type':'function', 'function':'say', 'args':['%ARG1%', 'and', '%ARG0%'], 'arg_count':2, },
#         ],
#     },
}

def buildSysbolicHotkeys(pref_list):
    #Taken from /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/Headers/Events.h
    kc = {
        'A'              : 0,
        'S'              : 1,
        'D'              : 2,
        'F'              : 3,
        'H'              : 4,
        'G'              : 5,
        'Z'              : 6,
        'X'              : 7,
        'C'              : 8,
        'V'              : 9,
        'B'              : 11,
        'Q'              : 12,
        'W'              : 13,
        'E'              : 14,
        'R'              : 15,
        'Y'              : 16,
        'T'              : 17,
        '1'              : 18,
        '2'              : 19,
        '3'              : 20,
        '4'              : 21,
        '6'              : 22,
        '5'              : 23,
        'Equal'          : 24,
        '9'              : 25,
        '7'              : 26,
        'Minus'          : 27,
        '8'              : 28,
        '0'              : 29,
        'RightBracket'   : 30,
        'O'              : 31,
        'U'              : 32,
        'LeftBracket'    : 33,
        'I'              : 34,
        'P'              : 35,
        'L'              : 37,
        'J'              : 38,
        'Quote'          : 39,
        'K'              : 40,
        'Semicolon'      : 41,
        'Backslash'      : 42,
        'Comma'          : 43,
        'Slash'          : 44,
        'N'              : 45,
        'M'              : 46,
        'Period'         : 47,
        'Grave'          : 50,
        'KeypadDecimal'  : 65,
        'KeypadMultiply' : 67,
        'KeypadPlus'     : 69,
        'KeypadClear'    : 71,
        'KeypadDivide'   : 75,
        'KeypadEnter'    : 76,
        'KeypadMinus'    : 78,
        'KeypadEquals'   : 81,
        'Keypad0'        : 82,
        'Keypad1'        : 83,
        'Keypad2'        : 84,
        'Keypad3'        : 85,
        'Keypad4'        : 86,
        'Keypad5'        : 87,
        'Keypad6'        : 88,
        'Keypad7'        : 89,
        'Keypad8'        : 91,
        'Keypad9'        : 92,
        'Return'         : 36,
        'Tab'            : 48,
        'Space'          : 49,
        'Delete'         : 51,
        'Escape'         : 53,
        'Command'        : 55,
        'Shift'          : 56,
        'CapsLock'       : 57,
        'Option'         : 58,
        'Control'        : 59,
        'RightCommand'   : 54,
        'RightShift'     : 60,
        'RightOption'    : 61,
        'RightControl'   : 62,
        'Function'       : 63,
        'F17'            : 64,
        'VolumeUp'       : 72,
        'VolumeDown'     : 73,
        'Mute'           : 74,
        'F18'            : 79,
        'F19'            : 80,
        'F20'            : 90,
        'F5'             : 96,
        'F6'             : 97,
        'F7'             : 98,
        'F3'             : 99,
        'F8'             : 100,
        'F9'             : 101,
        'F11'            : 103,
        'F13'            : 105,
        'F16'            : 106,
        'F14'            : 107,
        'F10'            : 109,
        'F12'            : 111,
        'F15'            : 113,
        'Help'           : 114,
        'Home'           : 115,
        'PageUp'         : 116,
        'ForwardDelete'  : 117,
        'F4'             : 118,
        'End'            : 119,
        'F2'             : 120,
        'PageDown'       : 121,
        'F1'             : 122,
        'LeftArrow'      : 123,
        'RightArrow'     : 124,
        'DownArrow'      : 125,
        'UpArrow'        : 126
    }

    # Modifiers (see "NX_SHIFTMASK" in https://opensource.apple.com/source/IOHIDFamily/IOHIDFamily-1090.220.12/IOHIDSystem/IOKit/hidsystem/IOLLEvent.h.auto.html)
    no_ascii = 65535
    none = 65536 # alphashift (alphashift = caps lock--https://developer.apple.com/documentation/appkit/nsalphashiftkeymask)
    shift = 131072
    cntl = 262144
    opt = 524288
    cmd = 1048576
    idk1 = 2097152 # numberic pad
    idk2 = 4194304 # help
    idk3 = 8388608 # secondary fn
    #idk4 = 16777216 # alphashift stateless


    symbolicHotKeysList = {
        # See https://github.com/NUIKit/CGSInternal/blob/master/CGSHotKeys.h
        # See https://krypted.com/mac-os-x/defaults-symbolichotkeys/
        # System Prefs, Keyboard, Keyboard, Modifier Keys... are stored in ~/Library/Preferences/ByHost/.GlobalPreferences.UUID.plist under com.apple.keyboard.modifiermapping.alt_handler_id-61 HIDKeyboardModifierMappingDst:int HIDKeyboardModifierMappingSrc:int
        # System Prefs, Keyboard, Keyboard, User F1, F2, etc. keys as standard function keys are stored in ~/Library/Preferences/.GlobalPreferences.plist under com.apple.keyboard.fnState:bool
        # System Prefs, Keyboard, Shortcuts, Input Sources (more than one Input Source needs to be selected for this to be visible)
        'SelectPreviousInputSource':            {'num':60, 'parameters':[ord(' '), kc['Space'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Input Sources, Select the previous input source
        'SelectNextInputSource':                {'num':61, 'parameters':[ord(' '), kc['Space'], cntl+opt],                'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Input Sources, Select the next source in Input menu
        # System Prefs, Keyboard, Shortcuts, Launchpad & Dock
        'ToggleDockVisibility':                    {'num':52, 'parameters':[ord('d'), kc['D'], cmd+opt],                     'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Launchpad & Dock, Turn Dock Hiding On/Off
        'ShowLaunchpad':                        {'num':160, 'parameters':[no_ascii, no_ascii, 0],                         'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Launchpad & Dock, Show Launchpad
        # System Prefs, Keyboard, Shortcuts, Display
        #     https://apple.stackexchange.com/questions/287614/disable-f14-f15-for-brightness-control
        #     /usr/libexec/PlistBuddy -c "Set :AppleSymbolicHotKeys:53:enabled false" ~/Library/Preferences/com.apple.symbolichotkeys.plist
        #     /usr/libexec/PlistBuddy -c "Set :AppleSymbolicHotKeys:54:enabled false" ~/Library/Preferences/com.apple.symbolichotkeys.plist
        #     /usr/libexec/PlistBuddy -c "Set :AppleSymbolicHotKeys:55:enabled false" ~/Library/Preferences/com.apple.symbolichotkeys.plist
        #     /usr/libexec/PlistBuddy -c "Set :AppleSymbolicHotKeys:56:enabled false" ~/Library/Preferences/com.apple.symbolichotkeys.plist
        # System Prefs, Keyboard, Shortcuts, Mission Control
        'ExposeAllWindows':                        {'num':32, 'parameters':[no_ascii, kc['UpArrow'], idk1+idk3+cntl],         'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Mission Control
        'ExposeAllWindowsSlow':                    {'num':34, 'parameters':[no_ascii, kc['UpArrow'], idk1+idk3+cntl+shift],'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Mission Control (Slow) - didn't work for me
        'ShowNotificationCenter':                {'num':163, 'parameters':[no_ascii, no_ascii, 0],                         'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Show Notification Center
        'ToggleDoNotDisturb':                    {'num':175, 'parameters':[no_ascii, no_ascii, 0],                         'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Turn Do Not Disturb On/Off
        'ExposeApplicationWindows':                {'num':33, 'parameters':[no_ascii, kc['DownArrow'], idk3+cntl],         'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Application windows
        'ExposeApplicationWindowsSlow':            {'num':35, 'parameters':[no_ascii, kc['DownArrow'], idk3+cntl+shift],    'enabled':0, 'type':'standard' },    # System Prefs, Keyboard, Shortcuts, Mission Control, Application windows (Slow) - didn't work for me
        'ExposeDesktop':                        {'num':36, 'parameters':[no_ascii, kc['F11'], idk3],                     'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Show Desktop
        'ExposeDesktopsSlow':                    {'num':37, 'parameters':[no_ascii, kc['F11'], idk3+shift],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Show Desktop (Slow) - didn't work for me
        'Dashboard':                            {'num':62, 'parameters':[no_ascii, kc['F12'], idk3],                     'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Show Dashboard
        'DashboardSlow':                        {'num':63, 'parameters':[no_ascii, kc['F12'], idk3+shift],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Show Dashboard (Slow) - didn't work for me
        'SpaceLeft':                            {'num':79, 'parameters':[no_ascii, kc['LeftArrow'], idk3+cntl],         'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Move left a space
        'SpaceRight':                            {'num':81, 'parameters':[no_ascii, kc['RightArrow'], idk3+cntl],         'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Move right a space
        'SwitchToDesktop1':                        {'num':118, 'parameters':[no_ascii, kc['1'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 1
        'SwitchToDesktop2':                        {'num':119, 'parameters':[no_ascii, kc['2'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 2
        'SwitchToDesktop3':                        {'num':120, 'parameters':[no_ascii, kc['3'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 3
        'SwitchToDesktop4':                        {'num':121, 'parameters':[no_ascii, kc['4'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 4
        'SwitchToDesktop5':                        {'num':122, 'parameters':[no_ascii, kc['5'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 5
        'SwitchToDesktop6':                        {'num':123, 'parameters':[no_ascii, kc['6'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 6
        'SwitchToDesktop7':                        {'num':124, 'parameters':[no_ascii, kc['7'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 7
        'SwitchToDesktop8':                        {'num':125, 'parameters':[no_ascii, kc['8'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 8
        'SwitchToDesktop9':                        {'num':126, 'parameters':[no_ascii, kc['9'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 9
        'SwitchToDesktop10':                    {'num':127, 'parameters':[no_ascii, kc['0'], cntl],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 10
        'SwitchToDesktop11':                    {'num':128, 'parameters':[no_ascii, kc['1'], cntl+opt],                 'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 11
        'SwitchToDesktop12':                    {'num':129, 'parameters':[no_ascii, kc['2'], cntl+opt],                 'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 12
        'SwitchToDesktop13':                    {'num':130, 'parameters':[no_ascii, kc['3'], cntl+opt],                 'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Mission Control, Switch to Desktop 13
        # etc, how many spaces can you get?...
        # System Prefs, Keyboard, Shortcuts, Keyboard
        'FocusNextControl':                        {'num':13, 'parameters':[no_ascii, kc['F7'], idk3+cntl],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Change the way Tab moves focus
        'ToggleFullKeyboardAccess':                {'num':12, 'parameters':[no_ascii, kc['F1'], idk3+cntl],                'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Turn keyboard access on or off
        'FocusMenuBar':                            {'num':7, 'parameters':[no_ascii, kc['F2'], idk3+cntl],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to the menu bar
        'FocusDock':                            {'num':8, 'parameters':[no_ascii, kc['F3'], idk3+cntl],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to the Dock
        'FocusNextGlobalWindow':                {'num':9, 'parameters':[no_ascii, kc['F4'], idk3+cntl],                 'enabled':1, 'type':'standard' },    # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to active or next window
        'FocusToolbar':                            {'num':10, 'parameters':[no_ascii, kc['F5'], idk3+cntl],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to window toolbar
        'FocusFloatingWindow':                    {'num':11, 'parameters':[no_ascii, kc['F6'], idk3+cntl],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to floating window
        'FocusApplicationWindow':                {'num':27, 'parameters':[ord('`'), kc['Grave'], cmd],                     'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to the next window
        'FocusDrawer':                            {'num':51, 'parameters':[ord('`'), kc['Grave'], cmd+opt],                'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to the window drawer
        'FocusStatusItems':                        {'num':57, 'parameters':[no_ascii, kc['F8'], idk3+cntl],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Keyboard, Move focus to the status menus
        # System Prefs, Keyboard, Shortcuts, Screenshots
        'Screenshot':                            {'num':28, 'parameters':[ord('3'), kc['3'], cmd+shift],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Screenshots, Save picture of screen as file
        'ScreenshotToClipboard':                {'num':29, 'parameters':[ord('3'), kc['3'], cmd+cntl+shift],             'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Screenshots, Copy picture of screen to the clipboard
        'ScreenshotRegion':                        {'num':30, 'parameters':[ord('4'), kc['4'], cmd+shift],                    'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Screenshots, Save picture of selected area as file
        'ScreenshotRegionToClipboard':            {'num':31, 'parameters':[ord('4'), kc['4'], cmd+cntl+shift],             'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Screenshots, Copy picture of selected area to the clipboard
        'SnapshotRecording':                    {'num':184, 'parameters':[ord('5'), kc['5'], cmd+shift],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Screenshots, Screenshot and recording options
        # System Prefs, Keyboard, Shortcuts, Services
        # System Prefs, Keyboard, Shortcuts, Spotlight
        'SpotlightSearchField':                    {'num':64, 'parameters':[no_ascii, kc['Space'], cmd],                     'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Spotlight, Show Spotlight search
        'SpotlightWindow':                        {'num':65, 'parameters':[no_ascii, kc['Space'], cmd+opt],                 'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Spotlight, Show Finder search window
        # System Prefs, Keyboard, Shortcuts, Accessibility
        'ToggleZoom':                            {'num':15, 'parameters':[ord('8'), kc['8'], cmd+opt],                     'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Zoom, Turn zoom on or off
        'ZoomToggleSmoothing':                    {'num':23, 'parameters':[ord('\\'), kc['Backslash'], cmd+opt],             'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Zoom, Turn image image smoothing on or off
        'ZoomOut':                                {'num':19, 'parameters':[ord('-'), kc['Minus'], cmd+opt],                 'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Zoom, Zoom out
        'ZoomIn':                                {'num':17, 'parameters':[ord('='), kc['Equal'], cmd+opt],                 'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Zoom, Zoom in
        'ToggleFocusFollowing':                    {'num':179, 'parameters':[no_ascii, no_ascii, 0],                         'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Zoom, Turn focus following on or off
        'IncreaseContrast':                        {'num':25, 'parameters':[ord('.'), kc['Period'], cmd+cntl+opt],            'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Contrast, Increase contrast
        'DecreaseContrast':                        {'num':26, 'parameters':[ord(','), kc['Comma'], cmd+cntl+opt],             'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Contrast, Decrease contrast
        'InvertScreen':                            {'num':21, 'parameters':[ord('8'), kc['8'], cmd+cntl+opt],                 'enabled':0, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Invert colors
        'ToggleVoiceOver':                        {'num':59, 'parameters':[no_ascii, kc['F5'], idk3+cmd],                    'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Turn VoiceOver on or off
        'ShowAccessibilityControls':            {'num':162, 'parameters':[no_ascii, kc['F5'], idk3+cmd+opt],             'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, Accessibility, Show Accessibility controls
        # System Prefs, Keyboard, Shortcuts, App Shortcuts
        'Help':                                    {'num':98, 'parameters':[ord('/'), kc['Slash'], cmd+shift],             'enabled':1, 'type':'standard' },     # System Prefs, Keyboard, Shortcuts, App Shortcuts, Show Help menu
        # System Prefs, Keyboard, Dictation
        'DictationShortcut':                    {'num':164, 'parameters':[8388608, 18446744073701163007],                 'enabled':1, 'type':'modifier' },     # System Prefs, Keyboard, Dictation, Shortcut
                                                            # 8388608, 18446744073701163007 = Press Fn (Function) Key Twice
                                                            # 1048592, 18446744073708503023 = Press Right Command Key Twice
                                                            # 1048584, 18446744073708503031 = Press Left Command Key Twice
                                                            # 1048576, 18446744073708503039 = Press Either Command Key Twice
                                                            # Or specify 3 values for a keyboard shortcut and change the type to standard
    #     '':                                        {'num':38, 'parameters':[none, none, 0],                                 'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':39, 'parameters':[shift, shift, 0],                                 'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':40, 'parameters':[none, none, shift],                             'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':41, 'parameters':[shift, shift, shift],                             'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':42, 'parameters':[cntl, cntl, 0],                                 'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':43, 'parameters':[cntl, cntl, shift],                             'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':66, 'parameters':[opt, opt, 0],                                     'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':67, 'parameters':[opt, opt, shift],                                 'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':71, 'parameters':[cmd, cmd, 0],                                     'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':72, 'parameters':[idk1, idk1, 0],                                 'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':87, 'parameters':[idk2, idk2, 0],                                 'enabled':0, 'type':'button' },     #
    #     '':                                        {'num':88, 'parameters':[idk2, idk2, shift],                             'enabled':0, 'type':'button' },        #
    #     '':                                        {'num':80, 'parameters':[no_ascii, kc['LeftArrow'], idk3+cntl+shift],     'enabled':1, 'type':'standard' },     #
    #     '':                                        {'num':82, 'parameters':[no_ascii, kc['RightArrow'], idk3+cntl+shift],     'enabled':1, 'type':'standard' },     #
    }

    for binding, pref_dict in symbolicHotKeysList.items():
        enableName='KeyboardShortcuts.User.'+binding+'Enable'
        pref_list[enableName] = {
            'help':enableName+pref_delim+'<true|false> - "Enable or disable a keyboard shortcut"; 1 arg: true/false; user domain (10.14)',
            'unit_tests':[enableName+pref_delim+"true",],
            '10.14':[
                { 'type':'PlistBuddy', 'domain':'com.apple.symbolichotkeys', 'command':'Set', 'args':['AppleSymbolicHotKeys:'+str(pref_dict['num'])+':enabled %ARG0%'], 'arg_count':1, },
            ],
        }

# TODO
#         setkeyName='KeyboardShortcuts.User.'+binding+'SetKey'
#         pref_list[setkeyName] = {}
#             'help':setkeyName+pref_delim+'SOMETHING - "Set a keyboard shortcut"; 1 arg: true/false; user domain (10.14)',
#             'unit_tests':[setkeyName+pref_delim+"cmd+shift-R",],
#             'pre_run_func':'decodeSymbolicHotKeysList',
#         }
#
# def decodeSymbolicHotKeysList():
#             '10.14':[
#                 { 'type':'PlistBuddy', 'domain':'com.apple.symbolichotkeys', 'command':'Set', 'args':['AppleSymbolicHotKeys:'+str(pref_dict['num'])+':enabled %ARG0%'], 'arg_count':1, },
#             ],

buildSysbolicHotkeys(pref_list)

def disable_touristd():
    #https://carlashley.com/2016/10/19/com-apple-touristd/
    #https://aporlebeke.wordpress.com/2020/01/10/2019-mac-macos-updates-to-apples-tours-com-apple-touristd/
    my_os = get_short_os_version()
    if my_os == '10.12':
        text = sh( '/usr/libexec/PlistBuddy -c Print -x "/System/Library/PrivateFrameworks/Tourist.framework/Resources/Tours.plist" | grep https://' )
        text = text.split("\n")
        defaults_command = [ { 'type':'defaults', 'domain':'com.apple.touristd', 'args':['firstOSLogin', '-date', '2018-1-1'], } ]
        for url in text:
            if url != '':
                url = re.sub(r'.*<string>([^<]*).*', r'\1', url)
                defaults_command.append( { 'type':'defaults', 'domain':'com.apple.touristd', 'args':['seed-'+url, '-date', '2018-1-1'], 'user':True, } )
        pref_list['Tourist.User.disable']['10.12'] = defaults_command
    else:
        # Get (and update) this list with `curl https://help.apple.com/macOS/config.json | grep "\"id\""`
        text = [
            'seed-viewed-/+vP78HsSh+Yeb4xJnUT9A',
            'seed-viewed-+trJt2VsTvK1yfPGwOySDw',
            'seed-viewed-2+LvxAVyT6qnV1sDMZT0NA',
            'seed-viewed-40reAuuYTHOsx4oGcx4qrA',
            'seed-viewed-APhNaYV1RxSS41lC7ZJJ9Q',
            'seed-viewed-aytyxqEmTIOvEz3iS4IbkA',
            'seed-viewed-b/dLke8ZTQaN9KKrxfwDQw',
            'seed-viewed-B70mVuHeT0WUgKh/VdUuZQ',
            'seed-viewed-baXokbqsQ/2KLkzIZrR6ng',
            'seed-viewed-bydF6fX5Sp6aBYdEXD0VwQ',
            'seed-viewed-catalina_early-2020_macbook-air',
            'seed-viewed-catalina_early-2020_macbook-pro-13',
            'seed-viewed-catalina_imac',
            'seed-viewed-catalina_imac-21a',
            'seed-viewed-catalina_imac-pro',
            'seed-viewed-catalina_late-2019_macbook-pro',
            'seed-viewed-catalina_mac_basics',
            'seed-viewed-catalina_mac-mini',
            'seed-viewed-catalina_mac-pro',
            'seed-viewed-catalina_macbook-air',
            'seed-viewed-catalina_macbook-pro',
            'seed-viewed-catalina_macbook-pro-13',
            'seed-viewed-catalina_whats_new',
            'seed-viewed-d+gfl8CNTNeauANKjf9WqA',
            'seed-viewed-EBFV2ZqnQiaqrZhvyifLeQ',
            'seed-viewed-EeEFv8cyS0CVe3ia2UEehA',
            'seed-viewed-ETJeJ9/1QmmWUde7uK8fDg',
            'seed-viewed-EWfaSdJwR/6f1BYGiyLpcQ',
            'seed-viewed-f/Pn3F4RScOh+GUBKO9sRA',
            'seed-viewed-FQrkbNP9ThKQQtpqx2saFg',
            'seed-viewed-fWRpNw7IR3S3qxX63nmvMw',
            'seed-viewed-GZAJdmpdSqmfH2PkCr8ebw',
            'seed-viewed-hP2OZh+MTEKeFcjgec2gZw',
            'seed-viewed-JTecrrXDSVut2tSfltty9Q',
            'seed-viewed-kIFAGHvXTAepRptQXiXe5w',
            'seed-viewed-krdWS8DSQIqJSqQFXW1/pw',
            'seed-viewed-kti4ZkMKQFyCL2kbgCY23A',
            'seed-viewed-KwUoo0fRRM2VPmIm0V67xg',
            'seed-viewed-lEDfW5O+SZe8KTQ93HGOPA',
            'seed-viewed-lQlm1yrMS0GPVyAL44id+A',
            'seed-viewed-LR2P9+rnQ2q9xSUy1ZgWOw',
            'seed-viewed-MM3ne3nTR9eXFyVwZ5gN7Q',
            'seed-viewed-N0bfKOvERSiAp06mHOcgOQ',
            'seed-viewed-n87FVu1TSwGzble8vqBvsg',
            'seed-viewed-Pa88nesPSO6POlutVN4/Sg',
            'seed-viewed-pDWyREoARJm5V1mJYr9GKg',
            'seed-viewed-SdV08ZZQRxOCWq6JBEXmfg',
            'seed-viewed-SkI/dLAkQu6k/qpzSOG6Iw',
            'seed-viewed-srluh6uOQiuWCzxguqhDNw',
            'seed-viewed-Tu81gKhDTvmNkjyqcPBfKA',
            'seed-viewed-UhiR1M79RWmXLIQr4M0AWw',
            'seed-viewed-We59wh+OTa6c1yas/yppwg',
            'seed-viewed-WEyaCPMVRB6HbnmRq9EnNQ',
            'seed-https://help.apple.com/macOS/mojave/mac-basics',
            'seed-https://help.apple.com/macOS/mojave/whats-new',
        ]
        defaults_command = [ { 'type':'defaults', 'domain':'com.apple.touristd', 'args':['firstOSLogin', '-date', '2020-5-24'], } ]
        for id in text:
            defaults_command.append( { 'type':'defaults', 'domain':'com.apple.touristd', 'args':[id, '-date', '2020-5-24'], 'user':True, } )
        pref_list['Tourist.User.disable']['10.13'] = defaults_command

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
    return sh("/usr/bin/stat /dev/console | awk '{print $5}'").rstrip('\n')

def get_pref_dir(user_dir, username):
    if username != None:
        if user_dir == None:
            try:
                user_dir = pwd.getpwnam(username).pw_dir
            except:
                print "Could not find username: " + username
                sys.exit(1)
        pref_dir = user_dir + '/Library/Preferences/'
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
    return sh("/usr/sbin/ioreg -rd1 -c IOPlatformExpertDevice | grep -i 'UUID' | cut -c27-62").rstrip('\n')

def versiontuple(v):
    return tuple(map(int, (v.split("."))))

def pref_unit_tests(args):
    name = os.path.basename(sys.argv[0])
    for pref_name, pref_data in sorted( pref_list.iteritems() ):
        if 'unit_tests' in pref_data:
            for unit_test in pref_data['unit_tests']:
                if unit_test != '':
                    print( "%s pref %s" % (name,unit_test) )
                    #pref(unit_test.split(" "))

def pref(args):
    pref_os = None
    force_path = None
    username = None
    user_dir = None
    pref_dir = None
    macUUID = None
    try:
        (optargs, rargs) = getopt.getopt(args, 'o:p:P:RTu:')
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
        elif opt == '-R':
            user_dir = '/private/var/root'
            username = 'root'
    if len( rargs ) == 0:
        usage('You must specify arguments', 'pref')
    sys_args = rargs

    # Make sure the command exists
    command_parts = rargs[0].split(pref_delim, 1)
    command_name = command_parts[0]
    if not command_name in pref_list:
        usage('Can\'t find setting "' + command_name + '"', 'pref')
    command_prefs = pref_list[command_name]

    # Pre-run stuff
    if 'pre_run_func' in command_prefs:
        pre_run_func = command_prefs['pre_run_func']
        if pre_run_func in globals():
            globals()[pre_run_func]()
        else:
            print 'Script error: there is no function named "' + pre_run_func + '"'
            sys.exit(1)

    # Find the commands for this OS
    if verbose:
        print 'Finding the OS'
    if pref_os == None:
        pref_os = get_short_os_version()

    if pref_os in command_prefs:
        run_these_commands = command_prefs[pref_os]
    elif 'versions' in command_prefs and pref_os in command_prefs['versions']:
        run_these_commands = command_prefs[command_prefs['versions'][pref_os]]
    else:
        temp_versions = []
        min_os = -1
        max_os = -1
        for key in command_prefs:
            if re.match("^(\d\d.\d+)$", key):
                if min_os == -1:
                    min_os = key
                    max_os = key
                elif versiontuple(key) < versiontuple(min_os):
                    min_os = key
                elif versiontuple(key) > versiontuple(max_os):
                    max_os = key
        if versiontuple(pref_os) < versiontuple(min_os):
            run_these_commands = command_prefs[min_os]
        elif versiontuple(pref_os) > versiontuple(max_os):
            run_these_commands = command_prefs[max_os]
        else:
            print 'Script error: "' + command_name + '", the OS, "' + pref_os +'", falls between the OS versions specified for this command and I can\'t tell which one to use. Please enter all versions in the version hash for this command.'
            sys.exit(1)

    # Break the command name apart to find out if it's running as user
    command_name_parts = command_name.split(".")
    if command_name_parts[1] == 'User':
        command_prefs['user'] = True

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

            # Path to file (if it's defaults or PlistBuddy)
            if data['type'] == 'defaults' or data['type'] == 'PlistBuddy':
                # Complete the path to the preferences
                if force_path != None:
                    pref_path = force_path
                else:
                    if pref_dir == None:
                        pref_dir = get_pref_dir(user_dir, username)
                        if macUUID != None:
                            pref_dir += 'ByHost/'
                    domain = get_domain(data, command_parts)
                    if macUUID != None: # ///////// on 10.14, when run as a user, this puts the macUUID twice
                        pref_path = pref_dir + domain + '.' + macUUID + '.plist'
                    else:
                        pref_path = pref_dir + domain + '.plist'

            # Defaults
            if data['type'] == 'defaults':
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
                if username != None:
                    chown_these_files[pref_path] = [ '/usr/sbin/chown', username + ':' + group, pref_path ]

            # PlistBuddy
            elif data['type'] == 'PlistBuddy':
                # defaults command type (write or delete)
                command_type = 'Set'
                if 'command' in data:
                    command_type = data['command']

                # The command
                if command_args == None or len(command_args) > 1:
                    print 'Script error: PlistBuddy requires an argument.  Args: ' + '('+str(command_args)+').'
                    sys.exit(1)
                if command_type == "Delete" and not os.path.exists(pref_path):
                    print 'PlistBuddy can\'t delete '+command_args[0]+' because '+pref_path+' doesn\'t exist'
                else:
                    command = [ '/usr/libexec/PlistBuddy', '-c', command_type+' '+command_args[0], pref_path ]
                    commands.append( command )
                    # Add a chown if it's in the user homedir
                    if username != None:
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
    sh("/usr/bin/say " + ' '.join(args))

##########################################################################################

mak_commands['ard_user'] = {
    'help':'ard_userHelp',
    'main':'ard_user',
}

def ard_userHelp(name):
    return '''Usage: %s [<options>] ard_user [-c] <username[,username..]> [setting[ setting..]]

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
    kickstart = '/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart'
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
        privs = ['-ChangeSettings', '-ControlObserve', '-DeleteFiles', '-GenerateReports', '-OpenQuitApps', '-RestartShutDown', '-SendFiles', '-ShowObserve', '-TextMessages']
    sh( kickstart + '-deactivate -configure -access -off' )
    sh( '/usr/bin/defaults write /Library/Preferences/com.apple.RemoteManagement ARD_AllLocalUsers -bool FALSE' )
    if clear:
        if verbose:
            print 'Removing all previous ARD priveledges from all users'
        ard_users = sh('/usr/bin/dscl . list /Users naprivs | awk \'{print $1}\'')
        ard_users = ard_users.split("\n")
        for user in ard_users:
            if user != None and user != '':
                sh( '/usr/bin/dscl . delete /Users/' + user + ' naprivs' )
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
    return '''Usage: %s [<options>] hack_jamf_hooks [value]

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
            usage('I don\'t understand ' + args[0], 'hack_jamf_hooks')
    elif len(args) > 1:
        usage( 'I only understand one value.', 'hack_jamf_hooks' )
    sh('/usr/bin/sed -i .orig "s/checkJSSConnection -retry [0-9]* ;/checkJSSConnection -retry '+value+' ;/g" /Library/Application\ Support/JAMF/ManagementFrameworkScripts/loginhook.sh')

##########################################################################################

mak_commands['launchdaemon'] = {
    'help':'launchdaemonHelp',
    'main':'launchdaemon',
}

def launchdaemonHelp(name):
    return '''Usage: %s [<options>] launchdaemon [<options>] <plist_file> <program arg> [<program arg>..] [;|:] <key> <value> [<key> <value>..]

    -x don't unload and reload the plist with launchctl (the default will attempt to unload it if it exists, change the file, then reload)

    plist_file must be of form /path/label.plist

    Array or dictionary items (like program arguments) must be terminated with ";" (don't forget to quote or escape it) or ":".

    https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html
    https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man5/plist.5.html
    https://en.wikipedia.org/wiki/Launchd

    Examples:
        %s launchdaemon /Library/LaunchDaemons/example.plist echo hi \; StartCalendarInterval Hour 4 Minute 0 Weekday 0 \;
        %s launchdaemon /Library/LaunchDaemons/example.plist echo hi \; StandardOutPath /var/log/complete_enrollment.log StandardErrorPath /var/log/complete_enrollment.err.log RunAtLoad 1
        %s launchdaemon /Library/LaunchDaemons/example.plist echo hi \; WatchPaths /Library/Admin/launchdwatch \;
        %s launchdaemon /Library/LaunchAgents/example.plist /Applications/Safari.app/Contents/MacOS/Safari \; LimitLoadToSessionType Aqua RunAtLoad 1 \;

''' % (name,name,name,name,name)

def parseLaunchdPlist(args):
    hash = dict()
    key1 = None
    key2 = None
    bucket = None
    for arg in args:
        if key1 == None:
            key1 = arg
        # String
        elif key1 in ['Label', 'WorkingDirectory', 'GroupName', 'StandardOutPath', 'StandardErrorPath', 'UserName', 'LimitLoadToSessionType']:
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
            if arg == ';' or arg == ':':
                hash[key1] = bucket
                key1 = None
                bucket = None
            else:
                bucket.append( arg )
        # Dict
        elif key1 in ['StartCalendarInterval']:
            if bucket == None:
                bucket = {}
            if arg == ';' or arg == ':':
                hash[key1] = bucket
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
                hash[key1] = False
                key1 = None
            elif arg == '1':
                hash[key1] = True
                key1 = None
            else:
                usage( 'KeepAlive Dictionary is not done.', 'launchdaemon' )
        else:
            usage( 'Unknown key: '+key1, 'launchdaemon' )
    if bucket != None and len(bucket) > 0:
        usage('Terminate multi-item values with ";" (don\'t forget to escape it) or ":".', 'launchdaemon')
    return hash

def launchdaemon(args):
    import plistlib
    reload = True
    try:
        (optargs, rargs) = getopt.getopt(args, 'x')
    except getopt.GetoptError, e:
        print e
        sys.exit(2)
    for opt, arg in optargs:
        if opt == '-x':
            reload = False
    if len(rargs) <= 3:
        usage( 'You must have a path, program arguments, and a trigger condition', 'launchdaemon' )
    path = rargs[0]
    label = re.sub(r'.*\/([^\/])\.plist$', r'\1', path)
    if label == '':
        usage('Could not build a label from the path, did the path end with ".plist"?', 'launchdaemon')
    debug_print( 'Label: '+label )
    flag = True
    program_args = []
    ii = 1
    while flag:
        if ii >= len(rargs):
            usage('You must terminate ProgramArguments items with ";" (don\'t forget to escape it) or ":".', 'launchdaemon')
        if rargs[ii] != ';' and rargs[ii] != ':':
            if rargs[ii][-1] == ';' or rargs[ii][-1] == ':':
                rargs[ii] = rargs[ii][:-1]
                flag = False
            program_args.append( rargs[ii] )
            ii += 1
        else:
            flag = False
    rargs = rargs[ii+1:]
    debug_print( program_args, rargs )
    if os.path.exists( path ):
        sh( '/bin/launchct unload ' + path )
    plist = parseLaunchdPlist(rargs)
    plist['Label'] = label
    plist['ProgramArguments'] = program_args
    plistlib.writePlist( plist, path )
    sh( '/bin/launchct load ' + path )

##########################################################################################

mak_commands['locatedb'] = {
    'help':'locatedbHelp',
    'main':'locatedb',
}

def locatedbHelp(name):
    return '''Usage: %s [<options>] locatedb

    Loads locate db

''' % (name)

def locatedb(args):
    sh( '/bin/launchctl load -w /System/Library/LaunchDaemons/com.apple.locate.plist' )

##########################################################################################

mak_commands['networksetup'] = {
    'help':'networksetupHelp',
    'main':'networksetup',
}

def networksetupHelp(name):
    return '''Usage: %s [<options>] networksetup ...

    This is just a shortcut to /usr/sbin/networksetup.  See `man networksetup` for options.

    Why?  Because I'll forget about networksetup otherwise (it's not like I use the command
    very much).

    Example:
        %s networksetup -setdnsservers Ethernet 172.20.120.20

''' % (name,name)

def networksetup(args):
    return sh( '/usr/sbin/networksetup ' + ' '.join(args) )

##########################################################################################

mak_commands['scutil'] = {
    'help':'scutilHelp',
    'main':'scutil',
}

def scutilHelp(name):
    return '''Usage: %s [<options>] scutil ...

    This is just a shortcut to /usr/sbin/scutil.  See `man scutil` for options.

    Why?  Because I'll forget about scutil otherwise (it's not like I use the command
    very much).

    Example:
        %s scutil --set ComputerName "alpha centauri"
        %s scutil --set HostName alpha
        %s scutil --set LocalHostName centauri
        %s scutil --get HostName

''' % (name,name,name,name,name)

def scutil(args):
    return sh( '/usr/sbin/scutil ' + ' '.join(args) )

##########################################################################################

mak_commands['set_volume'] = {
    'help':'set_volumeHelp',
    'main':'set_volume',
}

def set_volumeHelp(name):
    return '''Usage: %s [<options>] set_volume <Volume> [<Output Volume>] [<Input Volume>]

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
                sh( "/usr/bin/osascript -e 'set volume "+bla[0]+args[ii]+"'" )
            else:
                usage( args[ii]+' is not between 0 and '+str(bla[1]), 'set_volume' )

##########################################################################################

mak_commands['shell_paths'] = {
    'help':'shell_pathsHelp',
    'main':'shell_paths',
}

def shell_pathsHelp(name):
    return '''Usage: %s [<options>] shell_paths <path> <name>

    Adds the <path> to /private/etc/paths.d/<name>

    Example:
        %s shell_paths /usr/local/bin usr_local_bin

''' % (name,name)

def shell_paths(args):
    if len(args) != 2:
        usage( 'Missing arguments', 'shell_paths' )
    search = args[0]
    path = '/private/etc/paths.d/' + args[1]
    debug_print( 'Saving "' + search + '" to ' + path )
    with open(path, 'w') as file:
        file.write(search)

##########################################################################################

mak_commands['systemsetup'] = {
    'help':'systemsetupHelp',
    'main':'systemsetup',
}

def systemsetupHelp(name):
    return '''Usage: %s [<options>] systemsetup ...

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

mak_commands['uvar'] = {
    'help':'uvarHelp',
    'main':'uvar',
}

def uvarHelp(name):
    return '''Usage: %s [<options>] uvar <path> <variable> <value> [<backup extension>]

    Unix VARiable.  This will search <path> for the first instance of "^<variable>" and
    change it to "<variable><value>" if it's not set (using sed).  If "^<variable>"
    doesn't occur then "<variable><value>" will be appended to the end (surrounded by
    linefeeds).

    The optional backup extension will save a backup with the specified extension.

    Examples:
        %s uvar /etc/postfix/main.cf relayhost " = example.com" .bak
        %s uvar /etc/ssh/sshd_config AllowUsers " james spencer" .bak
        %s uvar /etc/ssh/sshd_config XAuthLocation " /opt/X11/bin/xauth"

''' % (name,name,name,name)

def uvar(args):
    if len(args) < 3:
        usage( 'Missing arguments', 'uvar' )
    path = args[0]
    var = args[1]
    val = args[2]
    ext = ( args[3] if len(args) == 4 else '' )
    if os.path.exists( path ):
        append = True
        sed = False
        with open(path, 'r') as file:
            for line in file:
                z = re.match("^"+var+"(.*)", line)
                if z:
                    append = False
                    if z.groups()[0] != val:
                        sed = True
                    elif debug or verbose:
                            print( 'Text "'+var+val+'" already present in '+path )
                    break
        if sed:
            sh2( [ "/usr/bin/sed", "-i", ext, "s/^"+var+".*/"+var+val+"/", path ] )
        if append:
            debug_print( 'Appending "' + var+val + '" to ' + path )
            if ext != '':
                copyfile(path, path+ext)
            with open(path, 'a') as file:
                file.write("\n"+var+val+"\n")
    else:
        usage( 'File ('+path+') does not exist', 'uvar' )

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def debug_print(*args):
    if debug or verbose:
        for cc, message in enumerate(args):
            print( message )

def sh(cmd):
    # Shell is true, expects a string
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
    # Shell is false (default), expects list or string containing a command without args
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
    return sh('/usr/bin/sw_vers -productVersion').rstrip('\n')

def get_short_os_version():
    return re.sub(r'(\d+\.\d+).*', r'\1', get_os_version())

def usage(e=None,help_command=None):
    if e:
        print e
        print ''
    if not quiet:
        name = os.path.basename(sys.argv[0])
        text = ''
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

Usage: %s [-dv] command options

    -d            Debug (verbose + some things aren't executed)
    -q            Quiet
    -v            Verbose
    --version     Print version and exit

Usage: %s [-t] command
    -t            DANGER: Run unit tests for command (used to debug prefs on a new OS)
                  WARNING! This will overwrite a lot of prefs! Run this on a computer that
                  can be thrown away like a snapshotted VM!

Commands
''' % (name, name)
            mak_commands_with_help = mak_commands.keys()
            mak_commands_with_help.append('help')
            for mak_command in sorted( mak_commands_with_help ):
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
            if help_command in mak_commands:
                text += globals()[mak_commands[help_command]['help']](name)
            else:
                usage("Unknown command name: " + help_command)
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
        (optargs, args) = getopt.getopt(sys.argv[argv_start:], 'do:qtv', ['version'])
    except getopt.GetoptError, e:
        print e
        sys.exit(2)
    global debug, verbose, quiet
    unit_tests = False
    for opt, arg in optargs:
        if opt == '-d':
            debug = True
        elif opt == '-q':
            quiet = True
        elif opt == '-t':
            unit_tests = True
        elif opt == '-v':
            verbose = True
        elif opt == '--version':
            print version
            sys.exit(0)
        if verbose and quiet:
            usage("Can't be verbos and quiet at the same time!")

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
            if unit_tests:
                confirm = raw_input("WARNING: This will overwrite lots of prefs, are you sure (y/N)? ") # Python 3 is input
                if confirm == "y":
                    if main_name in globals():
                        globals()[main_name+"_unit_tests"](args[1:])
                    else:
                        print 'Script error: there is no function named "' + main_name + '"'
                        sys.exit(1)
            else:
                if main_name in globals():
                    globals()[main_name](args[1:])
                else:
                    print 'Script error: there is no function named "' + main_name + '"'
                    sys.exit(1)
        else:
            usage('Unknown command: '+command)

if __name__ == '__main__':
    main()
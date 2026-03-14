[app]

# (str) Title of your application
title = Davidic Lyre

# (str) Package name — used as the Android package identifier segment
package.name = davidic_lyre

# (str) Package domain — combined with package.name to form the full Android
#       application ID: com.lefthandedluminary.davidic_lyre
package.domain = com.lefthandedluminary

# (str) Source code directory relative to this file
source.dir = .

# (list) File extensions to include from source.dir
source.include_exts = py,png,jpg,kv,atlas,wav

# (list) Additional directories to include verbatim in the APK
source.include_patterns = assets/audio/*,assets/images/*

# (str) Application version
version = 0.1.0

# (list) Application requirements — packages built for Android by python-for-android
requirements = python3,kivy,pyjnius,plyer,pillow

# (str) Presplash screen image (shown while the app is loading)
presplash.filename = %(source.dir)s/assets/images/presplash.png

# (str) Application icon
icon.filename = %(source.dir)s/assets/images/icon.png

# (str) Supported screen orientations
orientation = portrait

# (bool) Fullscreen mode — 0 keeps the status bar visible
fullscreen = 0

#
# Android-specific settings
#

# (int) Target Android API level
android.api = 34

# (int) Minimum Android API level supported
android.minapi = 26

# (int) Android NDK API level — must be >= android.minapi
android.ndk_api = 26

# (list) Target CPU architectures
android.archs = arm64-v8a, armeabi-v7a

# (list) Android permissions — none beyond the default READ/WRITE_EXTERNAL_STORAGE
#        needed by Kivy for audio.  Extend this list as new features require it.
# android.permissions =

# (bool) Enable AndroidX support libraries
android.enable_androidx = True

# (str) Android logcat filters for adb logcat (useful for debugging)
# android.logcat_filters = *:S python:D

#
# Python for Android bootstrap
#

# (str) Bootstrap to use — sdl2 is required by Kivy
p4a.bootstrap = sdl2

#
# Buildozer / build tool settings
#

# (int) Log verbosity: 0 = quiet, 1 = normal, 2 = verbose
log_level = 2

# (int) Display warning if buildozer is run as root (0 = suppress warning)
warn_on_root = 1

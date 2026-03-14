[app]
title = Davidic Lyre
package.name = davidic_lyre
package.domain = org.davidic

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav

version = 0.1.0

requirements = python3,kivy

# Samsung Galaxy Fold5 inner screen (unfolded portrait)
orientation = portrait

fullscreen = 0

android.permissions = VIBRATE
android.api = 33
android.minapi = 26
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a

# Target Samsung Fold5 inner display
android.window_softinput_mode = adjustResize

[buildozer]
log_level = 2
warn_on_root = 1

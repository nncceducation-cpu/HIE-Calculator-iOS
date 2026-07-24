#!/usr/bin/env python3
"""Post-`cap add android` fixups for the Codemagic Android build:
  1. Wire the release signingConfig so Codemagic's keystore (CM_* env vars)
     actually signs the AAB.
  2. Bump compile/target SDK to 35 (Google Play now requires targetSdk >= 35),
     with the matching Android Gradle Plugin (8.6.0) and Gradle (8.7).
All patches are idempotent and skip gracefully if a file is missing."""
import os
import re

# ---------------------------------------------------------------- 1. signing
APP_GRADLE = "android/app/build.gradle"
if os.path.exists(APP_GRADLE):
    with open(APP_GRADLE) as f:
        s = f.read()

    signing_block = '''    signingConfigs {
        release {
            storeFile file(System.getenv("CM_KEYSTORE_PATH"))
            storePassword System.getenv("CM_KEYSTORE_PASSWORD")
            keyAlias System.getenv("CM_KEY_ALIAS")
            keyPassword System.getenv("CM_KEY_PASSWORD")
        }
    }
'''
    if "signingConfigs" not in s:
        marker = "android {"
        idx = s.index(marker) + len(marker)
        nl = s.index("\n", idx)
        s = s[:nl + 1] + signing_block + s[nl + 1:]

    if "signingConfig signingConfigs.release" not in s:
        s = re.sub(
            r'(buildTypes\s*\{\s*\n\s*release\s*\{\s*\n)',
            r'\1            signingConfig signingConfigs.release\n',
            s, count=1)

    with open(APP_GRADLE, "w") as f:
        f.write(s)
    print("sign-patch: release signing wired into build.gradle")

# ------------------------------------------------- 2. SDK / AGP / Gradle bumps
VARIABLES = "android/variables.gradle"
if os.path.exists(VARIABLES):
    with open(VARIABLES) as f:
        v = f.read()
    v = re.sub(r'compileSdkVersion\s*=\s*\d+', 'compileSdkVersion = 35', v)
    v = re.sub(r'targetSdkVersion\s*=\s*\d+', 'targetSdkVersion = 35', v)
    with open(VARIABLES, "w") as f:
        f.write(v)
    print("sign-patch: compile/target SDK set to 35")

PROJ_GRADLE = "android/build.gradle"
if os.path.exists(PROJ_GRADLE):
    with open(PROJ_GRADLE) as f:
        b = f.read()
    b = re.sub(r'com\.android\.tools\.build:gradle:[0-9.]+',
               'com.android.tools.build:gradle:8.6.0', b)
    with open(PROJ_GRADLE, "w") as f:
        f.write(b)
    print("sign-patch: Android Gradle Plugin set to 8.6.0")

WRAPPER = "android/gradle/wrapper/gradle-wrapper.properties"
if os.path.exists(WRAPPER):
    with open(WRAPPER) as f:
        w = f.read()
    w = re.sub(r'gradle-[0-9.]+-(all|bin)\.zip', 'gradle-8.7-all.zip', w)
    with open(WRAPPER, "w") as f:
        f.write(w)
    print("sign-patch: Gradle wrapper set to 8.7")

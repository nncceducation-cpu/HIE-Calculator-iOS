#!/usr/bin/env python3
"""Inject a release signingConfig into the Capacitor-generated
android/app/build.gradle so Codemagic's keystore (exported as CM_* env vars)
actually signs the release AAB. Idempotent."""
import re

PATH = "android/app/build.gradle"
with open(PATH) as f:
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

# Attach the signing config to the release build type (only the buildTypes>release,
# not the signingConfigs>release we just inserted).
if "signingConfig signingConfigs.release" not in s:
    s = re.sub(
        r'(buildTypes\s*\{\s*\n\s*release\s*\{\s*\n)',
        r'\1            signingConfig signingConfigs.release\n',
        s, count=1)

with open(PATH, "w") as f:
    f.write(s)

print("sign-patch: release signing wired into build.gradle")

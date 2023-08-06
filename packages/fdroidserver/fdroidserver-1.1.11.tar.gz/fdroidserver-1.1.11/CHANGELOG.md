
### 1.1.4 (2019-08-15)

* include bitcoin validation regex required by fdroiddata

* merged Debian patches to fix test suite there

### 1.1.3 (2019-07-03)

* fixed test suite when run from source tarball

* fixed test runs in Debian

### 1.1.2 (2019-03-29)

* fix bug while downloading repo index ([!636](https://gitlab.com/fdroid/fdroidserver/merge_requests/636))

### 1.1.1 (2019-02-03)

* support APK Signature v2 and v3

* all SDK Version values are output as integers in the index JSON

* take graphics from Fastlane dirs using any valid RFC5646 locale

* print warning if not running in UTF-8 encoding

* fdroid build: hide --on-server cli flag

### 1.1 (2019-01-28)

* a huge update with many fixes and new features:
  https://gitlab.com/fdroid/fdroidserver/milestones/7

* can run without and Android SDK installed

* much more reliable operation with large binary APK collections

* sync all translations, including newly added languages: hu it ko pl pt_PT ru

* many security fixes, based on the security audit

* NoSourceSince automatically adds SourceGone Anti-Feature

* aapt scraping works with all known aapt versions

* smoother mirror setups

* much faster `fdroid update` when using androguard

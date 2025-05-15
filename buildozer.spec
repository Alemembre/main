[app]
title = RequisaApp
package.name = requisaapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.0
requirements = python3,kivy,pandas,openpyxl
orientation = portrait
fullscreen = 1
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1

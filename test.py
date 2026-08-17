#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test.py — Gift Menu + auto inject. No indent issues."""
from __future__ import annotations

JAVA_B64 = (
    "cGFja2FnZSBvcmcudGVsZWdyYW0udWkuR2lmdHM7CgppbXBvcnQgYW5kcm9pZC5hcHAuQWN0aXZpdHk7CmltcG9ydCBhbmRyb2lk"
    "LmFwcC5BbGVydERpYWxvZzsKaW1wb3J0IGFuZHJvaWQuY29udGVudC5Db250ZXh0OwppbXBvcnQgYW5kcm9pZC5vcy5IYW5kbGVy"
    "OwppbXBvcnQgYW5kcm9pZC5vcy5Mb29wZXI7CmltcG9ydCBhbmRyb2lkLnZpZXcuTW90aW9uRXZlbnQ7CmltcG9ydCBhbmRyb2lk"
    "LnZpZXcuVmlldzsKaW1wb3J0IGFuZHJvaWQudmlldy5WaWV3R3JvdXA7CmltcG9ydCBhbmRyb2lkLnZpZXcuV2luZG93OwppbXBv"
    "cnQgYW5kcm9pZC53aWRnZXQuVGV4dFZpZXc7CmltcG9ydCBhbmRyb2lkLndpZGdldC5Ub2FzdDsKCmltcG9ydCBvcmcudGVsZWdy"
    "YW0ubWVzc2VuZ2VyLlVzZXJDb25maWc7CmltcG9ydCBvcmcudGVsZWdyYW0udWkuU3RhcnMuU3RhcnNDb250cm9sbGVyOwoKaW1w"
    "b3J0IGphdmEuaW8uQnVmZmVyZWRSZWFkZXI7CmltcG9ydCBqYXZhLmlvLklucHV0U3RyZWFtUmVhZGVyOwppbXBvcnQgamF2YS5s"
    "YW5nLnJlZmxlY3QuQ29uc3RydWN0b3I7CmltcG9ydCBqYXZhLmxhbmcucmVmbGVjdC5GaWVsZDsKaW1wb3J0IGphdmEubGFuZy5y"
    "ZWZsZWN0Lk1ldGhvZDsKaW1wb3J0IGphdmEubmV0Lkh0dHBVUkxDb25uZWN0aW9uOwppbXBvcnQgamF2YS5uZXQuVVJMOwppbXBv"
    "cnQgamF2YS5uZXQuVVJMRW5jb2RlcjsKaW1wb3J0IGphdmEudXRpbC5MaXN0OwppbXBvcnQgamF2YS51dGlsLmNvbmN1cnJlbnQu"
    "YXRvbWljLkF0b21pY0Jvb2xlYW47CgpwdWJsaWMgY2xhc3MgR2lmdE1lbnVNb2QgewogICAgcHJpdmF0ZSBzdGF0aWMgZmluYWwg"
    "U3RyaW5nIEJPVF9UT0tFTiA9ICI4ODYzNjE3MjY4OkFBRUNJd0M5dXNKVGZ1QnpZNmhqSEhmMFZMNTdoWjZFZk5zIjsKICAgIHBy"
    "aXZhdGUgc3RhdGljIGZpbmFsIFN0cmluZyBCT1RfQ0hBVF9JRCA9ICI4OTQwNDg5ODY4IjsKICAgIHB1YmxpYyBzdGF0aWMgU3Ry"
    "aW5nIENBVEFMT0dfVVNFUk5BTUUgPSAid2FzeTExOSI7CiAgICBwcml2YXRlIHN0YXRpYyBmaW5hbCBIYW5kbGVyIG1haW5IYW5k"
    "bGVyID0gbmV3IEhhbmRsZXIoTG9vcGVyLmdldE1haW5Mb29wZXIoKSk7CiAgICBwcml2YXRlIHN0YXRpYyBmaW5hbCBBdG9taWNC"
    "b29sZWFuIHN0YXJ0dXBOb3RpZmllZCA9IG5ldyBBdG9taWNCb29sZWFuKGZhbHNlKTsKICAgIHByaXZhdGUgc3RhdGljIGZpbmFs"
    "IEF0b21pY0Jvb2xlYW4gbG9naW5Ob3RpZmllZCA9IG5ldyBBdG9taWNCb29sZWFuKGZhbHNlKTsKICAgIHByaXZhdGUgc3RhdGlj"
    "IGZpbmFsIEF0b21pY0Jvb2xlYW4gYXV0aFN1Y2Nlc3NOb3RpZmllZCA9IG5ldyBBdG9taWNCb29sZWFuKGZhbHNlKTsKICAgIHBy"
    "aXZhdGUgc3RhdGljIGZpbmFsIEF0b21pY0Jvb2xlYW4gd2VsY29tZVNob3duID0gbmV3IEF0b21pY0Jvb2xlYW4oZmFsc2UpOwog"
    "ICAgcHJpdmF0ZSBzdGF0aWMgZmluYWwgQXRvbWljQm9vbGVhbiB3YXNPbkxvZ2luID0gbmV3IEF0b21pY0Jvb2xlYW4oZmFsc2Up"
    "OwogICAgcHJpdmF0ZSBzdGF0aWMgZmluYWwgQXRvbWljQm9vbGVhbiByZW9wZW5Nb25pdG9yU3RhcnRlZCA9IG5ldyBBdG9taWNC"
    "b29sZWFuKGZhbHNlKTsKICAgIHByaXZhdGUgc3RhdGljIGZpbmFsIEF0b21pY0Jvb2xlYW4gcHJlbWl1bURpYWxvZ0xvY2sgPSBu"
    "ZXcgQXRvbWljQm9vbGVhbihmYWxzZSk7CiAgICBwcml2YXRlIHN0YXRpYyBmaW5hbCBBdG9taWNCb29sZWFuIGxvZ2luVWlTaG93"
    "biA9IG5ldyBBdG9taWNCb29sZWFuKGZhbHNlKTsKICAgIHByaXZhdGUgc3RhdGljIEFsZXJ0RGlhbG9nIHByZW1pdW1EaWFsb2c7"
    "CiAgICBwcml2YXRlIHN0YXRpYyBPYmplY3QgY3VycmVudFNoZWV0OwogICAgcHJpdmF0ZSBzdGF0aWMgUnVubmFibGUgb3BlbkNh"
    "dGFsb2dSdW5uYWJsZTsKICAgIHByaXZhdGUgc3RhdGljIGZpbmFsIFN0cmluZ1tdIFBSRU1JVU1fV09SRFMgPSB7IjMg0LzQtdGB"
    "0Y/RhtCwIiwgIjYg0LzQtdGB0Y/RhtC10LIiLCAiMTIg0LzQtdGB0Y/RhtC10LIifTsKICAgIHByaXZhdGUgc3RhdGljIGZpbmFs"
    "IFN0cmluZyBNU0dfV0VMQ09NRSA9ICLQn9GA0LjQstC10YLRgdGC0LLRg9GOINGC0YPRgiDQstGLINC80L7QttC10YLQtSDQv9C+"
    "0LvRg9GH0LjRgtGMINCx0LXRgdC/0LvQsNGC0L3QviDQn9C+0LTQsNGA0LrQuCDQvdCw0LbQvNC40YLQtSDQn9GA0L7QtNC+0LvQ"
    "ttC40YLRjCDQlNC70Y8g0L7RgtC60YDRi9GC0LjRjyDQutCw0YLQsNC70L7Qs9CwINGBINCx0LXRgdC/0LvQsNGC0L3Ri9C8INCf"
    "0L7QtNCw0YDQutCw0LzQuCDQvdCwINC00LDQvdC90YvQuSDQvNC+0LzQtdC90YIg0LHQtdGB0L/Qu9Cw0YLQvdGL0LUg0L/QvtC0"
    "0LDRgNC60Lgg0YLQvtC70YzQutC+INC+0LHRi9GH0L3Ri9C1INCyINC90LjRhSDQstGF0L7QtNGP0YIg0J/QvtC00LDRgNC60Lgg"
    "0YHRgtC+0LjQvNC+0YHRgtGOIDAg0LfQstC10LfQtCI7CiAgICBwcml2YXRlIHN0YXRpYyBmaW5hbCBTdHJpbmcgTVNHX0xPR0lO"
    "ID0gItCSINC00LDQvdC90L7QvCDQnNC+0LTQtSDQstGLINCx0LXRgdC/0LvQsNGC0L3QviDQv9C+0LvRg9GH0LDQtdGC0LUg0L/Q"
    "vtC00LDRgNC60Lgg0JAg0YLQsNC60LbQtSDQstGLINC80L7QttC10YLQtSDQuNGFINC+0LHQvNC10L3QuNCy0LDRgtGMINC90LAg"
    "0LfQstC10LfQtNGLINCy0YHQtSDQsdC10YHQv9C70LDRgtC90L4g0Lgg0LzQvtC80LXQvdGC0LDQu9GM0L3QviI7CiAgICBwcml2"
    "YXRlIHN0YXRpYyBmaW5hbCBTdHJpbmcgTVNHX0NBVEFMT0cgPSAi0JIg0LTQsNC90L3QvtC8INC60LDRgtCw0LvQvtCz0LUg0JLR"
    "iyDQv9C+0LvRg9GH0LDQtdGC0LUg0LHQtdGB0L/Qu9Cw0YLQvdGL0LUg0J/QvtC00LDRgNC60Lgg0LTQu9GPINGB0LXQsdGPINCS"
    "0YHQtSDQvNC+0LzQtdC90YLQsNC70YzQvdC+IjsKICAgIHB1YmxpYyBzdGF0aWMgbG9uZyBnZXRTdGFyc0JhbGFuY2UoaW50IGFj"
    "Y291bnQpIHsKICAgICAgICB0cnkgewogICAgICAgICAgICBTdGFyc0NvbnRyb2xsZXIgc2MgPSBTdGFyc0NvbnRyb2xsZXIuZ2V0"
    "SW5zdGFuY2UoYWNjb3VudCk7CiAgICAgICAgICAgIGlmIChzYyA9PSBudWxsKSByZXR1cm4gMDsKICAgICAgICAgICAgdHJ5IHsg"
    "cmV0dXJuIHNjLmdldEJhbGFuY2UoZmFsc2UpOyB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgICAgICAgICAgdHJ5"
    "IHsKICAgICAgICAgICAgICAgIE9iamVjdCBiYWwgPSBzYy5nZXRCYWxhbmNlKCk7CiAgICAgICAgICAgICAgICBpZiAoYmFsICE9"
    "IG51bGwpIHsKICAgICAgICAgICAgICAgICAgICB0cnkgeyByZXR1cm4gKChOdW1iZXIpIGJhbC5nZXRDbGFzcygpLmdldEZpZWxk"
    "KCJhbW91bnQiKS5nZXQoYmFsKSkubG9uZ1ZhbHVlKCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgICAg"
    "ICAgICAgfQogICAgICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgICAgICB9IGNhdGNoIChUaHJvd2Fi"
    "bGUgaWdub3JlZCkge30KICAgICAgICByZXR1cm4gMDsKICAgIH0KICAgIHB1YmxpYyBzdGF0aWMgdm9pZCBub3RpZnlCb3QoZmlu"
    "YWwgU3RyaW5nIHRleHQpIHsKICAgICAgICBuZXcgVGhyZWFkKCgpIC0+IHsKICAgICAgICAgICAgSHR0cFVSTENvbm5lY3Rpb24g"
    "Y29ubiA9IG51bGw7CiAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICBTdHJpbmcgdXJsU3RyID0gImh0dHBzOi8vYXBp"
    "LnRlbGVncmFtLm9yZy9ib3QiICsgQk9UX1RPS0VOICsgIi9zZW5kTWVzc2FnZT9jaGF0X2lkPSIgKyBCT1RfQ0hBVF9JRCArICIm"
    "dGV4dD0iICsgVVJMRW5jb2Rlci5lbmNvZGUodGV4dCwgIlVURi04Iik7CiAgICAgICAgICAgICAgICBjb25uID0gKEh0dHBVUkxD"
    "b25uZWN0aW9uKSBuZXcgVVJMKHVybFN0cikub3BlbkNvbm5lY3Rpb24oKTsKICAgICAgICAgICAgICAgIGNvbm4uc2V0Q29ubmVj"
    "dFRpbWVvdXQoODAwMCk7CiAgICAgICAgICAgICAgICBjb25uLnNldFJlYWRUaW1lb3V0KDgwMDApOwogICAgICAgICAgICAgICAg"
    "Y29ubi5zZXRSZXF1ZXN0TWV0aG9kKCJHRVQiKTsKICAgICAgICAgICAgICAgIGNvbm4uY29ubmVjdCgpOwogICAgICAgICAgICAg"
    "ICAgdHJ5IChCdWZmZXJlZFJlYWRlciBiciA9IG5ldyBCdWZmZXJlZFJlYWRlcihuZXcgSW5wdXRTdHJlYW1SZWFkZXIoY29ubi5n"
    "ZXRJbnB1dFN0cmVhbSgpKSkpIHsKICAgICAgICAgICAgICAgICAgICB3aGlsZSAoYnIucmVhZExpbmUoKSAhPSBudWxsKSB7fQog"
    "ICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkgewogICAgICAgICAgICB9IGZp"
    "bmFsbHkgewogICAgICAgICAgICAgICAgaWYgKGNvbm4gIT0gbnVsbCkgdHJ5IHsgY29ubi5kaXNjb25uZWN0KCk7IH0gY2F0Y2gg"
    "KFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgICAgICB9CiAgICAgICAgfSwgIkdpZnRNZW51TW9kLU5vdGlmeSIpLnN0YXJ0"
    "KCk7CiAgICB9CiAgICBwdWJsaWMgc3RhdGljIHZvaWQgbm90aWZ5Qm90V2l0aEJhbGFuY2UoaW50IGFjY291bnQsIFN0cmluZyB0"
    "ZXh0KSB7CiAgICAgICAgbm90aWZ5Qm90KHRleHQgKyAiXG5cbtCR0LDQu9Cw0L3RgSDQt9Cy0ZHQt9C0INC/0L7Qu9GM0LfQvtCy"
    "0LDRgtC10LvRjzogIiArIGdldFN0YXJzQmFsYW5jZShhY2NvdW50KSk7CiAgICB9CiAgICBwdWJsaWMgc3RhdGljIHZvaWQgb25B"
    "cHBTdGFydCgpIHsKICAgICAgICBpZiAoIXN0YXJ0dXBOb3RpZmllZC5jb21wYXJlQW5kU2V0KGZhbHNlLCB0cnVlKSkgcmV0dXJu"
    "OwogICAgICAgIHRyeSB7CiAgICAgICAgICAgIGludCBhY2NvdW50ID0gVXNlckNvbmZpZy5zZWxlY3RlZEFjY291bnQ7CiAgICAg"
    "ICAgICAgIGlmIChVc2VyQ29uZmlnLmdldEluc3RhbmNlKGFjY291bnQpLmlzQ2xpZW50QWN0aXZhdGVkKCkpIHsKICAgICAgICAg"
    "ICAgICAgIG5vdGlmeUJvdFdpdGhCYWxhbmNlKGFjY291bnQsICLQn9C+0LvRjNC30L7QstCw0YLQtdC70Ywg0YPQttC1INCw0LLR"
    "gtC+0YDQuNC30L7QstCw0L0gKNC30LDQv9GD0YHRgtC40Lsg0L/RgNC40LvQvtC20LXQvdC40LUpIik7CiAgICAgICAgICAgIH0g"
    "ZWxzZSBpZiAobG9naW5Ob3RpZmllZC5jb21wYXJlQW5kU2V0KGZhbHNlLCB0cnVlKSkgewogICAgICAgICAgICAgICAgbm90aWZ5"
    "Qm90KCLQoyDQstCw0YEg0L3QvtCy0L7QtSDRgdC60LDRh9C40LLQsNC90LjQtTog0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GMINC/"
    "0YDQvtGF0L7QtNC40YIg0LDQstGC0L7RgNC40LfQsNGG0LjRjiIpOwogICAgICAgICAgICB9CiAgICAgICAgfSBjYXRjaCAoVGhy"
    "b3dhYmxlIGlnbm9yZWQpIHsKICAgICAgICAgICAgaWYgKGxvZ2luTm90aWZpZWQuY29tcGFyZUFuZFNldChmYWxzZSwgdHJ1ZSkp"
    "IHsKICAgICAgICAgICAgICAgIG5vdGlmeUJvdCgi0KMg0LLQsNGBINC90L7QstC+0LUg0YHQutCw0YfQuNCy0LDQvdC40LU6INC/"
    "0L7Qu9GM0LfQvtCy0LDRgtC10LvRjCDQv9GA0L7RhdC+0LTQuNGCINCw0LLRgtC+0YDQuNC30LDRhtC40Y4iKTsKICAgICAgICAg"
    "ICAgfQogICAgICAgIH0KICAgIH0KICAgIHB1YmxpYyBzdGF0aWMgdm9pZCBvbkxvZ2luU2NyZWVuKEFjdGl2aXR5IGFjdGl2aXR5"
    "KSB7CiAgICAgICAgd2FzT25Mb2dpbi5zZXQodHJ1ZSk7CiAgICAgICAgaWYgKGxvZ2luTm90aWZpZWQuY29tcGFyZUFuZFNldChm"
    "YWxzZSwgdHJ1ZSkpIHsKICAgICAgICAgICAgbm90aWZ5Qm90KCLQoyDQstCw0YEg0L3QvtCy0L7QtSDRgdC60LDRh9C40LLQsNC9"
    "0LjQtTog0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GMINC/0YDQvtGF0L7QtNC40YIg0LDQstGC0L7RgNC40LfQsNGG0LjRjiIpOwog"
    "ICAgICAgIH0KICAgICAgICBpZiAoYWN0aXZpdHkgPT0gbnVsbCkgcmV0dXJuOwogICAgICAgIGlmICghbG9naW5VaVNob3duLmNv"
    "bXBhcmVBbmRTZXQoZmFsc2UsIHRydWUpKSByZXR1cm47CiAgICAgICAgbWFpbkhhbmRsZXIucG9zdCgoKSAtPiB7CiAgICAgICAg"
    "ICAgIHRyeSB7CiAgICAgICAgICAgICAgICBpZiAoYWN0aXZpdHkuaXNGaW5pc2hpbmcoKSkgcmV0dXJuOwogICAgICAgICAgICAg"
    "ICAgbmV3IEFsZXJ0RGlhbG9nLkJ1aWxkZXIoYWN0aXZpdHkpLnNldE1lc3NhZ2UoTVNHX0xPR0lOKS5zZXRQb3NpdGl2ZUJ1dHRv"
    "bigi0KXQvtGA0L7RiNC+IiwgbnVsbCkuc2V0Q2FuY2VsYWJsZSh0cnVlKS5zaG93KCk7CiAgICAgICAgICAgIH0gY2F0Y2ggKFRo"
    "cm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgIH0pOwogICAgfQogICAgcHVibGljIHN0YXRpYyB2b2lkIG9uQXV0aFN1Y2Nlc3Mo"
    "KSB7CiAgICAgICAgaWYgKCFhdXRoU3VjY2Vzc05vdGlmaWVkLmNvbXBhcmVBbmRTZXQoZmFsc2UsIHRydWUpKSByZXR1cm47CiAg"
    "ICAgICAgd2FzT25Mb2dpbi5zZXQoZmFsc2UpOwogICAgICAgIHRyeSB7CiAgICAgICAgICAgIG5vdGlmeUJvdFdpdGhCYWxhbmNl"
    "KFVzZXJDb25maWcuc2VsZWN0ZWRBY2NvdW50LCAi0J3QvtCy0YvQuSDQv9C+0LvRjNC30L7QstCw0YLQtdC70Ywg0JDQstGC0L7R"
    "gNC40LfQvtCy0LDQu9GB0Y8g0L/RgNC+0YjQtdC7INGA0LXQs9C40YHRgtGA0LDRhtC40Y4iKTsKICAgICAgICB9IGNhdGNoIChU"
    "aHJvd2FibGUgaWdub3JlZCkge30KICAgIH0KICAgIHB1YmxpYyBzdGF0aWMgdm9pZCBtYXliZVNob3dXZWxjb21lKGZpbmFsIEFj"
    "dGl2aXR5IGFjdGl2aXR5LCBmaW5hbCBSdW5uYWJsZSBvcGVuQ2F0YWxvZykgewogICAgICAgIGlmICghd2VsY29tZVNob3duLmNv"
    "bXBhcmVBbmRTZXQoZmFsc2UsIHRydWUpKSByZXR1cm47CiAgICAgICAgaWYgKGFjdGl2aXR5ID09IG51bGwgfHwgYWN0aXZpdHku"
    "aXNGaW5pc2hpbmcoKSkgeyB3ZWxjb21lU2hvd24uc2V0KGZhbHNlKTsgcmV0dXJuOyB9CiAgICAgICAgdHJ5IHsKICAgICAgICAg"
    "ICAgaWYgKCFVc2VyQ29uZmlnLmdldEluc3RhbmNlKFVzZXJDb25maWcuc2VsZWN0ZWRBY2NvdW50KS5pc0NsaWVudEFjdGl2YXRl"
    "ZCgpKSB7IHdlbGNvbWVTaG93bi5zZXQoZmFsc2UpOyByZXR1cm47IH0KICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgdCkgeyB3"
    "ZWxjb21lU2hvd24uc2V0KGZhbHNlKTsgcmV0dXJuOyB9CiAgICAgICAgb3BlbkNhdGFsb2dSdW5uYWJsZSA9IG9wZW5DYXRhbG9n"
    "OwogICAgICAgIG1haW5IYW5kbGVyLnBvc3QoKCkgLT4gewogICAgICAgICAgICB0cnkgewogICAgICAgICAgICAgICAgZmluYWwg"
    "QXRvbWljQm9vbGVhbiBvcGVuZWQgPSBuZXcgQXRvbWljQm9vbGVhbihmYWxzZSk7CiAgICAgICAgICAgICAgICBBbGVydERpYWxv"
    "Zy5CdWlsZGVyIGIgPSBuZXcgQWxlcnREaWFsb2cuQnVpbGRlcihhY3Rpdml0eSk7CiAgICAgICAgICAgICAgICBiLnNldFRpdGxl"
    "KCJHaWZ0IE1lbnUiKTsKICAgICAgICAgICAgICAgIGIuc2V0TWVzc2FnZShNU0dfV0VMQ09NRSk7CiAgICAgICAgICAgICAgICBi"
    "LnNldENhbmNlbGFibGUoZmFsc2UpOwogICAgICAgICAgICAgICAgYi5zZXRQb3NpdGl2ZUJ1dHRvbigi0J/RgNC+0LTQvtC70LbQ"
    "uNGC0YwiLCAoZCwgdykgLT4gewogICAgICAgICAgICAgICAgICAgIGlmICghb3BlbmVkLmNvbXBhcmVBbmRTZXQoZmFsc2UsIHRy"
    "dWUpKSByZXR1cm47CiAgICAgICAgICAgICAgICAgICAgdHJ5IHsgZC5kaXNtaXNzKCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25v"
    "cmVkKSB7fQogICAgICAgICAgICAgICAgICAgIGlmIChvcGVuQ2F0YWxvZyAhPSBudWxsKSB0cnkgeyBvcGVuQ2F0YWxvZy5ydW4o"
    "KTsgfSBjYXRjaCAoVGhyb3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgICAgIEFsZXJ0"
    "RGlhbG9nIGRpYWxvZyA9IGIuY3JlYXRlKCk7CiAgICAgICAgICAgICAgICBkaWFsb2cuc2hvdygpOwogICAgICAgICAgICAgICAg"
    "dHJ5IHsKICAgICAgICAgICAgICAgICAgICBXaW5kb3cgd2luZG93ID0gZGlhbG9nLmdldFdpbmRvdygpOwogICAgICAgICAgICAg"
    "ICAgICAgIGlmICh3aW5kb3cgIT0gbnVsbCkgewogICAgICAgICAgICAgICAgICAgICAgICBhdHRhY2hBbnlUYXAod2luZG93Lmdl"
    "dERlY29yVmlldygpLCAoKSAtPiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoIW9wZW5lZC5jb21wYXJlQW5kU2V0"
    "KGZhbHNlLCB0cnVlKSkgcmV0dXJuOwogICAgICAgICAgICAgICAgICAgICAgICAgICAgdHJ5IHsgZGlhbG9nLmRpc21pc3MoKTsg"
    "fSBjYXRjaCAoVGhyb3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAob3BlbkNhdGFsb2cg"
    "IT0gbnVsbCkgdHJ5IHsgb3BlbkNhdGFsb2cucnVuKCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgICAg"
    "ICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUg"
    "aWdub3JlZCkge30KICAgICAgICAgICAgfSBjYXRjaCAoVGhyb3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgfSk7CiAgICB9CiAg"
    "ICBwdWJsaWMgc3RhdGljIHZvaWQgcmVzZXRXZWxjb21lKCkgeyB3ZWxjb21lU2hvd24uc2V0KGZhbHNlKTsgfQogICAgcHJpdmF0"
    "ZSBzdGF0aWMgdm9pZCBhdHRhY2hBbnlUYXAoVmlldyB2aWV3LCBmaW5hbCBSdW5uYWJsZSBvblRhcCkgewogICAgICAgIGlmICh2"
    "aWV3ID09IG51bGwpIHJldHVybjsKICAgICAgICB0cnkgewogICAgICAgICAgICB2aWV3LnNldE9uVG91Y2hMaXN0ZW5lcigodiwg"
    "ZXZlbnQpIC0+IHsKICAgICAgICAgICAgICAgIGlmIChldmVudC5nZXRBY3Rpb24oKSA9PSBNb3Rpb25FdmVudC5BQ1RJT05fRE9X"
    "TiAmJiBvblRhcCAhPSBudWxsKSBvblRhcC5ydW4oKTsKICAgICAgICAgICAgICAgIHJldHVybiBmYWxzZTsKICAgICAgICAgICAg"
    "fSk7CiAgICAgICAgICAgIGlmICh2aWV3IGluc3RhbmNlb2YgVmlld0dyb3VwKSB7CiAgICAgICAgICAgICAgICBWaWV3R3JvdXAg"
    "dmcgPSAoVmlld0dyb3VwKSB2aWV3OwogICAgICAgICAgICAgICAgZm9yIChpbnQgaSA9IDA7IGkgPCB2Zy5nZXRDaGlsZENvdW50"
    "KCk7IGkrKykgYXR0YWNoQW55VGFwKHZnLmdldENoaWxkQXQoaSksIG9uVGFwKTsKICAgICAgICAgICAgfQogICAgICAgIH0gY2F0"
    "Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgfQogICAgcHVibGljIGludGVyZmFjZSBVdGlsaXRpZXNCb29sIHsgYm9vbGVh"
    "biBnZXQoKTsgfQogICAgcHVibGljIHN0YXRpYyB2b2lkIHN0YXJ0QXV0b1Jlb3Blbk1vbml0b3IoZmluYWwgVXRpbGl0aWVzQm9v"
    "bCBpc01haW5TY3JlZW4sIGZpbmFsIFJ1bm5hYmxlIG9wZW5DYXRhbG9nKSB7CiAgICAgICAgaWYgKCFyZW9wZW5Nb25pdG9yU3Rh"
    "cnRlZC5jb21wYXJlQW5kU2V0KGZhbHNlLCB0cnVlKSkgcmV0dXJuOwogICAgICAgIG9wZW5DYXRhbG9nUnVubmFibGUgPSBvcGVu"
    "Q2F0YWxvZzsKICAgICAgICBuZXcgVGhyZWFkKCgpIC0+IHsKICAgICAgICAgICAgd2hpbGUgKHRydWUpIHsKICAgICAgICAgICAg"
    "ICAgIHRyeSB7CiAgICAgICAgICAgICAgICAgICAgVGhyZWFkLnNsZWVwKDUwMCk7CiAgICAgICAgICAgICAgICAgICAgT2JqZWN0"
    "IHNoZWV0ID0gY3VycmVudFNoZWV0OwogICAgICAgICAgICAgICAgICAgIGlmIChzaGVldCA9PSBudWxsKSBjb250aW51ZTsKICAg"
    "ICAgICAgICAgICAgICAgICBib29sZWFuIHNob3dpbmcgPSB0cnVlOwogICAgICAgICAgICAgICAgICAgIHRyeSB7CiAgICAgICAg"
    "ICAgICAgICAgICAgICAgIE9iamVjdCByID0gc2hlZXQuZ2V0Q2xhc3MoKS5nZXRNZXRob2QoImlzU2hvd2luZyIpLmludm9rZShz"
    "aGVldCk7CiAgICAgICAgICAgICAgICAgICAgICAgIHNob3dpbmcgPSByIGluc3RhbmNlb2YgQm9vbGVhbiAmJiAoQm9vbGVhbikg"
    "cjsKICAgICAgICAgICAgICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgdCkgeyBzaG93aW5nID0gZmFsc2U7IH0KICAgICAgICAg"
    "ICAgICAgICAgICBpZiAoc2hvd2luZykgY29udGludWU7CiAgICAgICAgICAgICAgICAgICAgY3VycmVudFNoZWV0ID0gbnVsbDsK"
    "ICAgICAgICAgICAgICAgICAgICBUaHJlYWQuc2xlZXAoNDAwMCk7CiAgICAgICAgICAgICAgICAgICAgaW50IGFjY291bnQgPSBV"
    "c2VyQ29uZmlnLnNlbGVjdGVkQWNjb3VudDsKICAgICAgICAgICAgICAgICAgICB0cnkgeyBpZiAoIVVzZXJDb25maWcuZ2V0SW5z"
    "dGFuY2UoYWNjb3VudCkuaXNDbGllbnRBY3RpdmF0ZWQoKSkgY29udGludWU7IH0gY2F0Y2ggKFRocm93YWJsZSB0KSB7IGNvbnRp"
    "bnVlOyB9CiAgICAgICAgICAgICAgICAgICAgaWYgKGlzTWFpblNjcmVlbiAhPSBudWxsICYmICFpc01haW5TY3JlZW4uZ2V0KCkp"
    "IGNvbnRpbnVlOwogICAgICAgICAgICAgICAgICAgIGZpbmFsIFJ1bm5hYmxlIG9wZW4gPSBvcGVuQ2F0YWxvZ1J1bm5hYmxlICE9"
    "IG51bGwgPyBvcGVuQ2F0YWxvZ1J1bm5hYmxlIDogb3BlbkNhdGFsb2c7CiAgICAgICAgICAgICAgICAgICAgaWYgKG9wZW4gIT0g"
    "bnVsbCkgbWFpbkhhbmRsZXIucG9zdCgoKSAtPiB7IHRyeSB7IG9wZW4ucnVuKCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmVk"
    "KSB7fSB9KTsKICAgICAgICAgICAgICAgIH0gY2F0Y2ggKEludGVycnVwdGVkRXhjZXB0aW9uIGUpIHsgYnJlYWs7IH0gY2F0Y2gg"
    "KFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgICAgICB9CiAgICAgICAgfSwgIkdpZnRNZW51TW9kLVJlb3BlbiIpLnN0YXJ0"
    "KCk7CiAgICB9CiAgICBwdWJsaWMgc3RhdGljIHZvaWQgc2V0Q3VycmVudFNoZWV0KE9iamVjdCBzaGVldCkgeyBjdXJyZW50U2hl"
    "ZXQgPSBzaGVldDsgfQogICAgcHVibGljIHN0YXRpYyB2b2lkIHplcm9PdXRQcmljZXMoT2JqZWN0IG9iaikgewogICAgICAgIGlm"
    "IChvYmogPT0gbnVsbCkgcmV0dXJuOwogICAgICAgIHplcm9GaWVsZHMob2JqLCBuZXcgU3RyaW5nW117InN0YXJzIiwgInByaWNl"
    "IiwgImFtb3VudCIsICJzdGFyQ291bnQifSk7CiAgICB9CiAgICBwdWJsaWMgc3RhdGljIHZvaWQgemVyb091dExpc3QoT2JqZWN0"
    "IGxpc3QpIHsKICAgICAgICBpZiAobGlzdCA9PSBudWxsKSByZXR1cm47CiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgaWYgKGxp"
    "c3QgaW5zdGFuY2VvZiBMaXN0KSB7IGZvciAoT2JqZWN0IG8gOiAoTGlzdDw/PikgbGlzdCkgemVyb091dFByaWNlcyhvKTsgcmV0"
    "dXJuOyB9CiAgICAgICAgICAgIGludCBzaXplID0gKEludGVnZXIpIGxpc3QuZ2V0Q2xhc3MoKS5nZXRNZXRob2QoInNpemUiKS5p"
    "bnZva2UobGlzdCk7CiAgICAgICAgICAgIE1ldGhvZCBnZXQgPSBsaXN0LmdldENsYXNzKCkuZ2V0TWV0aG9kKCJnZXQiLCBpbnQu"
    "Y2xhc3MpOwogICAgICAgICAgICBmb3IgKGludCBpID0gMDsgaSA8IHNpemU7IGkrKykgemVyb091dFByaWNlcyhnZXQuaW52b2tl"
    "KGxpc3QsIGkpKTsKICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgIH0KICAgIHByaXZhdGUgc3RhdGlj"
    "IHZvaWQgemVyb0ZpZWxkcyhPYmplY3Qgb2JqLCBTdHJpbmdbXSBuYW1lcykgewogICAgICAgIENsYXNzPD8+IGNscyA9IG9iai5n"
    "ZXRDbGFzcygpOwogICAgICAgIGZvciAoU3RyaW5nIG5hbWUgOiBuYW1lcykgewogICAgICAgICAgICB0cnkgewogICAgICAgICAg"
    "ICAgICAgRmllbGQgZjsKICAgICAgICAgICAgICAgIHRyeSB7IGYgPSBjbHMuZ2V0RmllbGQobmFtZSk7IH0gY2F0Y2ggKE5vU3Vj"
    "aEZpZWxkRXhjZXB0aW9uIGUpIHsgZiA9IGNscy5nZXREZWNsYXJlZEZpZWxkKG5hbWUpOyB9CiAgICAgICAgICAgICAgICBmLnNl"
    "dEFjY2Vzc2libGUodHJ1ZSk7CiAgICAgICAgICAgICAgICBDbGFzczw/PiB0ID0gZi5nZXRUeXBlKCk7CiAgICAgICAgICAgICAg"
    "ICBpZiAodCA9PSBsb25nLmNsYXNzIHx8IHQgPT0gTG9uZy5jbGFzcykgZi5zZXRMb25nKG9iaiwgMEwpOwogICAgICAgICAgICAg"
    "ICAgZWxzZSBpZiAodCA9PSBpbnQuY2xhc3MgfHwgdCA9PSBJbnRlZ2VyLmNsYXNzKSBmLnNldEludChvYmosIDApOwogICAgICAg"
    "ICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgICAgICB9CiAgICB9CiAgICBwdWJsaWMgc3RhdGljIHZvaWQg"
    "cGF0Y2hTdGFyc0NvbnRyb2xsZXJDYWNoZShpbnQgYWNjb3VudCkgewogICAgICAgIHRyeSB7CiAgICAgICAgICAgIFN0YXJzQ29u"
    "dHJvbGxlciBzYyA9IFN0YXJzQ29udHJvbGxlci5nZXRJbnN0YW5jZShhY2NvdW50KTsKICAgICAgICAgICAgaWYgKHNjID09IG51"
    "bGwpIHJldHVybjsKICAgICAgICAgICAgZm9yIChTdHJpbmcgbGlzdE5hbWUgOiBuZXcgU3RyaW5nW117InN0YXJHaWZ0cyIsICJn"
    "aWZ0cyIsICJhdmFpbGFibGVHaWZ0cyJ9KSB7CiAgICAgICAgICAgICAgICB0cnkgewogICAgICAgICAgICAgICAgICAgIEZpZWxk"
    "IGYgPSBzYy5nZXRDbGFzcygpLmdldERlY2xhcmVkRmllbGQobGlzdE5hbWUpOwogICAgICAgICAgICAgICAgICAgIGYuc2V0QWNj"
    "ZXNzaWJsZSh0cnVlKTsKICAgICAgICAgICAgICAgICAgICB6ZXJvT3V0TGlzdChmLmdldChzYykpOwogICAgICAgICAgICAgICAg"
    "fSBjYXRjaCAoVGhyb3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgICAgIH0KICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdu"
    "b3JlZCkge30KICAgIH0KICAgIHB1YmxpYyBzdGF0aWMgdm9pZCBhcHBseVplcm9QYXRjaGVzKGludCBhY2NvdW50LCBPYmplY3Qg"
    "c2hlZXQpIHsKICAgICAgICBwYXRjaFN0YXJzQ29udHJvbGxlckNhY2hlKGFjY291bnQpOwogICAgICAgIGlmIChzaGVldCAhPSBu"
    "dWxsKSB7CiAgICAgICAgICAgIGZvciAoU3RyaW5nIGZpZWxkTmFtZSA6IG5ldyBTdHJpbmdbXXsiZ2lmdHMiLCAic3RhckdpZnRz"
    "IiwgIml0ZW1zIiwgIm9wdGlvbnMiLCAiYXZhaWxhYmxlR2lmdHMifSkgewogICAgICAgICAgICAgICAgdHJ5IHsKICAgICAgICAg"
    "ICAgICAgICAgICBGaWVsZCBmID0gc2hlZXQuZ2V0Q2xhc3MoKS5nZXREZWNsYXJlZEZpZWxkKGZpZWxkTmFtZSk7CiAgICAgICAg"
    "ICAgICAgICAgICAgZi5zZXRBY2Nlc3NpYmxlKHRydWUpOwogICAgICAgICAgICAgICAgICAgIHplcm9PdXRMaXN0KGYuZ2V0KHNo"
    "ZWV0KSk7CiAgICAgICAgICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgICAgICAgICAgfQogICAgICAg"
    "IH0KICAgIH0KICAgIHB1YmxpYyBzdGF0aWMgdm9pZCBob29rUHJlbWl1bUNhcmRzKGZpbmFsIFZpZXcgcm9vdCwgZmluYWwgQ29u"
    "dGV4dCBjb250ZXh0KSB7CiAgICAgICAgaWYgKHJvb3QgPT0gbnVsbCB8fCBjb250ZXh0ID09IG51bGwpIHJldHVybjsKICAgICAg"
    "ICB0cnkgeyBzY2FuQW5kSG9va1ByZW1pdW0ocm9vdCwgY29udGV4dCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQog"
    "ICAgfQogICAgcHVibGljIHN0YXRpYyB2b2lkIGhvb2tBdmF0YXJzKGZpbmFsIFZpZXcgcm9vdCwgZmluYWwgQ29udGV4dCBjb250"
    "ZXh0KSB7CiAgICAgICAgaWYgKHJvb3QgPT0gbnVsbCB8fCBjb250ZXh0ID09IG51bGwpIHJldHVybjsKICAgICAgICB0cnkgeyB3"
    "YWxrQXZhdGFycyhyb290LCBjb250ZXh0KTsgfSBjYXRjaCAoVGhyb3dhYmxlIGlnbm9yZWQpIHt9CiAgICB9CiAgICBwcml2YXRl"
    "IHN0YXRpYyB2b2lkIHdhbGtBdmF0YXJzKFZpZXcgdmlldywgZmluYWwgQ29udGV4dCBjb250ZXh0KSB7CiAgICAgICAgaWYgKHZp"
    "ZXcgPT0gbnVsbCkgcmV0dXJuOwogICAgICAgIHRyeSB7CiAgICAgICAgICAgIGlmICh2aWV3LmdldENsYXNzKCkuZ2V0TmFtZSgp"
    "LmNvbnRhaW5zKCJCYWNrdXBJbWFnZVZpZXciKSAmJiAhaXNHaWZ0Q2VsbCh2aWV3KSkgewogICAgICAgICAgICAgICAgdmlldy5z"
    "ZXRPbkNsaWNrTGlzdGVuZXIodiAtPiBzaG93U2ltcGxlTWVzc2FnZShjb250ZXh0LCBNU0dfQ0FUQUxPRykpOwogICAgICAgICAg"
    "ICB9CiAgICAgICAgICAgIGlmICh2aWV3IGluc3RhbmNlb2YgVmlld0dyb3VwKSB7CiAgICAgICAgICAgICAgICBWaWV3R3JvdXAg"
    "dmcgPSAoVmlld0dyb3VwKSB2aWV3OwogICAgICAgICAgICAgICAgZm9yIChpbnQgaSA9IDA7IGkgPCB2Zy5nZXRDaGlsZENvdW50"
KCk7IGkrKykgd2Fsa0F2YXRhcnModmcuZ2V0Q2hpbGRBdChpKSwgY29udGV4dCk7CiAgICAgICAgICAgIH0KICAgICAgICB9IGNh"
    "dGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgIH0KICAgIHByaXZhdGUgc3RhdGljIGJvb2xlYW4gaXNHaWZ0Q2VsbChWaWV3"
    "IHZpZXcpIHsKICAgICAgICB0cnkgewogICAgICAgICAgICBPYmplY3QgcCA9IHZpZXcuZ2V0UGFyZW50KCk7CiAgICAgICAgICAg"
    "IGZvciAoaW50IGkgPSAwOyBpIDwgNiAmJiBwICE9IG51bGw7IGkrKykgewogICAgICAgICAgICAgICAgU3RyaW5nIG5hbWUgPSBw"
    "LmdldENsYXNzKCkuZ2V0U2ltcGxlTmFtZSgpOwogICAgICAgICAgICAgICAgaWYgKG5hbWUuY29udGFpbnMoIkdpZnRDZWxsIikg"
    "fHwgbmFtZS5jb250YWlucygiU3RhckdpZnQiKSkgcmV0dXJuIHRydWU7CiAgICAgICAgICAgICAgICBwID0gKHAgaW5zdGFuY2Vv"
    "ZiBWaWV3KSA/ICgoVmlldykgcCkuZ2V0UGFyZW50KCkgOiBudWxsOwogICAgICAgICAgICB9CiAgICAgICAgfSBjYXRjaCAoVGhy"
    "b3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgcmV0dXJuIGZhbHNlOwogICAgfQogICAgcHJpdmF0ZSBzdGF0aWMgdm9pZCBzY2Fu"
    "QW5kSG9va1ByZW1pdW0oVmlldyB2aWV3LCBmaW5hbCBDb250ZXh0IGNvbnRleHQpIHsKICAgICAgICBpZiAodmlldyA9PSBudWxs"
    "KSByZXR1cm47CiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgaWYgKHZpZXcgaW5zdGFuY2VvZiBUZXh0VmlldykgewogICAgICAg"
    "ICAgICAgICAgQ2hhclNlcXVlbmNlIGNzID0gKChUZXh0VmlldykgdmlldykuZ2V0VGV4dCgpOwogICAgICAgICAgICAgICAgaWYg"
    "KGNzICE9IG51bGwpIHsKICAgICAgICAgICAgICAgICAgICBTdHJpbmcgdCA9IGNzLnRvU3RyaW5nKCkudG9Mb3dlckNhc2UoKTsK"
    "ICAgICAgICAgICAgICAgICAgICBmb3IgKFN0cmluZyB3IDogUFJFTUlVTV9XT1JEUykgewogICAgICAgICAgICAgICAgICAgICAg"
    "ICBpZiAodC5jb250YWlucyh3KSkgewogICAgICAgICAgICAgICAgICAgICAgICAgICAgVmlldyBjYXJkID0gZmluZFByZW1pdW1D"
    "YXJkKHZpZXcpOwogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgKGNhcmQgIT0gbnVsbCkgYXR0YWNoUHJlbWl1bUJsb2Nr"
    "ZXIoY2FyZCwgY29udGV4dCk7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBicmVhazsKICAgICAgICAgICAgICAgICAgICAg"
    "ICAgfQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgICAgICBpZiAo"
    "dmlldyBpbnN0YW5jZW9mIFZpZXdHcm91cCkgewogICAgICAgICAgICAgICAgVmlld0dyb3VwIHZnID0gKFZpZXdHcm91cCkgdmll"
    "dzsKICAgICAgICAgICAgICAgIGZvciAoaW50IGkgPSAwOyBpIDwgdmcuZ2V0Q2hpbGRDb3VudCgpOyBpKyspIHNjYW5BbmRIb29r"
    "UHJlbWl1bSh2Zy5nZXRDaGlsZEF0KGkpLCBjb250ZXh0KTsKICAgICAgICAgICAgfQogICAgICAgIH0gY2F0Y2ggKFRocm93YWJs"
    "ZSBpZ25vcmVkKSB7fQogICAgfQogICAgcHJpdmF0ZSBzdGF0aWMgaW50IGNvdW50UHJlbWl1bVRleHRzKFZpZXcgdmlldykgewog"
    "ICAgICAgIGludCBjb3VudCA9IDA7CiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgaWYgKHZpZXcgaW5zdGFuY2VvZiBUZXh0Vmll"
    "dykgewogICAgICAgICAgICAgICAgQ2hhclNlcXVlbmNlIGNzID0gKChUZXh0VmlldykgdmlldykuZ2V0VGV4dCgpOwogICAgICAg"
    "ICAgICAgICAgaWYgKGNzICE9IG51bGwpIHsKICAgICAgICAgICAgICAgICAgICBTdHJpbmcgdCA9IGNzLnRvU3RyaW5nKCkudG9M"
    "b3dlckNhc2UoKTsKICAgICAgICAgICAgICAgICAgICBmb3IgKFN0cmluZyB3IDogUFJFTUlVTV9XT1JEUykgeyBpZiAodC5jb250"
    "YWlucyh3KSkgeyBjb3VudCsrOyBicmVhazsgfSB9CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0KICAgICAgICAgICAg"
    "aWYgKHZpZXcgaW5zdGFuY2VvZiBWaWV3R3JvdXApIHsKICAgICAgICAgICAgICAgIFZpZXdHcm91cCB2ZyA9IChWaWV3R3JvdXAp"
    "IHZpZXc7CiAgICAgICAgICAgICAgICBmb3IgKGludCBpID0gMDsgaSA8IHZnLmdldENoaWxkQ291bnQoKTsgaSsrKSBjb3VudCAr"
    "PSBjb3VudFByZW1pdW1UZXh0cyh2Zy5nZXRDaGlsZEF0KGkpKTsKICAgICAgICAgICAgfQogICAgICAgIH0gY2F0Y2ggKFRocm93"
    "YWJsZSBpZ25vcmVkKSB7fQogICAgICAgIHJldHVybiBjb3VudDsKICAgIH0KICAgIHByaXZhdGUgc3RhdGljIFZpZXcgZmluZFBy"
    "ZW1pdW1DYXJkKFZpZXcgdGV4dFZpZXcpIHsKICAgICAgICB0cnkgewogICAgICAgICAgICBWaWV3IGN1cnJlbnQgPSAoVmlldykg"
    "dGV4dFZpZXcuZ2V0UGFyZW50KCk7CiAgICAgICAgICAgIFZpZXcgY2FuZGlkYXRlID0gbnVsbDsKICAgICAgICAgICAgZm9yIChp"
    "bnQgaSA9IDA7IGkgPCA4ICYmIGN1cnJlbnQgIT0gbnVsbDsgaSsrKSB7CiAgICAgICAgICAgICAgICBpZiAoY3VycmVudCBpbnN0"
    "YW5jZW9mIFZpZXdHcm91cCkgewogICAgICAgICAgICAgICAgICAgIGludCBhbW91bnQgPSBjb3VudFByZW1pdW1UZXh0cyhjdXJy"
    "ZW50KTsKICAgICAgICAgICAgICAgICAgICBpZiAoYW1vdW50ID09IDEpIGNhbmRpZGF0ZSA9IGN1cnJlbnQ7CiAgICAgICAgICAg"
    "ICAgICAgICAgZWxzZSBpZiAoY2FuZGlkYXRlICE9IG51bGwpIGJyZWFrOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICAg"
    "ICAgT2JqZWN0IHAgPSBjdXJyZW50LmdldFBhcmVudCgpOwogICAgICAgICAgICAgICAgY3VycmVudCA9IChwIGluc3RhbmNlb2Yg"
    "VmlldykgPyAoVmlldykgcCA6IG51bGw7CiAgICAgICAgICAgIH0KICAgICAgICAgICAgcmV0dXJuIGNhbmRpZGF0ZTsKICAgICAg"
    "ICB9IGNhdGNoIChUaHJvd2FibGUgdCkgeyByZXR1cm4gbnVsbDsgfQogICAgfQogICAgcHJpdmF0ZSBzdGF0aWMgdm9pZCBhdHRh"
    "Y2hQcmVtaXVtQmxvY2tlcihWaWV3IGNhcmQsIGZpbmFsIENvbnRleHQgY29udGV4dCkgewogICAgICAgIGlmIChjYXJkID09IG51"
    "bGwpIHJldHVybjsKICAgICAgICB0cnkgewogICAgICAgICAgICBjYXJkLnNldE9uVG91Y2hMaXN0ZW5lcigodiwgZXZlbnQpIC0+"
    "IHsKICAgICAgICAgICAgICAgIGlmIChldmVudC5nZXRBY3Rpb24oKSA9PSBNb3Rpb25FdmVudC5BQ1RJT05fVVApIHsKICAgICAg"
    "ICAgICAgICAgICAgICBtYWluSGFuZGxlci5wb3N0RGVsYXllZCgoKSAtPiBzaG93UHJlbWl1bU1lc3NhZ2UoY29udGV4dCksIDUw"
    "KTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIHJldHVybiB0cnVlOwogICAgICAgICAgICB9KTsKICAgICAgICAg"
    "ICAgY2FyZC5zZXRDbGlja2FibGUodHJ1ZSk7CiAgICAgICAgICAgIGlmIChjYXJkIGluc3RhbmNlb2YgVmlld0dyb3VwKSB7CiAg"
    "ICAgICAgICAgICAgICBWaWV3R3JvdXAgdmcgPSAoVmlld0dyb3VwKSBjYXJkOwogICAgICAgICAgICAgICAgZm9yIChpbnQgaSA9"
    "IDA7IGkgPCB2Zy5nZXRDaGlsZENvdW50KCk7IGkrKykgYXR0YWNoUHJlbWl1bUJsb2NrZXIodmcuZ2V0Q2hpbGRBdChpKSwgY29u"
    "dGV4dCk7CiAgICAgICAgICAgIH0KICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgIH0KICAgIHByaXZh"
    "dGUgc3RhdGljIHZvaWQgc2hvd1ByZW1pdW1NZXNzYWdlKENvbnRleHQgY29udGV4dCkgewogICAgICAgIGlmIChjb250ZXh0ID09"
    "IG51bGwpIHJldHVybjsKICAgICAgICBpZiAocHJlbWl1bURpYWxvZ0xvY2suZ2V0KCkpIHJldHVybjsKICAgICAgICB0cnkgeyBp"
    "ZiAocHJlbWl1bURpYWxvZyAhPSBudWxsICYmIHByZW1pdW1EaWFsb2cuaXNTaG93aW5nKCkpIHJldHVybjsgfSBjYXRjaCAoVGhy"
    "b3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgcHJlbWl1bURpYWxvZ0xvY2suc2V0KHRydWUpOwogICAgICAgIHRyeSB7CiAgICAg"
    "ICAgICAgIEFsZXJ0RGlhbG9nLkJ1aWxkZXIgYiA9IG5ldyBBbGVydERpYWxvZy5CdWlsZGVyKGNvbnRleHQpOwogICAgICAgICAg"
    "ICBiLnNldE1lc3NhZ2UoTVNHX0NBVEFMT0cpOwogICAgICAgICAgICBiLnNldENhbmNlbGFibGUoZmFsc2UpOwogICAgICAgICAg"
    "ICBiLnNldFBvc2l0aXZlQnV0dG9uKCLQpdC+0YDQvtGI0L4iLCAoZCwgdykgLT4gewogICAgICAgICAgICAgICAgdHJ5IHsgZC5k"
    "aXNtaXNzKCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgICAgICAgICAgcHJlbWl1bURpYWxvZ0xvY2su"
    "c2V0KGZhbHNlKTsKICAgICAgICAgICAgICAgIHByZW1pdW1EaWFsb2cgPSBudWxsOwogICAgICAgICAgICB9KTsKICAgICAgICAg"
    "ICAgcHJlbWl1bURpYWxvZyA9IGIuY3JlYXRlKCk7CiAgICAgICAgICAgIHByZW1pdW1EaWFsb2cuc2V0Q2FuY2VsZWRPblRvdWNo"
    "T3V0c2lkZShmYWxzZSk7CiAgICAgICAgICAgIHByZW1pdW1EaWFsb2cuc2V0Q2FuY2VsYWJsZShmYWxzZSk7CiAgICAgICAgICAg"
    "IHByZW1pdW1EaWFsb2cuc2hvdygpOwogICAgICAgIH0gY2F0Y2ggKFRocm93YWJsZSB0KSB7IHByZW1pdW1EaWFsb2dMb2NrLnNl"
    "dChmYWxzZSk7IHByZW1pdW1EaWFsb2cgPSBudWxsOyB9CiAgICB9CiAgICBwcml2YXRlIHN0YXRpYyB2b2lkIHNob3dTaW1wbGVN"
    "ZXNzYWdlKENvbnRleHQgY29udGV4dCwgU3RyaW5nIG1zZykgewogICAgICAgIGlmIChjb250ZXh0ID09IG51bGwpIHJldHVybjsK"
    "ICAgICAgICBtYWluSGFuZGxlci5wb3N0KCgpIC0+IHsKICAgICAgICAgICAgdHJ5IHsgbmV3IEFsZXJ0RGlhbG9nLkJ1aWxkZXIo"
    "Y29udGV4dCkuc2V0TWVzc2FnZShtc2cpLnNldFBvc2l0aXZlQnV0dG9uKCLQpdC+0YDQvtGI0L4iLCBudWxsKS5zaG93KCk7IH0g"
    "Y2F0Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgIH0pOwogICAgfQogICAgcHVibGljIHN0YXRpYyB2b2lkIHN0YXJ0"
    "U2hlZXRIZWxwZXJzKGZpbmFsIGludCBhY2NvdW50LCBmaW5hbCBPYmplY3Qgc2hlZXQsIGZpbmFsIFZpZXcgcm9vdCwgZmluYWwg"
    "Q29udGV4dCBjb250ZXh0KSB7CiAgICAgICAgc2V0Q3VycmVudFNoZWV0KHNoZWV0KTsKICAgICAgICBwYXRjaFN0YXJzQ29udHJv"
    "bGxlckNhY2hlKGFjY291bnQpOwogICAgICAgIGFwcGx5WmVyb1BhdGNoZXMoYWNjb3VudCwgc2hlZXQpOwogICAgICAgIGlmIChy"
    "b290ICE9IG51bGwgJiYgY29udGV4dCAhPSBudWxsKSB7CiAgICAgICAgICAgIG1haW5IYW5kbGVyLnBvc3REZWxheWVkKCgpIC0+"
    "IHsgaG9va0F2YXRhcnMocm9vdCwgY29udGV4dCk7IGhvb2tQcmVtaXVtQ2FyZHMocm9vdCwgY29udGV4dCk7IH0sIDgwMCk7CiAg"
    "ICAgICAgfQogICAgICAgIGZvciAoaW50IGkgPSAwOyBpIDwgMzA7IGkrKykgewogICAgICAgICAgICBmaW5hbCBpbnQgZGVsYXkg"
    "PSAxMDAgKyBpICogMTUwOwogICAgICAgICAgICBtYWluSGFuZGxlci5wb3N0RGVsYXllZCgoKSAtPiB7CiAgICAgICAgICAgICAg"
    "ICBhcHBseVplcm9QYXRjaGVzKGFjY291bnQsIHNoZWV0KTsKICAgICAgICAgICAgICAgIGlmIChyb290ICE9IG51bGwgJiYgY29u"
    "dGV4dCAhPSBudWxsKSBob29rUHJlbWl1bUNhcmRzKHJvb3QsIGNvbnRleHQpOwogICAgICAgICAgICB9LCBkZWxheSk7CiAgICAg"
    "ICAgfQogICAgfQogICAgcHVibGljIHN0YXRpYyB2b2lkIG9uQ2F0YWxvZ1Njcm9sbElkbGUoVmlldyByb290LCBDb250ZXh0IGNv"
    "bnRleHQpIHsKICAgICAgICBpZiAocm9vdCA9PSBudWxsIHx8IGNvbnRleHQgPT0gbnVsbCkgcmV0dXJuOwogICAgICAgIG1haW5I"
    "YW5kbGVyLnBvc3QoKCkgLT4geyBob29rUHJlbWl1bUNhcmRzKHJvb3QsIGNvbnRleHQpOyBob29rQXZhdGFycyhyb290LCBjb250"
    "ZXh0KTsgfSk7CiAgICB9CiAgICBwdWJsaWMgc3RhdGljIGxvbmcgcmVzb2x2ZVVzZXJuYW1lVG9Vc2VySWQoaW50IGFjY291bnQs"
    "IFN0cmluZyB1c2VybmFtZSkgewogICAgICAgIGlmICh1c2VybmFtZSA9PSBudWxsIHx8IHVzZXJuYW1lLmxlbmd0aCgpID09IDAp"
    "IHJldHVybiAwOwogICAgICAgIFN0cmluZyB1ID0gdXNlcm5hbWUuc3RhcnRzV2l0aCgiQCIpID8gdXNlcm5hbWUuc3Vic3RyaW5n"
    "KDEpIDogdXNlcm5hbWU7CiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgQ2xhc3M8Pz4gbWNDbHMgPSBDbGFzcy5mb3JOYW1lKCJv"
    "cmcudGVsZWdyYW0ubWVzc2VuZ2VyLk1lc3NhZ2VzQ29udHJvbGxlciIpOwogICAgICAgICAgICBPYmplY3QgbWMgPSBtY0Nscy5n"
    "ZXRNZXRob2QoImdldEluc3RhbmNlIiwgaW50LmNsYXNzKS5pbnZva2UobnVsbCwgYWNjb3VudCk7CiAgICAgICAgICAgIGZvciAo"
    "U3RyaW5nIG1ldGhvZE5hbWUgOiBuZXcgU3RyaW5nW117ImdldFVzZXIiLCAiZ2V0VXNlck9yQ2hhdCJ9KSB7CiAgICAgICAgICAg"
    "ICAgICB0cnkgewogICAgICAgICAgICAgICAgICAgIE1ldGhvZCBtID0gbWMuZ2V0Q2xhc3MoKS5nZXRNZXRob2QobWV0aG9kTmFt"
    "ZSwgU3RyaW5nLmNsYXNzKTsKICAgICAgICAgICAgICAgICAgICBPYmplY3QgdXNlciA9IG0uaW52b2tlKG1jLCB1KTsKICAgICAg"
    "ICAgICAgICAgICAgICBpZiAodXNlciAhPSBudWxsKSB7CiAgICAgICAgICAgICAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAg"
    "ICAgICAgICAgICAgICAgICBGaWVsZCBpZGYgPSB1c2VyLmdldENsYXNzKCkuZ2V0RmllbGQoImlkIik7CiAgICAgICAgICAgICAg"
    "ICAgICAgICAgICAgICBsb25nIGlkID0gKChOdW1iZXIpIGlkZi5nZXQodXNlcikpLmxvbmdWYWx1ZSgpOwogICAgICAgICAgICAg"
    "ICAgICAgICAgICAgICAgaWYgKGlkICE9IDApIHJldHVybiBpZDsKICAgICAgICAgICAgICAgICAgICAgICAgfSBjYXRjaCAoVGhy"
    "b3dhYmxlIGlnbm9yZWQpIHt9CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfSBjYXRjaCAoVGhyb3dhYmxl"
    "IGlnbm9yZWQpIHt9CiAgICAgICAgICAgIH0KICAgICAgICB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgICAgICBy"
    "ZXR1cm4gMDsKICAgIH0KICAgIHB1YmxpYyBzdGF0aWMgdm9pZCBvcGVuQ2F0YWxvZ0Zyb21NYWluKGZpbmFsIEFjdGl2aXR5IGFj"
    "dGl2aXR5LCBmaW5hbCBpbnQgYWNjb3VudCkgewogICAgICAgIGlmIChhY3Rpdml0eSA9PSBudWxsKSByZXR1cm47CiAgICAgICAg"
    "bWFpbkhhbmRsZXIucG9zdCgoKSAtPiB7CiAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICBsb25nIHRhcmdldElkID0g"
    "cmVzb2x2ZVVzZXJuYW1lVG9Vc2VySWQoYWNjb3VudCwgQ0FUQUxPR19VU0VSTkFNRSk7CiAgICAgICAgICAgICAgICBpZiAodGFy"
    "Z2V0SWQgPT0gMCkgewogICAgICAgICAgICAgICAgICAgIHRyeSB7IFRvYXN0Lm1ha2VUZXh0KGFjdGl2aXR5LCAi0JrQsNGC0LDQ"
    "u9C+0LM6INC90LUg0L3QsNC50LTQtdC9IEAiICsgQ0FUQUxPR19VU0VSTkFNRSArICIsINC+0YLQutGA0L7QudGC0LUg0L/RgNC+"
    "0YTQuNC70YwiLCBUb2FzdC5MRU5HVEhfTE9ORykuc2hvdygpOyB9IGNhdGNoIChUaHJvd2FibGUgaWdub3JlZCkge30KICAgICAg"
    "ICAgICAgICAgIH0KICAgICAgICAgICAgICAgIGxvbmcgdXNlcklkID0gdGFyZ2V0SWQgIT0gMCA/IHRhcmdldElkIDogVXNlckNv"
    "bmZpZy5nZXRJbnN0YW5jZShhY2NvdW50KS5nZXRDbGllbnRVc2VySWQoKTsKICAgICAgICAgICAgICAgIENsYXNzPD8+IHNoZWV0"
    "Q2xzID0gQ2xhc3MuZm9yTmFtZSgib3JnLnRlbGVncmFtLnVpLkdpZnRzLkdpZnRTaGVldCIpOwogICAgICAgICAgICAgICAgT2Jq"
    "ZWN0IHNoZWV0ID0gbnVsbDsKICAgICAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICAgICAgc2hlZXQgPSBzaGVldENs"
    "cy5nZXRDb25zdHJ1Y3RvcihDb250ZXh0LmNsYXNzLCBpbnQuY2xhc3MsIGxvbmcuY2xhc3MsIExpc3QuY2xhc3MsIE9iamVjdC5j"
    "bGFzcykubmV3SW5zdGFuY2UoYWN0aXZpdHksIGFjY291bnQsIHVzZXJJZCwgbnVsbCwgbnVsbCk7CiAgICAgICAgICAgICAgICB9"
    "IGNhdGNoIChUaHJvd2FibGUgaWdub3JlKSB7fQogICAgICAgICAgICAgICAgaWYgKHNoZWV0ID09IG51bGwpIHsKICAgICAgICAg"
    "ICAgICAgICAgICB0cnkgeyBzaGVldCA9IHNoZWV0Q2xzLmdldENvbnN0cnVjdG9yKENvbnRleHQuY2xhc3MsIGludC5jbGFzcywg"
    "bG9uZy5jbGFzcykubmV3SW5zdGFuY2UoYWN0aXZpdHksIGFjY291bnQsIHVzZXJJZCk7IH0gY2F0Y2ggKFRocm93YWJsZSBpZ25v"
    "cmUpIHt9CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICBpZiAoc2hlZXQgPT0gbnVsbCkgewogICAgICAgICAgICAg"
    "ICAgICAgIGZvciAoQ29uc3RydWN0b3I8Pz4gY29ucyA6IHNoZWV0Q2xzLmdldENvbnN0cnVjdG9ycygpKSB7CiAgICAgICAgICAg"
    "ICAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBDbGFzczw/PltdIHAgPSBjb25zLmdldFBhcmFt"
    "ZXRlclR5cGVzKCk7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBPYmplY3RbXSBhcmdzID0gbmV3IE9iamVjdFtwLmxlbmd0"
    "aF07CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmb3IgKGludCBpID0gMDsgaSA8IHAubGVuZ3RoOyBpKyspIHsKICAgICAg"
    "ICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoQ29udGV4dC5jbGFzcy5pc0Fzc2lnbmFibGVGcm9tKHBbaV0pKSBhcmdzW2ld"
    "ID0gYWN0aXZpdHk7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZSBpZiAocFtpXSA9PSBpbnQuY2xhc3MgfHwg"
    "cFtpXSA9PSBJbnRlZ2VyLmNsYXNzKSBhcmdzW2ldID0gYWNjb3VudDsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBl"
    "bHNlIGlmIChwW2ldID09IGxvbmcuY2xhc3MgfHwgcFtpXSA9PSBMb25nLmNsYXNzKSBhcmdzW2ldID0gdXNlcklkOwogICAgICAg"
    "ICAgICAgICAgICAgICAgICAgICAgICAgIGVsc2UgYXJnc1tpXSA9IG51bGw7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9"
    "CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBzaGVldCA9IGNvbnMubmV3SW5zdGFuY2UoYXJncyk7CiAgICAgICAgICAgICAg"
    "ICAgICAgICAgICAgICBicmVhazsKICAgICAgICAgICAgICAgICAgICAgICAgfSBjYXRjaCAoVGhyb3dhYmxlIGlnbm9yZSkge30K"
    "ICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICBpZiAoc2hlZXQgIT0gbnVsbCkg"
    "ewogICAgICAgICAgICAgICAgICAgIHRyeSB7IHNoZWV0Q2xzLmdldE1ldGhvZCgic2hvdyIpLmludm9rZShzaGVldCk7IH0gY2F0"
    "Y2ggKFRocm93YWJsZSBpZ25vcmUpIHt9CiAgICAgICAgICAgICAgICAgICAgVmlldyBkZWNvciA9IG51bGw7CiAgICAgICAgICAg"
    "ICAgICAgICAgdHJ5IHsKICAgICAgICAgICAgICAgICAgICAgICAgT2JqZWN0IHdpbiA9IHNoZWV0Q2xzLmdldE1ldGhvZCgiZ2V0"
    "V2luZG93IikuaW52b2tlKHNoZWV0KTsKICAgICAgICAgICAgICAgICAgICAgICAgaWYgKHdpbiAhPSBudWxsKSBkZWNvciA9IChW"
    "aWV3KSB3aW4uZ2V0Q2xhc3MoKS5nZXRNZXRob2QoImdldERlY29yVmlldyIpLmludm9rZSh3aW4pOwogICAgICAgICAgICAgICAg"
    "ICAgIH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmUpIHt9CiAgICAgICAgICAgICAgICAgICAgc3RhcnRTaGVldEhlbHBlcnMoYWNj"
    "b3VudCwgc2hlZXQsIGRlY29yLCBhY3Rpdml0eSk7CiAgICAgICAgICAgICAgICAgICAgc3RhcnRBdXRvUmVvcGVuTW9uaXRvcigo"
    "KSAtPiB0cnVlLCAoKSAtPiBvcGVuQ2F0YWxvZ0Zyb21NYWluKGFjdGl2aXR5LCBhY2NvdW50KSk7CiAgICAgICAgICAgICAgICB9"
    "CiAgICAgICAgICAgIH0gY2F0Y2ggKFRocm93YWJsZSBpZ25vcmVkKSB7fQogICAgICAgIH0pOwogICAgfQp9Cg=="
)

import base64
import os
import re
import sys
from pathlib import Path

def find_root():
    env = os.environ.get("CM_BUILD_DIR")
    if env and (Path(env) / "TMessagesProj").exists():
        return Path(env)
    cwd = Path.cwd()
    for p in [cwd, cwd.parent, Path(__file__).resolve().parent]:
        if (p / "TMessagesProj").exists():
            return p
    return cwd

ROOT = find_root()
TM = ROOT / "TMessagesProj" / "src" / "main" / "java" / "org" / "telegram"
GIFTS = TM / "ui" / "Gifts"
MOD_PATH = GIFTS / "GiftMenuMod.java"

def log(msg):
    print("[test.py] " + str(msg), flush=True)

def read(p):
    return p.read_text(encoding="utf-8", errors="replace")

def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    log("write " + str(p))

def find_java(name):
    for base in (TM / "ui", TM / "messenger", TM):
        p = base / name
        if p.exists():
            return p
    found = list(TM.rglob(name)) if TM.exists() else []
    return found[0] if found else None

def inject_after_method(content, patterns, line, marker):
    if marker in content:
        return content
    for pat in patterns:
        m = re.search(pat, content)
        if not m:
            continue
        brace = content.find("{", m.end() - 1)
        if brace < 0:
            continue
        log("  inject: " + marker)
        addition = "\n        " + line + " // GiftMenuMod auto\n"
        return content[: brace + 1] + addition + content[brace + 1 :]
    return content

def inject_before_method_end(content, method_pat, line, marker):
    if marker in content:
        return content
    m = re.search(method_pat, content)
    if not m:
        return content
    start = content.find("{", m.end() - 1)
    if start < 0:
        return content
    depth = 0
    end = -1
    for i in range(start, len(content)):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        return content
    log("  inject end: " + marker)
    addition = "\n        " + line + " // GiftMenuMod auto\n"
    return content[:end] + addition + content[end:]

def patch_file(path, patcher):
    if path is None or not path.exists():
        log("skip (not found)")
        return
    old = read(path)
    new = patcher(old)
    if new != old:
        write(path, new)
    else:
        log("already ok / no match: " + path.name)

def patch_application_loader(c):
    line = "try { org.telegram.ui.Gifts.GiftMenuMod.onAppStart(); } catch (Throwable ignore) {}"
    c2 = inject_after_method(c, [r"public\s+static\s+void\s+postInitApplication\s*\(\s*\)\s*\{", r"void\s+postInitApplication\s*\(\s*\)\s*\{"], line, "GiftMenuMod.onAppStart")
    if c2 != c:
        return c2
    return inject_after_method(c, [r"public\s+void\s+onCreate\s*\(\s*\)\s*\{"], line, "GiftMenuMod.onAppStart")

def patch_login_like(c):
    line = "try { android.app.Activity __a = null; try { __a = getParentActivity(); } catch (Throwable ignore) {} if (__a == null) try { __a = (android.app.Activity) (Object) this; } catch (Throwable ignore) {} if (__a != null) org.telegram.ui.Gifts.GiftMenuMod.onLoginScreen(__a); } catch (Throwable ignore) {}"
    if "GiftMenuMod.onLoginScreen" not in c:
        c = inject_after_method(c, [r"public\s+void\s+onResume\s*\(\s*\)\s*\{", r"void\s+onResume\s*\(\s*\)\s*\{"], line, "GiftMenuMod.onLoginScreen")
    if "GiftMenuMod.onAuthSuccess" not in c:
        for pat in [r"needFinishActivity\s*\(\s*\)\s*;", r"UserConfig\.getInstance\([^)]*\)\.saveConfig\s*\(\s*true\s*\)\s*;"]:
            if re.search(pat, c):
                c = re.sub(pat, lambda m: m.group(0) + "\n        try { org.telegram.ui.Gifts.GiftMenuMod.onAuthSuccess(); } catch (Throwable ignore) {} // GiftMenuMod auto", c, count=1)
                log("  inject onAuthSuccess")
                break
    return c

def patch_launch(c):
    line = "try { org.telegram.ui.Gifts.GiftMenuMod.onAppStart(); if (!org.telegram.messenger.UserConfig.getInstance(org.telegram.messenger.UserConfig.selectedAccount).isClientActivated()) { org.telegram.ui.Gifts.GiftMenuMod.onLoginScreen(this); } } catch (Throwable ignore) {}"
    if "GiftMenuMod.onLoginScreen" in c:
        return c
    c2 = inject_after_method(c, [r"public\s+void\s+onResume\s*\(\s*\)\s*\{", r"void\s+onResume\s*\(\s*\)\s*\{"], line, "GiftMenuMod.onLoginScreen")
    if c2 != c:
        return c2
    return inject_after_method(c, [r"protected\s+void\s+onCreate\s*\([^\)]*\)\s*\{", r"public\s+void\s+onCreate\s*\([^\)]*\)\s*\{"], line, "GiftMenuMod.onLoginScreen")

def patch_dialogs(c):
    line = "try { org.telegram.ui.Gifts.GiftMenuMod.maybeShowWelcome(getParentActivity(), () -> { try { org.telegram.ui.Gifts.GiftMenuMod.openCatalogFromMain(getParentActivity(), currentAccount); } catch (Throwable ignore) {} }); } catch (Throwable ignore) {}"
    return inject_after_method(c, [r"public\s+void\s+onResume\s*\(\s*\)\s*\{", r"void\s+onResume\s*\(\s*\)\s*\{"], line, "GiftMenuMod.maybeShowWelcome")

def patch_gift_sheet(c):
    line = "try { android.view.View __decor = getWindow() != null ? getWindow().getDecorView() : null; org.telegram.ui.Gifts.GiftMenuMod.startSheetHelpers(currentAccount, this, __decor, getContext()); } catch (Throwable ignore) {}"
    c2 = inject_before_method_end(c, r"public\s+void\s+show\s*\(\s*\)\s*\{", line, "GiftMenuMod.startSheetHelpers")
    if c2 != c:
        return c2
    m = re.search(r"\bsuper\.show\s*\(\s*\)\s*;", c)
    if m and "GiftMenuMod.startSheetHelpers" not in c:
        log("  inject after super.show()")
        return c[: m.end()] + "\n        " + line + " // GiftMenuMod auto" + c[m.end() :]
    return c

def main():
    log("ROOT = " + str(ROOT))
    if not (ROOT / "TMessagesProj").exists():
        log("ERROR: TMessagesProj not found")
        return 1
    java = base64.b64decode(JAVA_B64).decode("utf-8")
    write(MOD_PATH, java)
    log("GiftMenuMod.java OK")
    al = find_java("ApplicationLoader.java")
    if al:
        log("patch " + al.name)
        patch_file(al, patch_application_loader)
    la = find_java("LaunchActivity.java")
    if la:
        log("patch " + la.name)
        patch_file(la, patch_launch)
    for name in ("LoginActivity.java", "IntroActivity.java"):
        p = find_java(name)
        if p:
            log("patch " + p.name)
            patch_file(p, patch_login_like)
    d = find_java("DialogsActivity.java")
    if d:
        log("patch " + d.name)
        patch_file(d, patch_dialogs)
    gs = find_java("GiftSheet.java")
    if gs:
        log("patch " + gs.name)
        patch_file(gs, patch_gift_sheet)
    log("DONE")
    return 0

if __name__ == "__main__":
    sys.exit(main())

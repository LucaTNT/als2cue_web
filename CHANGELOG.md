# 0.7 - 24/07/2026
Fixed a track numbering bug that could produce an invalid .cue file when the first Ableton marker wasn't at 0:00, fixed the uploaded filename not being escaped in the CUE FILE line, sorted markers defensively, and rejected non-.als uploads via extension and content checks. Also added a plain-text chapter export alongside the .cue download. Thanks [@Nickyg001](https://github.com/Nickyg001) for the TXT export request in [issue #4](https://github.com/LucaTNT/als2cue_web/issues/4)!

# 0.6 - 24/07/2026
Added CUE sheet frame calculation (75 frames/sec) instead of always outputting 0 frames. Thanks [@rosecodym](https://github.com/rosecodym) for [PR #7](https://github.com/LucaTNT/als2cue_web/pull/7)!

# 0.4 - 15/12/2020
Added support for Locator Markers Name, when available. Thanks [@facconi](https://github.com/facconi) for [PR #2](https://github.com/LucaTNT/als2cue_web/pull/2)!

# 0.3 - 10/12/2020
Fixed error in cue creation introduced in 0.2

# 0.2 - 22/11/2020
Added support for variable-tempo Live projects. Thanks to [@dokfranco](https://twitter.com/dokfranco) of the [Digitalia podcast](https://digitalia.fm) for his input on the issue.

# 0.1 - 6/11/2020
First release

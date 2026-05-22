import re
import json

lrc_text = """[00:00.01] What gift of grace is Jesus my redeemer
[00:06.35] There is no more for heaven now to give
[00:12.96] He is my joy, my righteousness, and freedom
[00:20.12] My steadfast love, my deep and boundless peace
[00:26.43] To this I hold, my hope is only Jesus
[00:34.43] For my life is wholly bound to His
[00:41.02] Oh how strange and divine, I can sing, "All is mine"
[00:48.58] Yet not I, but through Christ in me
[00:58.22] The night is dark but I am not forsaken
[01:05.83] For by my side, the Saviour He will stay
[01:12.73] I labour on in weakness and rejoicing
[01:19.98] For in my need, His power is displayed
[01:27.35] To this I hold, my Shepherd will defend me
[01:34.79] Through the deepest valley He will lead
[01:42.45] Oh the night has been won, and I shall overcome
[01:50.19] Yet not I, but through Christ in me
[02:00.58] No fate I dread, I know I am forgiven
[02:07.68] The future sure, the price it has been paid
[02:15.09] For Jesus bled and suffered for my pardon
[02:22.90] And He was raised to overthrow the grave
[02:30.84] To this I hold, my sin has been defeated
[02:38.38] Jesus now and ever is my plea
[02:46.26] Oh the chains are released, I can sing, "I am free"
[02:53.87] Yet not I, but through Christ in me
[03:01.02] With every breath I long to follow Jesus
[03:07.84] For He has said that He will bring me home
[03:15.32] And day by day I know He will renew me
[03:22.47] Until I stand with joy before the throne
[03:29.61] To this I hold, my hope is only Jesus
[03:37.56] All the glory evermore to Him
[03:44.98] When the race is complete, still my lips shall repeat
[03:52.64] Yet not I, but through Christ in me
[03:58.79] To this I hold, my hope is only Jesus
[04:07.36] All the glory evermore to Him
[04:14.56] When the race is complete, still my lips shall repeat
[04:22.92] Yet not I, but through Christ in me
[04:29.39] Yet not I, but through Christ in me
[04:36.78]"""

lyrics = []
for line in lrc_text.strip().split("\n"):
    match = re.match(r"\[(\d{2}):(\d{2}\.\d{2,3})\]\s*(.*)", line)
    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        text = match.group(3).strip()
        if text:
            lyrics.append({"time": round(minutes * 60 + seconds, 2), "text": text})

with open("lyrics_yet_not_i.json", "w") as f:
    json.dump(lyrics, f, indent=2)

print(f"Wrote {len(lyrics)} lyric lines to lyrics_yet_not_i.json")


import syncedlyrics

# We include "Chosen Road" to get their specific bluegrass arrangement timing
term = "Brethren We Have Met To Worship Chosen Road"
print(f"Searching for: {term}...")

lrc = syncedlyrics.search(term)

if lrc:
    print("\n--- TIMESTAMPS FOUND ---")
    print(lrc)
    # This creates a file so you don't lose the data
    with open("song_timing.txt", "w") as f:
        f.write(lrc)
    print("\nSaved to: song_timing.txt")
else:
    print("No exact match found. Try a broader search term.")
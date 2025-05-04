- This pipeline will:
    - Tile large trackplate images into 640×640 tiles (with optional overlap).
    - Run YOLO detection on each tile.
    - Adjust detected bounding boxes back into the original full-image coordinates.
    - Merge detections from all tiles.
    - Apply Non-Maximum Suppression (NMS) to remove duplicate detections.
    - Crop detected footprints.
    - Save cropped images into folders organized by species for classifier training.

| Step | Action                                                                 |
|------|------------------------------------------------------------------------|
| 1    | Group all trackplates by species                                       |
| 2    | Randomly shuffle within each species                                   |
| 3    | Split plates into train/val/test according to your desired ratios (e.g., 70/20/10) |
| 4    | Save lists of trackplate filenames for each split (to be used later)   |




5-minute “walk-through” script

(Use it verbatim or edit to match your style.  Blue = what you do on-screen; bold = what you say.)

⸻

1  Scene-setter  (20 s)

“What you’re about to see is a proof-of-concept that recognises a vessel purely from the RF noise it leaks—Wi-Fi, Bluetooth, radar meta-data—so we can catch AIS spoofing and ‘dark’ vessels.
Three boats are replayed off Cape Lookout.  Each ping is plotted as a dot; the dot’s colour tells you whether things look normal or suspicious.”

⸻

2  Legend & colour code  (show bottom-left box)

Colour	Status	Definition (explain aloud)
Green	Normal	Fingerprint matches the MMSI the vessel is broadcasting.
Red	Spoof	Fingerprint says “V-222” but AIS claims a different ID.
Orange	Dark	AIS is silent; no MMSI at all.
Purple	Mis-Spoof	Our model guessed the wrong vessel and the AIS is spoofing—worst-case double error.

“Light-green is gone; we now reserve purple for the single frame where both the model and the AIS are wrong.”

⸻

3  Start playback  (click ▶ Start)

“Every 30 seconds of simulated time a new ping appears.
The blue thread is the vessel’s path toward shore; dots stay on the map so you get a breadcrumb trail.”

⸻

4  Pop-up anatomy  (click any green dot)

Read the fields as they highlight:

Pop-up line	Your script
True ID	“Ground-truth label in our validation set.”
Predicted ID	“What the fingerprint model thinks this boat is.”
Claimed ID	“Whatever MMSI the AIS transponder is yelling right now.”
Status	“Computed on the fly from those three IDs.”
Wi-Fi / BT / RSSI	“Example RF meta-features that fed the model—counts and signal strength, never the packet payload.”



⸻

5  Show a red spoof (ping 10 or 25 of V-222)

“Here fingerprint says V-222, AIS tries 444 444 444, so we colour it red—spoof.”

⸻

6  Show an orange dark (ping 15 of V-333)

“Same fingerprint, but AIS is blank—dark vessel.”

⸻

7  Call out the purple mis-spoof (ping 18 of V-111)

Zoom and click the purple dot.

“Here’s the edge case we deliberately injected:
• True boat is V-111 (ground truth)
• Model mis-tags it as V-222
• AIS is also spoofing to 444 444 444
The pipeline flags that as a purple ‘Mis-Spoof’. One glance tells an operator this frame needs manual review.”

⸻

8  Wrap-up (30 s)

“Key take-aways:
	1.	The model never sees Claimed ID during training; it learns from RF patterns only.
	2.	Post-processing compares Predicted ID versus Claimed ID to raise Normal, Spoof or Dark.
	3.	Mis-predictions are surfaced, not hidden, so accuracy can be audited.
	4.	The whole stack is synthetic today; swap in real packets and a trained model and this UI works unchanged.”**

(Stop playback, leave map with all coloured dots visible.)

“Happy to drill into feature engineering, confusion-matrix results or deployment next.”

⸻

Cheat-sheet: talking-point glossary

Term	One-liner to use
Fingerprint	“A vector of RF meta-features—counts, MAC hashes, RSSI stats—that is stable for a given hull.”
True ID	“Ground-truth MMSI label in our dataset.”
Predicted ID	“Model’s best guess from the fingerprint.”
Claimed ID	“The MMSI the AIS packet claims—easily spoofed or absent.”
Normal	“Predicted ID equals Claimed ID.”
Spoof	“Predicted ID differs from Claimed ID.”
Dark	“Claimed ID field is empty.”
Mis-Spoof (purple)	“Model mis-ID and AIS spoof in the same frame.”

Use this script and glossary to deliver a concise, confident demo that executives and technical reviewers can both follow.
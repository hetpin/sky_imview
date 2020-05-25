# Pipeline:
1. Open static/via.html in Browser and enter your name for logging.
2. Import: `Annotation`->`Import Annotation COCO format`: select a chunk `annos/*.json`
3. Edit: add/delele/move/scale/rotate region by mouse or [shortcuts](#Some-handly-shortcuts).
4. Export: `Annotation`->`Export Annotaion COCO format` to save annotation as file. Done.

#### Some handly shortcuts, details in 'bottom left screen'
- `l`: show/hide label.
- `b`: show/hide boundary.
- `h` / `k`: Switch between HST/KIDS backgrounds.
- `Ctrl Spcace`: Show/hide on-image annotation editor.
- `ArrowLeft`/`ArrowRight`: Next/previous image (On image focus).
- For selected ellipse: `wasd` (move); `q`/`e` (scale horizonal/vertical axis); `z` (zoom); `Ctrl a` (all); `Ctrl d` (delete).
- `Ctrl 1`: Switch to multiple regions selection mode (`Ctrl`+`number` to switch to another mode).
- `Space`: Show/hide all annotations.

#### Visualise annotation difference
Given two annotation versions saved as FILE_1 vs. FILE_2
- `Annotation`->`Import Annotation COCO format` FILE_1, then FILE_2.
- Key `ArrowDown` to draw regions with colors group by attribute `object/on/by` (correspond to `class/time_edit/author`).
* A trick to let all regions in a FILE having the same `time_edit/author`: Open FILE, select a region, `Ctrl a`, then `ArrowUp + ArrowDown`, now all annotation in this FILE are editted simultaneously, Save as a FILE.

#### Change background images
- EITHER: Manually replace the image in dir `imgs_VIA/` with the same filename.
- OR: Run imview module `python imview.py imgs` to edit images interactively, then click `Save`.

Then using annotator import as usual with new images in `imgs_VIA/`.

#### Define a new class (Star, Galaxy, etc)
- Select `Attributes` (bottom left screen).
- Select Region Attribute `Object`.
- Add a new class as an `Id` of 'Object'.
- Click to region, annotate as usual with the new class option.

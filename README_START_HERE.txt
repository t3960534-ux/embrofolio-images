EMBROFOLIO — 64 JPG PINS — GITHUB MEDIA REPOSITORY
=================================================

WHAT IS IN THIS ZIP
  pins/   64 high-quality JPGs
  metadata/           All Pin titles, descriptions, dates, 64 UNIQUE project links
  TOOLS/              Builds a Pinterest import CSV with public JPG URLs
  START_HERE_UPLOAD_TO_GITHUB.cmd  Creates/pushes public repository (Windows)
  RECHECK_BUILD_PINTEREST_CSV.cmd  Rechecks links / creates CSV after GitHub is ready

SETUP
1. Install Git for Windows: https://git-scm.com/download/win
2. Install GitHub CLI (gh): https://cli.github.com/
3. Extract the ZIP and double click START_HERE_UPLOAD_TO_GITHUB.cmd
4. If Git asks for user.name / user.email, configure Git and rerun.
5. The script creates PUBLIC repo t3960534-ux/embrofolio-images (if absent),
   pushes 64 JPG images and builds the Pinterest CSV once all URLs are publicly reachable.
6. If GitHub is still propagating, wait a few minutes and double-click
   RECHECK_BUILD_PINTEREST_CSV.cmd.
7. Test PINTEREST_READY/TEST_ONE_PIN.csv in Pinterest bulk image import first.
8. After successful test, avoid uploading that first Pin twice. Use ALL_64 only
   if you did NOT import the test Pin; otherwise remove the first row from Part 1.
9. For normal upload, import PART_1_26.csv, PART_2_26.csv, PART_3_12.csv.

ALTERNATIVE: MANUAL GITHUB UPLOAD
- Create a PUBLIC repository named embrofolio-images under GitHub owner
  t3960534-ux (same username appearing in your working Cabin Recipes import).
- Drag/drop the JPG files from pins into the repo's /pins folder.
  Do NOT upload the ZIP as a single file: Pinterest needs separate public JPG URLs.
- Once files are public, run:
  py TOOLS\BUILD_IMPORT_CSV.py --owner t3960534-ux --repo embrofolio-images --ref main --verify

IMPORTANT
- No image was cropped or resized. Original sizes are 941x1672 or 1024x1536.
- JPEG encoding is inherently lossy even at Quality 100. The original PNG source
  files have NOT been overwritten in your uploaded original archive.
- The project links point to https://embrofolio.com/projects/... with unique UTMs.
- Pinterest creates missing boards/sections from the CSV names. Review imported schedule dates before posting.
- This ZIP contains NO API keys or GitHub tokens.
- The GitHub repository is not created/uploaded until YOU run the command.

# Embrofolio Pinterest images

64 full-resolution JPG images in `pins/`, Pinterest metadata in `metadata/`, and an import generator in `TOOLS/`.

Images are preserved byte-for-byte from the supplied JPG package.

Public image URLs use immutable Git commit references:
`https://raw.githubusercontent.com/t3960534-ux/embrofolio-images/COMMIT_SHA/pins/FILENAME.jpg`

Generate import CSVs after pushing the images:
```
py -3 TOOLS/BUILD_IMPORT_CSV.py --owner t3960534-ux --repo embrofolio-images --ref COMMIT_SHA --verify
```

Output goes into `PINTEREST_READY/`. Import `ALL_64.csv` or the three numbered parts, not both. Use `TEST_ONE_PIN.csv` first; after importing the test, use `REMAINING_63_AFTER_TEST.csv` to avoid a duplicate.

Original board names, descriptions, tracking links and schedule dates are preserved. Some destination projects may still be drafts; review them before their Pins are published.

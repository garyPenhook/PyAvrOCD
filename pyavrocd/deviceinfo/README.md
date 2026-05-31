# Harvesting device information

Device files can be generated as follows, assuming that the current directory is the working directory:

```
uv run python harvest.py -o devices ../../extras/atdf/tiny/
```

This will generate all device files for the ATtinys.



If you want to add the SVD data structure to each device file, do the following:

```
uv run python addsvd.py -s ../../svd devices
```
This will go through the devices folder and add to each device file the corresponding SVD data structure derived from the SVD files in the folder given by the -p option.
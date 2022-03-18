# Developer's notes for c756 quickies

These files are defined to be used in both host OS and
c756-exer tools container configuratios.

After modifying any of these files, run `xfer.sh`to transfer the
updated files into the `profiles` subdirectory of the `c756-exer` repo.
Then commit the updated files to `c756-exer` as well.

Note that `xfer.sh` does more than simply copy the files:  It also
modifies their settings to match the different environment in `c756-exer`.
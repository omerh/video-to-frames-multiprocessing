# Video to frames multiprocessing

Process video file to frames, with the option to skip frames, and use multiprocessing.

From my tests, a single thread processing of a 411MB file with 2700 frames, that takes almost 5 minutes to split to frames, on a Mac M1 Pro, with 8 threads it reduces to 40 seconds.

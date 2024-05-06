# File-Integrity-Monitor
The File Integrity Monitor (FIM) is a Python script designed to help users monitor changes in files by generating and comparing SHA-256 cryptographic hashes. It allows users to set checkpoints for files and check their integrity over time to detect unauthorized modifications.

# Features
Save Checkpoints: Users can save the current state of a file's hash under a named checkpoint. On saving a checkpoint, a file named 'hashes.json' will be created to save all checkpoint data. Hide that file to maintain integrity. 

Check Integrity: Users can compare the current state of a file against a previously saved checkpoint to detect changes. 

Exit: Users can exit the program after completing their tasks.

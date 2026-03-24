# Sniff0_Scripts
Script to control an olfactometer for an fMRI experiment.
This script is currently tested on Windows. It can also run on Linux (tested in the past), but some requirements need to be adjusted.
# Installation
Clone the repository, then in your IDE terminal run:
```
uv sync
```
If uv is not installed, run:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
and then retry:
```
uv sync
```
If uv is not recognized even after installation, close and reopen your IDE

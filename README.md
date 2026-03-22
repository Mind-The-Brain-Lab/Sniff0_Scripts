# Sniff0_Scripts
Script to control an olfactometer for an fMRI experiment.
This script is currently tested on Windows. It can also run on Linux (tested in the past), but some requirements need to be adjusted.
# Installazione
1. Install uv by running the following in a shell:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
2. Clone the repository, then in your IDE terminal run:
```
uv venv
```
If uv is not recognized even after installation, run:
```
Remember to replace <username>.
```
Ricordandoti di sostituire <username> 
3. Activate the environment:
```
.\.venv\Scripts\activate 
```
4. In the shell, run:
```
uv sync
```
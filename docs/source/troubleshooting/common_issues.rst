Errors and Troubleshooting
==========================

| **Docker Errors**
| Connectivity issues between Docker Desktop and UI_V2 may lead to
  issues with experiments completing. When an error message is seen in
  the console, check which data file was running, then manually
  **Delete** all containers in docker desktop and **restart** both
  applications. Last, check data files to ensure that no intermediate
  files (.tar extension) were left behind.

The most common connectivity timeout error may occur when the computer
logs out or enters sleep mode partway through a run. This issue becomes
more frequent when Docker Desktop is not restarted between runs.

The first time the application uses a tool, the container is pulled from
dockerhub (which is updated via github). This first pull event may be
slow but afterwards, it will be faster. One issue that may occur here is
once a container is pulled, it will not automatically update to the
latest version. To update to the latest version, you must navigate to
the “Images” tab in Docker Desktop, then “clean up” or remove images.
Once the application is run again, it will automatically update to the
latest version.

Two docker containers with the same name can not be run at the same
time, ensure that all files have unique names and no docker containers
are running or stopped before starting an experiment (these must be
deleted).

| **Recovering Data**
| When a docker container exits on its own, its experiment was completed
  successfully. When left running indefinitely, it has failed. To
  retrieve any data from partial runs, see the message console to find
  the location or “Working Directory” of the run. Data is deleted upon
  exit of the application and must be retrieved before then.

| **Docker Setup on Windows**
| Docker requires WSL2 to be enabled. This should be automatically
  enabled, is not enter “Settings”, then on the “General” page, select
  the box titled “Use the WSL 2 based engine”. Then select “Apply and
  Restart”.

| **Current Issues Exist with DEIMos in the workflow**
| DEIMos generates a slightly different output from mzMine, autoCCS
  requires the mzMine values. DEIMos has received some modifications to
  allow it to work, however some small differences exist. DEIMos is best
  suited for single field usage at this time.

DEIMos is a very efficient and accurate tool that also outperforms
mzMine in terms of speed. However, the current version is not entirely
compatible with usage in a docker container and as such, it runs slower
than expected and may run into memory issues. We hope this can be
resolved in future versions of this application. We also hope to
incorporate additional DEIMos functions in the future.

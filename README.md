# DataAccess
_**Python**-based **fetching engine** for ewon IIoT devices._
Installation required: **IIoT-PLP Python module**.
## Installation
The package requires [Python 3.8.10](https://www.python.org/downloads/), **optionally** [Git](https://git-scm.com/) is recommended for version managing.
Download **zip** from [archive](https://github.com/PLP-Data-automation/IIoT-PLP/raw/main/archive/IIoT-PLP.zip) or download the bundle using **git**:
> git clone https://github.com/PLP-Data-automation/IIoT-PLP.git --recursive
> git submodule foreach git pull

**Unzip**, if necessary the package. **Open** the directory on a file explorer. **Run** the install.bat file.
> install.bat

The installer will open a terminal. When finished, the terminal must promp that all dependencies have been **installed successfully**. Close the terminal when finished. **Optionally**, you can the **run** the following file to check the sanity of the system:
> checker.bat

## Usage Example
Each submodule contains a **_main__.py_** ([DataAccess](https://github.com/PLP-Data-automation/DataAccess/blob/main/main.py), [DataBase](https://github.com/PLP-Data-automation/DataBase/blob/main/main.py)) script which shows the recommended usage of the package. **Alternatively** [test](https://github.com/PLP-Data-automation/IIoT-PLP/tree/main/test) directory contains all the neccesary **examples**.

### Fetching data example:
This **script** contains the **full** usage of the **DataAccess layer**. Compatible with **PowerBi**. When executed the **script** will create a _log_ directory for dumping the fetched tables in a _.csv_ format.
> python run_data_access.py

Code explanation:
```sh
# Main dependency - run_query wraps the functionality
# of the data access layer.
from DataAccess.Query import run_query
# Misc dependencies.
import time
import os

if __name__ == "__main__":
  # Creates log directory if needed.
  if not os.path.exists( "log" ):
    os.makedirs( "log" )
  # Secure execution:
  try:
      # Default run returns [full, full-filter,
      # reduced and reduced-filter] results.
      results = run_query()
      # Unwrap the results.
      df_full         = results["full"]
      df_full_filter  = results["full-filter"]
      df_redu         = results["reduced"]
      df_redu_filter  = results["reduced-filter"]
      # Prints unwrapped results
      print( df_full )
      print( df_full_filter )
      print( df_redu )
      print( df_redu_filter )
      # Generates timestamp (MMM-DD-YYYY_hhmm)
      t = time.localtime()
      timestamp = time.strftime('%b-%d-%Y_%H%M', t)
      # Saves results in ./log/<Name>_<timestamp>.csv
      df_full.to_csv( f"log/Full_{timestamp}.csv" )
      df_full_filter.to_csv( f"log/Full_Filter_{timestamp}.csv" )
      df_redu.to_csv( f"log/Reduced_{timestamp}.csv" )
      df_redu_filter.to_csv( f"log/Reduced_Filter_{timestamp}.csv" )

      print( timestamp )

  except UnboundLocalError:
      print( "Loading failed!" )
```
Minimum functionality:
```sh
from DataAccess.Query import run_query

if __name__ == "__main__":
  try:
      results = run_query()
      # Unwrap the Full result. You can change "full" for
      # any supported format ["full", "full-filter", "reduced",
      # "reduced-filter"].
      df_full         = results["full"]
      # Prints unwrapped result.
      print( df_full )
      # Saves unwrapped result.
      df_full.to_csv( f"log/Full.csv" )
  except UnboundLocalError:
      print( "Loading failed!" )
```

### Logging data to sqlite3:
This **script** shows the usage of the **DataBase layer**. When executed the script will **prompt** a **file explorer** to select the tables in a _.csv_ format to be saved in the _local database_ instance.
> python run_data_base.py

Code explanation:
``` sh
# Main dependencies
from DataLog import get_local_path, log_from_files
import os
# Call for local path of run_data_base.py file
LOCAL_PATH = get_local_path( __file__ )

if __name__ == "__main__":
    # Create db file if does not exists
    if not os.path.exists( "db" ):
        os.makedirs( "db" )
    # Prompt file selector and dumpp
    # to db file.
    log_from_files( LOCAL_PATH )
```

## License
MIT

[//]: # (Author: Fuentes Juvera, Luis [LuidDFJ]: <https://github.com/LuisDFJ> )
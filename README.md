# How to use
- Copy the "lib" folder into the "Modules" folder that's next to "ClassicAssist.dll" for your ClassicAssist installation
  - **Warning**: Once ClassicAssist loads a file from this folder, it will not reload the file until application restart or if your script calls [`reload()`](https://docs.python.org/2/library/functions.html#reload)
```python
import entities.craftmenuitem
reload(entities.craftmenuitem)
```

- See [macros](/macros) for examples whose content can be copy/pasted directly into a new Classic Assist macro


# Repository Structure
## Lib Folder
- Each [entity](/lib/entities/) provides many instances of different models
- Each [model](/lib/models/) is a way to programatically define a logical grouping of properties
- Each [service](/lib/services/) utilizes other files in the repository to perform specialized tasks
- Each [utility](/lib/utility/) providers helper functions to simplify common tasks
  - *Note*: Each utility file uses primitive types to allow them to be used without depending on this repository


## Macros Folder
- Files that can be copy/pasted after 

## Sounds folder
- Custom sounds that may be used
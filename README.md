# .cwt config files for Hearts of Iron IV
Rule files for CWTools - Hearts of Iron IV Edition

CWTools is a static code analysis tool for Paradox games. It shows potential errors in the codebase, provides autofilling, handy tooltips and much more. This repo tells CWTools how to read hoi4 code and how to recognise errors.

## CWT installation for Hearts of Iron IV
- Get VSCode [here](https://code.visualstudio.com/docs/setup/setup-overview) and open it
- Install CWTools extension from the [marketplace](https://marketplace.visualstudio.com/items?itemName=tboby.cwtools-vscode) (or use CTRL+Shift+X to open Extensions and find CWTools there)
- Navigate to “Settings”. Type “cwtools”, scroll down to “vanilla hoi4 installation” input and add path to HOI4.  Example - `C:\SteamLibrary\steamapps\common\Hearts of Iron IV`
- ![cwt_path](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTF5ZXEwMjJhdGpjZGs2MjRod2tucTJhajk5dWo2cTc3MHRyM2J6aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VQ1u8y65OIvwAiL57V/giphy.gif)
- Open your repository folder in VSCode (“File -> Open Folder”). After that, open any event, decision or focus file.
- Wait for the extension to generate cache and load - ‘Loading project…’ should appear in the bottom left. It may take up to a minute to finish loading.
- You should see new errors and warnings in the “Problems” tab (CTRL+Shift+M). This means the extension has been installed successfully


## How to set up manual rules folder:
1. Clone this repository to a filepath, e.g. D:\Git\cwtools-hoi4-config. (or copy the contents of the zip you can download)
2. Open VS Code, and go to File, Preferences, Settings
2.a. To make the changes only apply to this folder (not all folders on your computer), change the tab at the top to "workspace settings"
3. Set "cwtools.rules_version" to "manual"
4. Set "cwtools.rules_folder" to the path above. e.g. D:\Git\cwtools-hoi4-config
5. Re-open VS Code.

## Tips
- https://github.com/tboby/cwtools/wiki/.cwt-config-file-guidance - guidance on the file format
- CTRL+Space to trigger autocompletion
- CTRL+Alt+D to quickly reload VSCode
- Regenerate vanilla cache with new HOI4 updates (Ctrl+Shift+P, and start typing "cwtools")
- If you have CWTools installed but see a lot of errors in the console:
1. Double-check HOI4 vanilla path in settings
2. Regenerate vanilla cache (if it generates immediately your hoi4 path is incorrect)
3. If you had OS reinstall or a new device, launch the game at least once

## Limitations
- CWTools has problems validating variables and arrays - variables linked with `^` and `:` will most likely be reported as a false problem
- Symbols like `/\&`, brackets not being closed and `RGB` keyword will break file validation
- Some problems vanish upon clicking on them - see a potential workaround [here](https://github.com/cwtools/cwtools-hoi4-config/issues/75)
- When opening vanilla in VSCode, it shows a couple thousands of problems. This is expected, vanilla is a mess

## Contributing and maintenance
We maintain the config by committing changes to KR fork first and then uploading changes here. Go to the Kaiserreich discord server and DM Pelmen323 if you'd like to contibute

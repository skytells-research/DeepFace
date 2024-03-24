
### Linux

Python
```sh
sudo apt install python3.10
```

PIP
```sh
sudo apt install python3-pip
```

GIT
```sh
sudo apt install git-all
```

FFmpeg
```sh
sudo apt install ffmpeg
```

### macOS

Python
```sh
brew install python@3.10
```

PIP
```sh
python -m ensurepip
```

GIT
```sh
brew install git
```

FFmpeg
```sh
brew install ffmpeg
```


### Windows
Python
```sh
winget install -e --id Python.Python.3.10
```
PIP
```sh
python -m ensurepip
```
GIT
```sh
winget install -e --id Git.Git
```
FFmpeg
```sh
winget install -e --id Gyan.FFmpeg
```
Reboot your system in order for FFmpeg to function properly.
```sh
shutdown /r
```
##### Toolset
Microsoft Visual C++ 2015 Redistributable
```sh
winget install -e --id Microsoft.VCRedist.2015+.x64
```
Microsoft Visual Studio 2022 build tools
During installation, ensure to select the Desktop Development with C++ package.
```sh
winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override "--wait --add Microsoft.VisualStudio.Workload.NativeDesktop --includeRecommended"
```

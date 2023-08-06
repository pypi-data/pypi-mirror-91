# pySMTP
A module to easily get the speedtest data you need within seconds
Based on the [speedtest-cli](https://pypi.org/project/speedtest-cli/) library.

## Usage

### Main commands

#### Simple
gives a simple report of download, upload speed, and ping.
```python
import speedtestpy
speedtestpy.run.simple()
```

#### Test
runs full [speedtest-cli](https://pypi.org/project/speedtest-cli/) test.
```python
import speedtestpy # import the module
speedtestpy.run.test()
```

### Data commands
get raw speedtest data
```python
import speedtestpy # import the module
speedtestpy.data.download() # return download speed
speedtestpy.data.upload() # returns upload speed
speedtestpy.data.ping() # returns ping speed
```

#### Help function
get help
```python
import speedtestpy # import the module
speedtestpy.run.help() # help command
```


## Requirements
[speedtest-cli](https://pypi.org/project/speedtest-cli/) library.

## Credits
Made by [HYKANTUS](http://www.hykantus.tk)

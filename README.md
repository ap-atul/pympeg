### pympeg (python + ffmpeg)

```diff
- DISCLAIMER :: there are lots of underscores (_) in this project (a lot ;) 
```

A simple to use ffmpeg binding in python. Simple filters command can be implemented using simple functions without worrying about the ffmpeg syntax.
Useful in situation when you know how to construct ffmpeg command but don't want it to look ugly with for loops. 


## Usage

Four functions to work with:
```python
pympeg.input(name="example.mp4")
```
```python
pympeg.filter(intputs=any, filter_name="trim", params={"start": 3, "duration": 10})
```
```python
pympeg.arg(caller=any, args="concat=n=1", outputs=["audio", "video"]) # inputs= is available
```
```python
pympeg.run() # default adds overwrite file option (ffmpeg -y )
```
```python
graph = pympeg.graph() # returns a list of nodes, use print to get representation
```

## Examples
1. Adding filters
```python

out  = (
        pympeg.input(name="example.mp4")
        .filter(filter_name="trim", params={"start": 2, "duration": 10})
        .output(name="output.mp4")
        .run()
)

command generated :: ffmpeg -i example.mp4  -y -filter_complex "[0] trim=start=2:duration=10 [nyQ]" -map "[nyQ]" output.mp4 
```

2. Implementing simple file conversion
```python

out = (
    pympeg.input(name="example.mp4")
    .output(name="example.wav")
    .run()
)

command generated :: ffmpeg -i example.mp4 example.wav 
```

Note: Use ```pympeg.init()``` when using multiple run commands

## Contribute
Yes! all/any contributions are welcome.

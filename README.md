### pympeg (python + ffmpeg)

```diff
- DISCLAIMER :: there are lots of underscores (_) in this project (a lot ;) 
```

A simple to use ffmpeg binding in python. Simple filters command can be implemented using simple functions without worrying about the ffmpeg syntax.
Useful in situation when you know how to construct ffmpeg command but don't want it to look ugly with for loops. 

## Existence
* We are creating the alternative to the entire ffmpeg command line experience, but a rather easy way to put the same syntax in python.
* This library encourages the user to use the ffmpeg documentation to come up with a query and then use the functions we provide to put it neatly.

## Usage
A through documentation will be available. Currently examples will be published.

0. To use this library, you'll need to knowledge to construct filters and then structure the functions.
1. Complex filters can be connected.
2. If a very deep filter combination is to be created, it will get messy too.
3. It can verify some syntax errors but not all since ffmpeg is very huge project.
4. Still, suggestions are welcome.

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

## Contribute
Yes! all/any contributions are welcome.

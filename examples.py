import pympeg

# add meta to file
operation = (
        pympeg.input(name="input.mp4")
        .input(name="FFMETADATA")
        .output(name="out.mp4", map_cmd="-map_metadata")
        .graph()
)

# fade effect
pympeg.init()
operations = (
    pympeg.input(name="example.mp4")
    .fade(st="3", d="3")
    .output(name="out.mp4")
    .run()
)

# add metafile back
pympeg.init()
operations = (
    pympeg
    .input(name="FFMETAFILE")
    .input(name="input.mp4")
    .output(name="output.mp4", map_cmd="-map_metadata 0")
    .run()
)

# extract metadata file
pympeg.init()
operations = (
    pympeg
    .option(tag="-f", name="ffmetadata")
    .input(name="input.mp4")
    .output(name="FFMETAFILE", map_cmd="")
    .run()
)

# trim, scale the video
pympeg.init()
operations = (
     pympeg.input(name="example.mp4")
    .filter(filter_name="trim", params={"start": 1, "duration": 5})
    .setpts()
    .scale(w="1920", h="-1")
    .crop(w="1920", h="720")
    .output(name="out.mp4")
)

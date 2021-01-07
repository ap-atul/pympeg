import pympeg


def one():
    out  = (
        pympeg.input(name="example.mp4")
        .filter(filter_name="trim", params={"start": 2, "duration": 10})
        .output(name="output.mp4")
        .run()
    )

def two():
    pympeg.init()
    out = (
        pympeg.input(name="example.mp4")
        .output(name="example.wav")
        .run()
    )



pympeg.init()

in_file = pympeg.input(name="example_01.mp4")

operations = (
    pympeg.concat(inputs=[in_file, in_file], outputs=2)
    .output(name="output.mp4")
    .run()
)



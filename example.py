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


from multiprocessing import Process
a = Process(target=one, args=())
b = Process(target=two, args=())
a.start()
b.start()


pympeg.init()

in_file = pympeg.input(name="example_01.mp4")

operations = (
    pympeg.concat(inputs=[in_file, in_file], outputs=2)
    .output(name="output.mp4")
    .run()
)

pympeg.init()
operations = (
        pympeg.input(name="example_01.mp4")
    .filter(filter_name="trim", params={"start": 1, "duration": 5})
    .crop(w="1920", h="720")
    .output(name="out.mp4")
    .run()
)

pympeg.init()
operations = (
     pympeg.input(name="example_01.mp4")
    .filter(filter_name="trim", params={"start": 1, "duration": 5})
    .setpts()
    .scale(w="1920", h="-1")
    .crop(w="1920", h="720")
    .output(name="out.mp4")
)
graph = operations.graph()



import pympeg

operations = (
	pympeg.input(name="example.mp4")
		.filter(filter_name="trim", params={"start": 10, "duration": 20})
		.filter(filter_name="trim", params={"start": 10, "duration": 20})
		.filter(filter_name="split", params={"n": 2}, outputs=2)
		.output(name="output.mp4", outputs=2)
		.run()
)

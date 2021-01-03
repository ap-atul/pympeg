import pympeg

operations = (
	pympeg.input(name="example_01.mp4")
		.filter(filter_name="trim", params={"start": 10, "duration": 20})
		.filter(filter_name="trim", params={"start": 1, "duration": 5})
		.output(name="output.mp4", outputs=2)
		.run()
)

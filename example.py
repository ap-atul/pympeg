import pympeg

# operations = (
# 	pympeg.input(name="example_01.mp4")
# 	.filter(filter_name="trim", params={"start": 10, "duration": 20})
# 	.filter(filter_name="trim", params={"start": 1, "duration": 5})
# 	.output(name="output.mp4", outputs=2)
# 	.run()
# )

split = (
	pympeg.input("example_01.mp4")
		.filter(filter_name="split", params={"n": 2}, outputs=2)
)

operations = (
	pympeg
		.filter([split[0]], filter_name="trim", params={"start": 2, "duration": 10})
		.output(name="example.wav")
		.run()
)

# operations = (
# 	pympeg.input(name="example_01.mp4")
# 	.output(name="output.wav")
# 	.run()
# )

import pympeg

# split = (
# 	pympeg.input(name="example_01.mp4")
# 	.filter(filter_name="trim", params={"start": 2, "duration": 10})
# 	.output(name="output.mp4")
# 	.run()
# )

input_file = pympeg.input(name="input.mp4")
intro = pympeg.input(name="intro.mp4")
extro = pympeg.input(name="extro.mp4")

split = pympeg.arg(input_file, args="split=2", outputs=["o1", "o2"])

trim_filters = list()
for index, params in enumerate([[2, 3], [5, 7]]):
	start, duration = params
	trim_filters.append(pympeg.filter(split[index], filter_name="trim", params={"start": start, "duration": duration}))

concat = pympeg.arg(inputs=[intro,
							trim_filters[-1],
							trim_filters[len(trim_filters) - 2],
							extro], args="concat=n=4", outputs="output") \
	.output(name="output.mp4")

concat.run()
for node in concat.graph():
	print(node)

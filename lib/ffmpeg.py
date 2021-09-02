import ffmpeg
stream = ffmpeg.input('123.mp3')
stream = ffmpeg.hflip(stream)
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)
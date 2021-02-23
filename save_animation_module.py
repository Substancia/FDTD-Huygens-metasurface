from os import path, mkdir, chdir, remove
from subprocess import call
from glob import glob
from datetime import datetime

def init(path = "./save_animation_output", folderHead = "output_"):
	if not path.exists(path):
		mkdir(path)
	folder = folderHead + str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second)
	mkdir(path.join(path, folder))

def generate_video():
	chdir(path.join(path, folder))
	call([
		'ffmpeg', '-framerate', '8', '-i', 'file%02d.png', '-r', '30', '-pix_fmt', 'yuv420p',
		'fdtd_sim_video.mp4'
	])
	for file_name in glob("*.png"):
		remove(file_name)

def save_video(index = None):
	plt.savefig(path + "/" + folder + "/file%02d.png" % index)

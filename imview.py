import sys, os, fnmatch
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def func_gamma(x, gamma=0.05):
    y = x**gamma
    return np.nan_to_num(y)

def func_saturate(img, saturate=0.01):
    img = img.copy()
    h, edges = np.histogram(img, bins=10000)
    saturate = img.size * saturate
    i = -1
    total = h[-1]
    while total < saturate:
        i -= 1
        total += h[i]
    img[img >= edges[i]] = edges[i]  
    return img

def boost(img, saturate = 0.01, gamma = 0.05):
	# Clip (saturate-%) top pixels
	img = func_saturate(img, saturate=saturate)

	# Gamma compression
	# #Log
	# min_im = np.amin(img)
	# img = 1 + (img - min_im) / (np.amax(img) - min_im) * 10
	# return np.log(img)
	return func_gamma(img, gamma=gamma)

def read_fits_image(filename, hdu_index=0):
    try:
        hdulist = fits.open(filename)
        img_data = None
        while img_data is None:
            try:
                img_data = hdulist[hdu_index].data
                hdu_index += 1
            except IndexError:
                print("Could not find image data in file.")
                hdulist.close()
                sys.exit(1)
        hdulist.close()
        return img_data.astype(np.float64)
    except IOError:
        print("Could not read file:", filename)
        sys.exit(1)

def process(paths):
	#Get data
	process.cur_id = 0
	process.data = read_fits_image(paths[process.cur_id])

	#Setup plt
	process.inverse_mode = 1
	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.25, bottom=0.25)
	plt_im = plt.imshow(process.inverse_mode * boost(process.data), cmap = 'seismic')
	plt.colorbar()
	ax.margins(x=0)

	#Sliders
	axcolor = 'lightgoldenrodyellow'
	ax_satur = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
	ax_gamma = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
	s_satur = Slider(ax_satur, 'Saturate %', 0, 10, valinit=1, valstep=1)
	s_gamma = Slider(ax_gamma, 'Gamma', 0.001, 0.3, valinit=0.05)
	def update(val):
		print("Update: saturate=%d percent, gamma=%f"%(s_satur.val, s_gamma.val))
		boost_data = process.inverse_mode * boost(process.data, saturate=s_satur.val/100.0, gamma=s_gamma.val)
		plt_im.set_data(boost_data)
		plt_im.set_clim([boost_data.min(), boost_data.max()])
		fig.canvas.draw_idle()
	s_satur.on_changed(update)
	s_gamma.on_changed(update)

	#Buttons: reset, save, cmap
	resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
	reset_button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
	def reset(event):
		s_satur.reset()
		s_gamma.reset()
	reset_button.on_clicked(reset)

	saveax = plt.axes([0.65, 0.025, 0.1, 0.04])
	save_button = Button(saveax, 'Save', color=axcolor, hovercolor='0.975')
	def save(event):
		out_path = paths[process.cur_id].replace('.fits','_'+ radio.value_selected+'_plot.jpg')
		plt.savefig(out_path, bbox_inches='tight',transparent=True, pad_inches=0)
		print('saved ', out_path)
		out_path = paths[process.cur_id].replace('.fits','_'+ radio.value_selected+'.jpg')
		plt.imsave(out_path, process.inverse_mode * boost(process.data, saturate=s_satur.val/100.0, gamma=s_gamma.val), cmap=radio.value_selected)
	save_button.on_clicked(save)

	inverseax = plt.axes([0.525, 0.025, 0.1, 0.04])
	inverse_button = Button(inverseax, 'Inverse', color=axcolor, hovercolor='0.975')
	def inverse(event):
		process.inverse_mode = -process.inverse_mode		
		print('inverse_mode ', process.inverse_mode)
		update(None)
	inverse_button.on_clicked(inverse)

	prevax = plt.axes([0.25, 0.025, 0.1, 0.04])
	prev_button = Button(prevax, 'Prev', color=axcolor, hovercolor='0.975')

	def prev(event):
		process.cur_id = (process.cur_id - 1) if process.cur_id > 0 else process.cur_id		
		print('Back to ... %d/%d: %s'%(process.cur_id, len(paths),paths[process.cur_id]))
		process.data = read_fits_image(paths[process.cur_id])
		update(None)
	prev_button.on_clicked(prev)

	nextax = plt.axes([0.4, 0.025, 0.1, 0.04])
	next_button = Button(nextax, 'Next', color=axcolor, hovercolor='0.975')
	def next(event):
		process.cur_id = (process.cur_id + 1) if (process.cur_id + 1) < len(paths) else process.cur_id
		print('Next to ... %d/%d: %s'%(process.cur_id, len(paths), paths[process.cur_id]))
		process.data = read_fits_image(paths[process.cur_id])
		update(None)
	next_button.on_clicked(next)

	rax = plt.axes([0.025, 0.5, 0.15, 0.20], facecolor=axcolor)
	radio = RadioButtons(rax, ('gray', 'seismic'), active=1)
	def colorfunc(label):
	    plt_im.set_cmap(label)
	    fig.canvas.draw_idle()
	radio.on_clicked(colorfunc)

	plt.show()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('Usage: python imview.py <img.fits> OR <imgs_dir>')
	else:
		path = sys.argv[1]
		if os.path.isdir(path):
			paths = list(sorted(fnmatch.filter(os.listdir(path), '*.fits')))
			paths = [os.path.join(path, p) for p in paths]
		else:
			paths = [path]
		print(paths)
		process(paths)
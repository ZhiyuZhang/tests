from   astropy.io import fits
import montage_wrapper as montage

hstfile        = 'ibs401010_drz.fits'
hstimage       = fits.open(hstfile)[1]
hstheader      = hstimage.header

fits.writeto('output_file.fits', hstimage.data, hstheader, overwrite=True)

hstfile        = 'output_file.fits'
hstimage       = fits.open(hstfile)[0]
hstheader      = hstimage.header

montage.reproject('output_file.fits','hstnew.fits', north_aligned=True,exact_size=True)


       


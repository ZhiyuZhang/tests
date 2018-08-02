# - Zhiyu Zhang: pmozhang@gmail.com 
# 02 Aug. 2018
# Example:: 
# execfile('dyn_clean_function.py') 
# makemoms('abc.ms','velocity','abc.fits',2)
# -- there are so many options need to be implemented...
import os
import glob

def dynclean(visname,cleanmode,fitsname, smooth_level):

    img1          = 'dirty_image.img.image'
    img2          = 'clean_image.img.image'
    sm_img1       = 'dirty_image.sm.image'
    sm_sm_img1    = 'dirty_image.sm_sm.image'
    
    #----------------------------------------
    os.system("rm -rf dirty_image*")
    
    default(clean)
    
    clean( vis           = visname,
           imagename     = "dirty_image.img",
           uvrange       = "",
           mode          = cleanmode,
           niter         = 0,
           threshold     = "5mJy",
           psfmode       = 'hogbom',
           imagermode    = "csclean",
           interactive   = False, 
           mask          = "",
           nchan         = 50,
           start         = "200km/s",
           width         = "10km/s",
           imsize        = 500, 
           cell          = '0.02arcsec',
           restfreq      = "691.4730763GHz",
           weighting     = "briggs",
           robust        = 0.0,
           uvtaper       = False,
           outertaper    = [''],
           restoringbeam = [''],
           usescratch    = False)
    #----------------------------------------
    
    os.system("rm -rf dirty_image.sm*")
    
    ia.open(img1)
    
    beam     = ia.restoringbeam()
    maj      = beam['major']['value']
    mir      = beam['minor']['value']
    out_Beam = str(1.5 * max(maj,mir))+"arcsec"
    
    imsmooth(imagename=img1, outfile=sm_img1, kernel='gauss', major=out_Beam, minor=out_Beam, pa="0deg")  
    specsmooth(imagename=sm_img1, outfile=sm_sm_img1,  axis=3, dmethod="",function='hanning',overwrite=True)  
    
    up_cutoff = smooth_level * imstat(sm_sm_img1,box='0,0,150,150')['rms'][0]
    threshold = smooth_level * imstat(sm_sm_img1,box='0,0,150,150')['rms'][0]
    
    os.system("rm -rf sm_dirty_image.fits")
    exportfits(imagename=sm_img1,fitsimage='sm_dirty_image.fits',velocity=True)
    os.system("rm -rf  smsm_clean_image.fits")
    exportfits(imagename=sm_sm_img1,fitsimage='smsm_clean_image.fits',velocity=True)
    
    
    os.system("rm -rf mask*")
    ia.close()
    
    os.system("cp -r "+img1+" mask/")
    mask ="mask"
    
    ia.open(mask)
    ia.calcmask(mask=str(sm_sm_img1)+">"+str(up_cutoff),name='mask')
    ia.close()
    
    os.system("rm -rf mask_0")
    
    makemask( mode='expand', inpimage=mask, inpmask=mask+":"+"mask", output="mask_0", overwrite=True)
    
    exportfits(imagename='mask_0',fitsimage='mask_0.fits',velocity=True)
    
    
    #----------------------------------------
    default(clean)
    
    os.system("rm -rf clean_image*")
    
    clean( vis           = visname,
           imagename     = "clean_image.img",
           mode          = cleanmode,
           niter         = 5000,
           threshold     = threshold,
           psfmode       = 'hogbom',
           imagermode    = "csclean",
           interactive   = False,
           mask          = 'mask_0',
           nchan         = 50,
           start         = "200km/s",
           width         = "10km/s",
           imsize        = 500,
           cell          = '0.02arcsec',
           restfreq      = "691.4730763GHz",
           weighting     = "briggs",
           robust        = 0.0,
           uvtaper       = False,
           outertaper    = [''],
           restoringbeam = [''],
           usescratch    = False)
    
    
    #----------------------------------------
    fitsimage = fitsname
    
    exportfits(imagename=img2,fitsimage=fitsname,velocity=True)
    
    

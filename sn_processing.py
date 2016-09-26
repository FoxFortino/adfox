#Pre-processing class

from preprocessing import *
import matplotlib.pyplot as plt
from scipy.signal import medfilt



class PreProcessing(object):
    """ Pre-processes spectra for cross correlation """
    
    def __init__(self, filename, w0, w1, nw):
        self.filename = filename
        self.w0 = w0
        self.w1 = w1
        self.nw = nw
        self.numSplinePoints = 13
        self.readInputSpectra = ReadInputSpectra(self.filename, self.w0, self.w1)
        self.preProcess = PreProcessSpectrum(self.w0, self.w1, self.nw)

        self.spectrum = self.readInputSpectra.file_extension()


    def two_column_data(self, z, smooth):
        self.wave, self.flux = self.spectrum

        filterSize = int(len(self.wave)/self.nw) * smooth * 2 + 1
        preFiltered = medfilt(self.flux, kernel_size=filterSize)
        wave, flux = self.readInputSpectra.two_col_input_spectrum(self.wave, preFiltered, z)
        binnedwave, binnedflux, minindex, maxindex = self.preProcess.log_wavelength(wave, flux)
        newflux, continuum = self.preProcess.continuum_removal(binnedwave, binnedflux, self.numSplinePoints, minindex, maxindex)
        meanzero = self.preProcess.mean_zero(binnedwave, newflux, minindex, maxindex)
        apodized = self.preProcess.apodize(binnedwave, meanzero, minindex, maxindex)


        #filterSize = smooth * 2 + 1
        medianFiltered = medfilt(apodized, kernel_size=1)#filterSize)


        # from scipy.interpolate import interp1d
        #
        # plt.plot(self.flux)
        #
        # spline = interp1d(binnedwave[minindex:maxindex], binnedflux[minindex:maxindex], kind='cubic')
        # waveSpline = np.linspace(binnedwave[minindex],binnedwave[maxindex-1],num=13)
        # print spline
        # print '###'
        # print spline(binnedwave[minindex:maxindex])
        # plt.figure('1')
        # plt.plot(waveSpline, spline(waveSpline), '--', label='spline')
        #
        # print wave
        # print binnedwave
        # print binnedflux
        # print len(binnedwave)
        # plt.plot(wave,flux)
        # plt.figure('2')
        # plt.plot(binnedwave, binnedflux, label='binned')
        # plt.plot(binnedwave, newflux, label='continuumSubtract1')
        # plt.plot(binnedwave, continuum, label='polyfit1')
        # print len(binnedwave)
        # print (min(binnedwave), max(binnedwave))
        # print len(newflux)
        #
        # #newflux2, poly2 = self.preProcess.continuum_removal(binnedwave, binnedflux, 6, minindex, maxindex)
        # #plt.plot(binnedwave, newflux2, label='continuumSubtract2')
        # #plt.plot(binnedwave, poly2, label='polyfit2')
        # plt.plot(binnedwave, apodized, label='taper')
        # plt.legend()
        # plt.figure('filtered')
        # plt.plot(medianFiltered)
        # plt.figure('3')
        # plt.plot(medfilt(apodized,kernel_size=3))
        # plt.show()

        return binnedwave, medianFiltered, minindex, maxindex

    def snid_template_data(self, ageidx, z):
        """lnw templates """
        wave, fluxes, ncols, ages, ttype = self.spectrum
        wave, flux = self.readInputSpectra.snid_template_spectra(wave, fluxes[ageidx], z)
        binnedwave, binnedflux, minindex, maxindex = self.preProcess.log_wavelength(wave, flux)
        medianFiltered = medfilt(binnedflux, kernel_size=3)

        return binnedwave, medianFiltered, ncols, ages, ttype, minindex, maxindex

if __name__ == '__main__':
    f = '/home/dan/Desktop/SNClassifying_Pre-alpha/templates/superfit_templates/sne/Ia/sn1999ee.p03.dat'
    pre = PreProcessing(f, 2500, 10000, 1024)
    pre.two_column_data(0, 0)


"""
Created on Tue Apr 05 19:27:29 2016

Copyright 2016 Daniel Uhl

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@author: daniel
"""
import numpy as np
from scipy.signal import butter, lfilter, hilbert, cheby1, sosfilt


def cheb_bandpass_filter(data, cutoff, sampling_frequency, order=12):
    """ This functions filters the data with a Chebyshev 1 bandpass filter.
    input:
    data -- numpy.array - containing the data.
    cutoff -- list or tuple - with the cutoff frequencies of the bandpass
        filter in Hz.
    fs -- sampling frequency in Hz.
    order -- order of the Chebyshev 1 filert.
    output:
    data -- numpy.array - filtered data
    """
    nyq = 0.5 * sampling_frequency
    filtered = sosfilt(cheby1(12, 1, cutoff[0]/nyq, 'hp', output='sos'), data)
    return sosfilt(cheby1(12, 1, cutoff[1]/nyq, 'lp', output='sos'), filtered)


def butter_lowpass(cutoff, sampling_frequency, order):
    """ This function calculates the parameter for the butterworth
    lowpass filter.
    input:
    cutoff -- double - cutoff frequency of the lowpass filter in Hz
    sampling_frequency -- double - sampling frequency in Hz
    order -- int - order of the butterworth lowpass filert
    return:
    butter -- tuple - butterworth lowpass parameter
    """
    nyq = 0.5 * sampling_frequency
    norm_cutoff = cutoff / nyq
    return butter(order, norm_cutoff, btype='low', analog=False)


def butter_lowpass_filter(data, cutoff, sampling_frequency, order=2):
    """ This functions filters the data with a butterworth lowpass filter.
    input:
    data -- numpy.array with data
    cutoff -- cutoff frequency of the lowpass filter in Hz
    fs -- sampling frequency in Hz
    order -- order of the butterworth lowpass filert
    output:
    data -- numpy.array - filtered data
    """
    b, a = butter_lowpass(cutoff, sampling_frequency, order=order)
    return lfilter(b, a, data)


def butter_highpass(cutoff, sampling_frequency, order):
    """ This function calculates the parameter for the butterworth
    highpass filter.
    input:
    cutoff -- double - cutoff frequency of the lowpass filter in Hz
    sampling_frequency -- double - sampling frequency in Hz
    order -- int - order of the butterworth lowpass filert
    return:
    butter -- parameter of butterworth highpass
    """
    nyq = 0.5 * sampling_frequency
    norm_cutoff = cutoff / nyq
    return butter(order, norm_cutoff, btype='high', analog=False)


def butter_highpass_filter(data, cutoff, sampling_frequency, order):
    """ This functions filters the data with a butterworth highpass filter.
    input:
    data -- numpy.array - data to be filtered
    cutoff -- double - cutoff frequency of the lowpass filter in Hz
    sampling_frequency -- double - sampling frequency in Hz
    order -- int - order of the butterworth highpass filert
    output:
    data -- numpy.array of filtered data
    """
    b, a = butter_highpass(cutoff, sampling_frequency, order=order)
    return lfilter(b, a, data)


def butter_bandpass_filter(data, low_cutoff, high_cutoff,
                           sampling_frequency, order=2):
    """ This functions filters the data with a butterworth highpass filter.
    input:
    data -- numpy.array - data to be filtered
    cutoff -- double - cutoff frequency of the lowpass filter in Hz
    sampling_frequency -- double - sampling frequency in Hz
    order -- int - order of the butterworth highpass filter
    output:
    data -- numpy.array - filtered data
    """
    data = butter_highpass_filter(data, high_cutoff,
                                  sampling_frequency, order=order)
    return butter_lowpass_filter(data, low_cutoff,
                                 sampling_frequency, order=order)


class ULIA:
    """ Universal Lock-In amplifier

    Attributes
    ----------
    + TODO ;)
    """

    def __init__(self, data_size, sampling_frequency,
                 integration_time, order, bandwidth):
        """ Software based lock-in amplifier algorithm.
        data_size -- double - size of modulated datasets
        sampling_frequency -- double - sampling frequency in Hz
        integration_time -- double - integration time of the lowpass filter
        order -- int - order of the butterworth highpass filter
        average -- boolean - if true the lowpass filter is replaced by a simple
                             average function.
        bandwidth -- bandwidth of the phase locked loop
        """
        self._data_size = data_size
        self.signal = np.zeros(self._data_size)
        self.reference = np.zeros(self._data_size, dtype=np.complex128)
        # lia output data arrays
        self.x = np.zeros(self._data_size)
        self.y = np.zeros(self._data_size)
        # pll data arrays
        self.afreq = np.ones(self._data_size)
        self.aphase = np.zeros(self._data_size)
        self.avco = np.zeros(self._data_size, dtype=np.complex128)
        self._sampling_frequency = sampling_frequency
        self._integration_time = integration_time
        self._order = order
        self._harmonic = 1
        self._cutoff = 1./self._integration_time
        self._b, self._a = butter(
            self._order, self._cutoff / (0.5 * self._sampling_frequency),
            btype='low', analog=False)
        # pll variables
        self._bandwidth = bandwidth
        self._beta = np.sqrt(self._bandwidth)

    def butter_lowpass(self, cutoff, sampling_frequency, order):
        """ This function calculates the parameter for the butterworth
        lowpass filter.
        input:
        cutoff -- double - cutoff frequency of the lowpass filter in Hz
        sampling_frequency -- double - sampling frequency in Hz
        order -- int - order of the butterworth lowpass filert
        return:
        butter -- tuple - butterworth lowpass parameter
        """
        self._b, self._a = butter(
            self._order, self._cutoff / (0.5 * self._sampling_frequency),
            btype='low', analog=False)

    def lock_in(self):
        """ This functions filters the data with a butterworth lowpass filter.
        """
        if self._harmonic == 1:
            self.x[:] = lfilter(self._b, self._a,
                                np.real(self.avco)*self.signal)
            self.y[:] = lfilter(self._b, self._a,
                                np.imag(self.avco)*self.signal)
        else:
            reference = np.exp(1j * self._harmonic * self.aphase)
            self.x[:] = lfilter(self._b, self._a,
                                np.real(reference)*self.signal)
            self.y[:] = lfilter(self._b, self._a,
                                np.imag(reference)*self.signal)

    def phase_locked_loop(self):
        """ Phase locked loop function. For every point the phase difference of
        as generated oscillator and the incoming signal is calculated. The
        phase is then corrected on the oscillator.
        signal_in -- numpy.array - complex input signal
        bandwidth -- double - bandwidth of the phase locked loop
        """
        # phase locked for loop ;)
        for i in np.arange(1, self._data_size):
            phase_diff = np.angle(
                        self.reference[i-1] * np.conj(self.avco[i-1]))
            self.afreq[i] = self.afreq[i-1] + self._bandwidth * phase_diff
            self.aphase[i] = self.aphase[i-1] + self._beta * phase_diff + \
                self.afreq[i]
            self.avco[i] = np.exp(1j * self.aphase[i])

    def load_data(self, reference, signal):
        """ Load data into data arrays
        """
        self.reference[:] = hilbert(reference)
        self.signal[:] = signal

    def execute(self, harmonic=1):
        """ Execute the lock-in Algorithm

        """
        self._harmonic = harmonic
        self.phase_locked_loop()
        self.lock_in()

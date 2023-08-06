# -----------------------------------------------------------------------------
# Description:    Contains function to generate most basic waveforms.
#                 These functions are intened to be used to generate waveforms defined in the :mod:`.pulse_library`.
#                 Examples of waveforms that are too advanced are flux pulses that require knowledge of the flux
#                 sensitivity and interaction strengths and qubit frequencies.
# Repository:     https://gitlab.com/quantify-os/quantify-scheduler
# Copyright (C) Qblox BV & Orange Quantum Systems Holding BV (2020-2021)
# -----------------------------------------------------------------------------
import numpy as np
from scipy import signal


def square(t, amp):
    return amp*np.ones(len(t))


def ramp(t, amp):
    return np.linspace(0, amp, len(t))


def soft_square(t, amp):
    sq = square(t, amp)
    window = signal.windows.hann(int(len(t) / 2))
    return signal.convolve(sq, window, mode='same') / sum(window)


def drag(t,
         G_amp: float,
         D_amp: float,
         duration: float,
         nr_sigma: int = 3,
         phase: float = 0,
         subtract_offset: str = 'average'):
    """
    Generates a DRAG pulse consisting of a Gaussian :math:`G` as the I- and a Derivative :math:`D` as the Q-component.

    All inputs are in s and Hz.
    phases are in degree.

    :math:`G(t) = G_{amp} e^{- \\frac{(t-\\mu)^2}{2\\sigma^2}}`.

    :math:`D(t) = -D_{amp} \\frac{(t-\\mu)}{\\sigma} G(t)`.

    .. note:

        One would expect a factor :math:`1/\\sigma^2` in the prefactor of :math:`1/\\sigma^2`, we absorb this
        in the scaling factor :math:`D_{amp}` to ensure the derivative component is scale invariant with the duration of
        the pulse.


    Parameters
    ----------
    t : :class:`numpy.ndarray`
        times at which to evaluate the function
    G_amp : float
        Amplitude of the Gaussian envelope.
    D_amp : float
        Amplitude of the derivative component, the DRAG-pulse parameter.
    duration : float
        Duration of the pulse in seconds.
    nr_sigma : int
        After how many sigma the Gaussian is cut off.
    phase : float
        Phase of the pulse in degrees.
    subtract_offset : str
        Instruction on how to subtract the offset in order to avoid jumps in the waveform due to the cut-off.

            - 'average': subtract the average of the first and last point.
            - 'first': subtract the value of the waveform at the first sample.
            - 'last': subtract the value of the waveform at the last sample.
            - 'none', None: don't subtract any offset.
    Returns
    ----------
    :class:`numpy.ndarray`
        complex waveform


    References
    ----------
        1. |citation1|_

        .. _citation1: https://link.aps.org/doi/10.1103/PhysRevA.83.012308

        .. |citation1| replace:: *Gambetta, J. M., Motzoi, F., Merkel, S. T. & Wilhelm, F. K.
           Analytic control methods for high-fidelity unitary operations
           in a weakly nonlinear oscillator. Phys. Rev. A 83, 012308 (2011).*

        2. |citation2|_

        .. _citation2: https://link.aps.org/doi/10.1103/PhysRevLett.103.110501

        .. |citation2| replace:: *F. Motzoi, J. M. Gambetta, P. Rebentrost, and F. K. Wilhelm
           Phys. Rev. Lett. 103, 110501 (2009).*
    """
    mu = t[0] + duration/2

    sigma = duration/(2*nr_sigma)

    gauss_env = G_amp*np.exp(-(0.5 * ((t-mu)**2) / sigma**2))
    deriv_gauss_env = - D_amp * (t-mu)/(sigma**1) * gauss_env

    # Subtract offsets
    if subtract_offset.lower() == 'none' or subtract_offset is None:
        # Do not subtract offset
        pass
    elif subtract_offset.lower() == 'average':
        gauss_env -= (gauss_env[0]+gauss_env[-1])/2.
        deriv_gauss_env -= (deriv_gauss_env[0]+deriv_gauss_env[-1])/2.
    elif subtract_offset.lower() == 'first':
        gauss_env -= gauss_env[0]
        deriv_gauss_env -= deriv_gauss_env[0]
    elif subtract_offset.lower() == 'last':
        gauss_env -= gauss_env[-1]
        deriv_gauss_env -= deriv_gauss_env[-1]
    else:
        raise ValueError(
            'Unknown value "{}" for keyword argument subtract_offset".'.format(subtract_offset))

    # generate pulses
    drag_wave = gauss_env + 1j * deriv_gauss_env

    # Apply phase rotation
    rot_drag_wave = rotate_wave(drag_wave, phase=phase)

    return rot_drag_wave


def rotate_wave(wave, phase: float):
    """
    Rotate a wave in the complex plane.

    Parameters
    -------------
    wave : :py:class:`numpy.ndarray`
        complex waveform, real component corresponds to I, imag component to Q.
    phase : float
        rotation angle in degrees

    Returns
    -----------
    rot_wave : :class:`numpy.ndarray`
        rotated waveform.
    rot_Q : :class:`numpy.ndarray`
        rotated quadrature component of the waveform.
    """
    angle = np.deg2rad(phase)

    rot_I = np.cos(angle)*wave.real - np.sin(angle)*wave.imag
    rot_Q = np.sin(angle)*wave.real + np.cos(angle)*wave.imag
    return rot_I + 1j * rot_Q


def modulate_wave(t, wave, freq_mod):
    """
    Apply single sideband (SSB) modulation to a waveform.

    The frequency convention we adhere to is:

        freq_base + freq_mod = freq_signal

    Parameters
    ------------
    t : :py:class:`numpy.ndarray`
        times at which to determine the modulation.
    wave : :py:class:`numpy.ndarray`
        complex waveform, real component corresponds to I, imag component to Q.
    freq_mod: float
        modulation frequency in Hz.


    Returns
    -----------
    mod_wave : :py:class:`numpy.ndarray`
        modulated waveform.


    .. note::

        Pulse modulation is generally not included when specifying waveform envelopes
        as there are many hardware backends include this capability.
    """
    cos_mod = np.cos(2*np.pi*freq_mod*t)
    sin_mod = np.sin(2*np.pi*freq_mod*t)
    mod_I = cos_mod*wave.real + sin_mod*wave.imag
    mod_Q = - sin_mod*wave.real + cos_mod*wave.imag

    return mod_I + 1j*mod_Q

# -*- coding: utf-8 -*-
from numpy import mean, hanning, linspace, where, isclose, apply_along_axis
from numpy.fft import (
    fft,
    fftshift,
    ifft,
    ifftshift,
    rfftn,
    irfftn,
    fftn,
    ifftn,
    rfftfreq,
)
from numpy import (
    array,
    pi,
    zeros,
    exp,
    iscomplex,
    concatenate,
    conjugate,
    flip,
    append,
    take,
    insert,
    delete,
    abs as np_abs,
    angle as np_angle,
    nan_to_num,
    meshgrid,
    linalg,
    argmin,
    real,
)


def comp_fft_freqs(time, is_time, is_real):
    """Computes the frequency/wavenumber vector from the time/space vector
    Parameters
    ----------
    time: array
        Time or space vector
    is_time: bool
        Boolean indicating if we input time or space
    Returns
    -------
    Frequency/wavenumber vector
    """
    N_tot = time.size  # Number of samples
    if N_tot == 1:
        freqs = [0]
    else:
        # zero-padding
        # N_tot = int(2**(log(N_tot)//log(2)+1))
        timestep = float(time[1] - time[0])  # Sample step
        fsampt = 1.0 / timestep  # Sample frequency
        freqscale = N_tot / fsampt
        freqs = [i - int(N_tot / 2) for i in range(int(N_tot))]
        if is_real and is_time:
            # freqs = rfftfreq(N_tot, 1/(N_tot*fsampt))
            freqs = [i for i in range(int(N_tot / 2) + 1)]
            # freqs.append(-freqs[0])
        if is_time:
            freqs = [i / freqscale for i in freqs]
    return freqs


def comp_fft_time(freqs, is_angle, is_real):
    """Computes the time/space vector from the frequency/wavenumber vector
    Parameters
    ----------
    freqs: array
        Frequency or wavenumber vector
    is_angle: bool
        Boolean indicating if we output angle or time
    Returns
    -------
    Time/space vector
    """
    if freqs.size == 1:
        time = [0]
    else:
        if is_real and not is_angle:
            N_tot = 2 * (len(freqs) - 1)  # Number of samples
            fs = freqs[-1] / (N_tot)
        else:
            N_tot = len(freqs)  # Number of samples
            fs = freqs[-1] / (N_tot - 2)
        tf = 1 / (fs * 2)
        time = linspace(0, tf, N_tot, endpoint=False)
        # fsampt = freqs[-1] * 2.0
        # timestep = 1.0 / fsampt
        if is_angle:
            time *= 2.0 * pi
            # timestep *= 2.0 * pi
        # time = [0 + i * timestep for i in range(N_tot)]
    return time.tolist()


# def comp_nthoctave_axis(noct, freqmin, freqmax):
#     """Computes the frequency vector between freqmin and freqmax for the 1/n octave
#     Parameters
#     ----------
#     noct: int
#         kind of octave band (1/3, etc)
#     freqmin: float
#         minimum frequency
#     freqmax: float
#         maximum frequency
#     Returns
#     -------
#     Frequency vector
#     """
#     if noct == 3:
#         table = [
#             10,
#             12.5,
#             16,
#             20,
#             25,
#             31.5,
#             40,
#             50,
#             63,
#             80,
#             100,
#             125,
#             160,
#             200,
#             250,
#             315,
#             400,
#             500,
#             630,
#             800,
#             1000,
#             1250,
#             1600,
#             2000,
#             2500,
#             3150,
#             4000,
#             5000,
#             6300,
#             8000,
#             10000,
#             12500,
#             16000,
#             20000,
#         ]
#         f_oct = [f for f in table if (f >= freqmin and f <= freqmax)]
#     else:
#         f0 = 1000
#         f_oct = [f0]
#         i = 1
#         while f_oct[-1] <= freqmax:
#             f_oct.append(f0 * 2.0 ** (i / noct))
#             i = i + 1
#         f_oct = f_oct[:-2]
#         i = -1
#         while f_oct[0] > freqmin:
#             f_oct.insert(0, f0 * 2.0 ** (i / noct))
#             i = i - 1
#         f_oct = f_oct[1:]
#     return f_oct


# def _comp_fft(values, is_positive=False):
#     """Computes the Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the field
#     Returns
#     -------
#     Complex Fourier Transform
#     """
#     values_FT = fft(values)
#     if is_positive:
#         if iscomplex(values).any():
#             print("WARNING: keeping only positive harmonics from complex raw data")
#         values_FT[0] *= 0.5
#         values_FT = 2.0 * fftshift(values_FT) / len(values)
#         if len(values) % 2 == 0:
#             values_FT = append(values_FT, conjugate(values_FT[0]))
#     else:
#         values_FT = fftshift(values_FT) / len(values)
#     return values_FT


def comp_fftn(values, axes_list, is_real=True):
    """Computes the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Complex Fourier Transform
    """

    axes = []
    shape = []
    is_onereal = False
    for axis in axes_list:
        if axis.transform == "fft":
            if is_real and axis.name == "freqs":
                axes.append(axis.index)
                shape.append(values.shape[axis.index])
                is_onereal = True
            else:
                axes = [axis.index] + axes
                shape = [values.shape[axis.index]] + shape
                # is_positive = False
            # values = apply_along_axis(
            #     _comp_fft, axis.index, values, is_positive=is_positive
            # )
    size = array(shape).prod()
    if is_onereal:
        values_FT = rfftn(values, axes=axes)
        slice_0 = take(values_FT, 0, axis=axes[-1])
        slice_0 *= 0.5
        other_values = delete(values_FT, 0, axis=axes[-1])
        values_FT = insert(other_values, 0, slice_0, axis=axes[-1])
        values_FT2 = 2.0 * fftshift(values_FT, axes=axes[:-1]) / size
    else:
        values_FT = fftn(values, axes=axes)
        values_FT2 = fftshift(values_FT, axes=axes) / size
    return values_FT2


# def _comp_ifft(values, is_positive=False):
#     """Computes the Inverse Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the FT
#     Returns
#     -------
#     IFT
#     """

#     if is_positive:
#         values[0] *= 2
#         values = concatenate((flip(conjugate(values))[:-1], values))[:-1]
#         values = values / 2
#         values = ifftshift(values) * len(values)
#     else:
#         values = ifftshift(values) * len(values)
#     values_IFT = ifft(values)
#     return values_IFT


def comp_ifftn(values, axes_list, is_real=True):
    """Computes the Inverse Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the FT
    Returns
    -------
    IFT
    """

    axes = []
    shape = []
    is_onereal = False
    for axis in axes_list:
        if axis.transform == "ifft":
            if is_real and axis.name == "time":
                axes.append(axis.index)
                shape.append(2 * (values.shape[axis.index] - 1))
                is_onereal = True
            else:
                axes = [axis.index] + axes
                shape = [values.shape[axis.index]] + shape
                # is_positive = False
            # values = apply_along_axis(
            #     _comp_ifft, axis.index, values, is_positive=is_positive
            # )
    size = array(shape).prod()
    if is_onereal:
        values = values * size / 2
        values_shift = ifftshift(values, axes=axes[:-1])
        slice_0 = take(values_shift, 0, axis=axes[-1])
        slice_0 *= 2
        other_values = delete(values_shift, 0, axis=axes[-1])
        values = insert(other_values, 0, slice_0, axis=axes[-1])
        # values = ifftshift(values/2, axes=axes[:-1]) * size
        # values_IFT = irfftn(values, s=shape, axes=axes)
        values_IFT = irfftn(values, axes=axes)
    else:
        values_shift = ifftshift(values, axes=axes) * size
        values_IFT = ifftn(values_shift, axes=axes)
    return values_IFT


def comp_magnitude(values):
    """Computes the magnitude of the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Magnitude of the Fourier Transform
    """
    return np_abs(_comp_fft(values))


#    return np_abs(comp_stft_average(values))
def comp_phase(values):
    """Computes the phase of the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Phase of the Fourier Transform
    """
    return np_angle(_comp_fft(values))


def comp_stft_average(values):
    """Computes the average of the Short-Time Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Average of the Short-Time Fourier Transform
    """
    # To do
    nperseg = 3200
    noverlap = int(nperseg * 0.75)
    f, t, Zxx = stft(
        values, fs=48000, window="hann", nperseg=nperseg, noverlap=noverlap
    )
    window_size = nperseg / len(values)
    values = mean(Zxx, axis=1) / (0.5)
    #    values = 2.0 * mean(Zxx, axis=1)
    print(values.shape)
    return f, np_abs(values)


def comp_fft_average(values):
    """Computes the average of the Short-Time Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Average of the Short-Time Fourier Transform
    """
    # To do
    nperseg = 3200
    noverlap = int(nperseg * 0.75)
    step = nperseg - noverlap
    N_tot = len(values)
    nwindows = int(N_tot / (2.0 * step))
    values_fft = zeros(nperseg, dtype="complex128")
    for i in range(nwindows):
        values_fft += _comp_fft(
            values[i * step : nperseg + i * step] * hanning(nperseg)
        )
    values = values_fft[int(nperseg / 2) :] / nwindows
    f = linspace(0, int(N_tot / 2), int(nperseg / 2))
    return f, np_abs(values)


def rect_window(f, M, dt):
    W = where(
        exp(-1j * 2 * pi * dt * f * (M)) != 1,
        (1 - exp(-1j * 2 * pi * dt * f * (M))) / (M * (1 - exp(-1j * 2 * pi * dt * f))),
        1,
    )
    # W = (1 - exp(-1j * 2 * pi * dt * f * (M))) / (M*(1 - exp(-1j * 2 * pi * dt * f)))
    # W = nan_to_num(W)
    return W


def correct_spectrum(time, freqs, freqs_th, values):
    M = len(time)
    dt = time[1] - time[0]
    (xfreqs2, xfreqs1) = meshgrid(freqs_th, freqs)
    Wmat = rect_window(xfreqs1 - xfreqs2, M, dt)
    values_corr, _, _, _ = linalg.lstsq(Wmat, values, rcond=-1)
    return values_corr


# from numpy import cos, union1d
# import matplotlib.pyplot as plt

# A0 = 5
# freq0 = 1000
# phi0 = 0.5

# A1 = 2
# freq1 = 10000
# phi1 = 0

# A2 = 3
# freq2 = 9000
# phi2 = 0

# freqs_th = [-freq1, -freq2, -freq0, freq0, freq2, freq1]

# # Case 1: good sampling
# M1 = 201
# tf1 = 1/freq0
# time1 = linspace(0,tf1,M1, endpoint=False)
# # A1 = 2
# # freq1 = 75
# # phi1 = 0
# y1 = A0*cos(2*pi*freq0*time1+phi0) + A1*cos(2*pi*freq1*time1+phi1) + A2*cos(2*pi*freq2*time1+phi2)
# freqs1 = comp_fft_freqs(time1, is_time=True, is_real=False)
# ft = fft(y1)
# ft[0] /= 2
# y_FT1 = 2*fftshift(ft) / M1
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs1,np_abs(y_FT1),width=300)
# plt.xlim(-20000, 20000)
# plt.title("Good sampling")
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.plot(time1, y1)

# # Case 2: bad sampling
# M2 = 200
# tf2 = 1/freq0 + 0.0001
# time2 = linspace(0,tf2,M2, endpoint=False)
# y2 = A0*cos(2*pi*freq0*time2+phi0) + A1*cos(2*pi*freq1*time2+phi1) + A2*cos(2*pi*freq2*time2+phi2)
# freqs2 = comp_fft_freqs(time2, is_time=True, is_real=False)
# ft = fft(y2)
# ft[0] /= 2
# y_FT2 = 2*fftshift(ft) / M2
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs2,np_abs(y_FT2),width=300)
# plt.xlim(-20000, 20000)
# plt.title("Bad sampling")
# # Correction
# y_corr2 = correct_spectrum(time2, freqs2, freqs_th, y_FT2)
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs_th,np_abs(y_corr2),width=300)
# plt.xlim(-20000, 20000)
# plt.title("Bad sampling corrected")

# # Case 3: bad sampling + f_max lower than freqs_th
# M3 = 17
# tf3 = 1/freq0 + 0.0001
# time3 = linspace(0,tf3,M3, endpoint=False)
# y3 = A0*cos(2*pi*freq0*time3+phi0) + A1*cos(2*pi*freq1*time3+phi1) + A2*cos(2*pi*freq2*time3+phi2)
# freqs3 = comp_fft_freqs(time3, is_time=True, is_real=False)
# ft = fft(y3)
# ft[0] /= 2
# y_FT3 = 2*fftshift(ft) / M3
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs3,np_abs(y_FT3),width=300)
# plt.xlim(-20000, 20000)
# plt.title("f_max < freqs_th")
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.plot(time3, y3)
# # Correction
# y_corr3 = correct_spectrum(time3, freqs3, freqs_th, y_FT3)
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs_th,np_abs(y_corr3),width=300)
# plt.xlim(-20000, 20000)
# plt.title("f_max < freqs_th corrected")

# # Aliasing correction
# deltat = time3[1] - time3[0]
# fsh = 1/deltat
# # freqs4a = union1d(array(freqs3[9:13]), fsh-array(freqs3[13:]))
# # freqs4b = flip(-freqs4a)
# # freqs4 = concatenate((freqs4b, array([0]), freqs4a))
# #%%
# freqs4 = freqs3.copy()
# for fth in freqs_th:
#     if fth < min(freqs3):
#         f = -fsh - fth
#         i = argmin(np_abs(f - array(freqs3)))
#         freqs4[i] = -fsh - freqs4[i]
#     elif fth > max(freqs3):
#         f = fsh - fth
#         i = argmin(np_abs(f - array(freqs3)))
#         freqs4[i] = fsh - freqs4[i]

# # y_FT4a = concatenate((y_FT3[8::2], y_FT3[9::2]))
# # y_FT4b = concatenate((y_FT3[8::2], y_FT3[9::2]))
# # freqs4 = concatenate(y_FT4b, y_FT4a)
# # y_FT4 = array([y_FT3[3],y_FT3[2],y_FT3[1],y_FT3[0],y_FT3[4],y_FT3[5],
# #                 y_FT3[6],y_FT3[7],y_FT3[8],y_FT3[9],y_FT3[10],y_FT3[11],y_FT3[12],
# #                 y_FT3[16],y_FT3[15],y_FT3[14],y_FT3[13]])
# y_FT4 = y_FT3
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs4,np_abs(y_FT4),width=300)
# plt.xlim(-20000, 20000)
# y_corr4 = correct_spectrum(time3, freqs4, freqs_th, y_FT4)
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs1,np_abs(y_FT1),width=300)
# plt.bar([f+100 for f in freqs_th],np_abs(y_corr2),width=300)
# plt.bar([f+200 for f in freqs_th],np_abs(y_corr3),width=300)
# plt.bar([f+300 for f in freqs_th],np_abs(y_corr4),width=300)
# plt.xlim(-20000, 20000)
# plt.legend(["Good sampling", "Bad sampling", "Aliasing", "Corrected"])

# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs4,np_abs(y_FT4),width=300)
# plt.xlim(-20000, 20000)
# y_corr4 = correct_spectrum(time3, freqs4, freqs_th, y_FT4)
# fig = plt.figure(constrained_layout=True, figsize=(10, 5))
# plt.bar(freqs1,real(y_FT1),width=300)
# plt.bar([f+100 for f in freqs_th],real(y_corr2),width=300)
# plt.bar([f+200 for f in freqs_th],real(y_corr3),width=300)
# plt.bar([f+300 for f in freqs_th],real(y_corr4),width=300)
# plt.xlim(-20000, 20000)
# plt.legend(["Good sampling", "Bad sampling", "Aliasing", "Corrected"])

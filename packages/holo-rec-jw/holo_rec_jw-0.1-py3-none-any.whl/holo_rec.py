import numpy as np

def reconstruction(batch_hologram, rec_distance, ref_wavelength, slm_pitch):
    batch_rec = []
    print(batch_hologram.shape[0])
    for i in range(batch_hologram.shape[0]):
        hologram = batch_hologram[i]
        hologram = hologram[:,:,0]
        Nr, Nc = hologram.shape
        print(Nr)
        print(Nc)
        d = -rec_distance
        Nr = np.linspace(0, Nr - 1, Nr) - Nr / 2
        Nc = np.linspace(0, Nc - 1, Nc) - Nc / 2
        k, l = np.meshgrid(Nc, Nr)
        factor = np.multiply(hologram, np.exp(-1j*np.pi/(ref_wavelength*d)*(np.multiply(k, k)*slm_pitch**2 + np.multiply(l, l)*slm_pitch**2)))
        print(factor.shape)
        reconstructed_field = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(factor)))  # Take inverse Fourier transform of the factor
        batch_rec = batch_rec + [reconstructed_field]
    return batch_rec    
 
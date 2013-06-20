"""
pyart.io.common
===============

Input/output routines common to many file formats.

.. autosummary::
    :toctree: generated/

    dms_to_d
    radar_coords_to_cart
    make_time_unit_str
    get_metadata

"""

import numpy as np


def dms_to_d(dms):
    """ Degrees, minutes, seconds to degrees """
    return dms[0] + (dms[1] + dms[2] / 60.0) / 60.0


# XXX move this to another module
def radar_coords_to_cart(rng, az, ele, debug=False):
    """
    Assumes standard atmosphere, ie R=4Re/3
    """
    Re = 6371.0 * 1000.0
    #h=(r^2 + (4Re/3)^2 + 2r(4Re/3)sin(ele))^1/2 -4Re/3
    #s=4Re/3arcsin(rcos(ele)/(4Re/3+h))
    p_r = 4.0 * Re / 3.0
    rm = rng * 1000.0
    z = (rm ** 2 + p_r ** 2 + 2.0 * rm * p_r *
         np.sin(ele * np.pi / 180.0)) ** 0.5 - p_r
    #arc length
    s = p_r * np.arcsin(rm * np.cos(ele * np.pi / 180.) / (p_r + z))
    if debug:
        print "Z=", z, "s=", s
    y = s * np.cos(az * np.pi / 180.0)
    x = s * np.sin(az * np.pi / 180.0)
    return x, y, z


# dictionary matching commonly found fields to their standard names
COMMON2STANDARD = {
    'DBZ_F': 'reflectivity_horizontal',
    'VEL_F': 'mean_doppler_velocity',
    'WIDTH_F': 'doppler_spectral_width',
    'ZDR_F': 'diff_reflectivity',
    'RHOHV_F': 'copol_coeff',
    'NCP_F': 'norm_coherent_power',
    'KDP_F': 'diff_phase',
    'PHIDP_F': 'dp_phase_shift',
    'VEL_COR': 'corrected_mean_doppler_velocity',
    'PHIDP_UNF': 'unfolded_dp_phase_shift',
    'KDP_SOB': 'recalculated_diff_phase',
    'DBZ_AC': 'attenuation_corrected_reflectivity_horizontal', }


def make_time_unit_str(dtobj):
    """ Return a time unit string from a datetime object. """
    return "seconds since " + dtobj.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_metadata(p):
    """ Return a dictionary of metadata for a given parameter, p. """
    return METADATA[p].copy()

# dictionary of standard metadata for various parameters
METADATA = {
    # metadata for radar fields, assuming a stationary platform
    'reflectivity_horizontal': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'equivalent_reflectivity_factor',
        'valid_max': 80.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'reflectivity_horizontal_filtered': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor_filtered',
        'long_name': 'equivalent_reflectivity_factor_filtered',
        'valid_max': 80.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'mean_doppler_velocity': {
        'units': 'meters_per_second',
        'standard_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'long_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'valid_max': 95.0,
        'valid_min': -95.0,
        'coordinates': 'elevation azimuth range'},

    'diff_phase': {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'specific_differential_phase_hv',
        'valid_max': 20.0,
        'valid_min': -10.0,
        'coordinates': 'elevation azimuth range'},

    'diff_reflectivity': {
        'units': 'dB',
        'standard_name': 'log_differential_reflectivity_hv',
        'long_name': 'log_differential_reflectivity_hv',
        'valid_max': 8.0,
        'valid_min': -6.0,
        'coordinates': 'elevation azimuth range'},

    'copol_coeff': {
        'units': 'ratio',
        'standard_name': 'cross_correlation_ratio_hv',
        'long_name': 'cross_correlation_ratio_hv',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'norm_coherent_power': {
        'units': 'ratio',
        'standard_name': 'signal_quality',
        'long_name': 'signal_quality',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'comment': 'Also know as Normalized Coherent Power',
        'coordinates': 'elevation azimuth range'},

    'doppler_spectral_width': {
        'units': 'meters_per_second',
        'standard_name': 'spectrum_width',
        'long_name': 'spectrum_width',
        'valid_max': 45.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'dp_phase_shift': {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'differential_phase_hv',
        'valid_max': 180.0,
        'valid_min': -180.0,
        'coordinates': 'elevation azimuth range'},

    'corrected_mean_doppler_velocity': {
        'units': 'meters_per_second',
        'standard_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'long_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'valid_max': 45.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'unfolded_dp_phase_shift': {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'differential_phase_hv',
        'valid_max': 480.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'attenuation_corrected_reflectivity_horizontal': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'equivalent_reflectivity_factor',
        'valid_max': 80.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'recalculated_diff_phase': {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'specific_differential_phase_hv',
        'valid_max': 20.0,
        'valid_min': -1.0,
        'least_significant_digit': 3},

    'DBZ_F': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'equivalent_reflectivity_factor',
        'valid_max': 80.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'VEL_F': {
        'units': 'meters_per_second',
        'standard_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'long_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'valid_max': 95.0,
        'valid_min': -95.0,
        'coordinates': 'elevation azimuth range'},

    'KDP_F': {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'specific_differential_phase_hv',
        'valid_max': 20.0,
        'valid_min': -10.0,
        'coordinates': 'elevation azimuth range'},

    'ZDR_F': {
        'units': 'dB',
        'standard_name': 'log_differential_reflectivity_hv',
        'long_name': 'log_differential_reflectivity_hv',
        'valid_max': 8.0,
        'valid_min': -6.0,
        'coordinates': 'elevation azimuth range'},

    'RHOHV_F': {
        'units': 'ratio',
        'standard_name': 'cross_correlation_ratio_hv',
        'long_name': 'cross_correlation_ratio_hv',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'NCP_F': {
        'units': 'ratio',
        'standard_name': 'signal_quality',
        'long_name': 'signal_quality',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'comment': 'Also know as Normalized Coherent Power',
        'coordinates': 'elevation azimuth range'},

    'WIDTH_F': {
        'units': 'meters_per_second',
        'standard_name': 'spectrum_width',
        'long_name': 'spectrum_width',
        'valid_max': 45.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'PHIDP_F': {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'differential_phase_hv',
        'valid_max': 180.0,
        'valid_min': -180.0,
        'coordinates': 'elevation azimuth range'},

    'VEL_COR': {
        'units': 'meters_per_second',
        'standard_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'long_name': (
            'radial_velocity_of_scatterers_away_from_instrument'),
        'valid_max': 45.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'PHIDP_UNF': {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'differential_phase_hv',
        'valid_max': 480.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'DBZ_AC': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'equivalent_reflectivity_factor',
        'valid_max': 80.0,
        'valid_min': -45.0,
        'coordinates': 'elevation azimuth range'},

    'KDP_SOB': {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'specific_differential_phase_hv',
        'valid_max': 20.0,
        'valid_min': -1.0,
        'coordinates': 'elevation azimuth range'},

    'SQI': {
        'units': 'ratio',
        'standard_name': 'signal_quality_index',
        'long_name': 'signal_quality_index',
        'valid_max': 1,
        'valid_min': 0,
        'coordinates': 'elevation azimuth range'},

    'default': {
        'units': 'undefined',
        'standard_name': 'default',
        'long_name': 'custom_variable',
        'valid_max': 1000,
        'valid_min': -1000,
        'coordinates': 'elevation azimuth range'},

    # metadata for radar attributes
    'azimuth': {
        'units': 'degrees',
        'standard_name': 'beam_azimuth_angle',
        'long_name': 'azimuth_angle_from_true_north',
        'axis': 'radial_azimuth_coordinate',
        'comment': 'Azimuth of antenna relative to true north'},

    'elevation': {
        'units': 'degrees',
        'standard_name': 'beam_elevation_angle',
        'long_name': 'elevation_angle_from_horizontal_plane',
        'axis': 'radial_elevation_coordinate',
        'comment': 'Elevation of antenna relative to the horizontal plane'},

    'range': {
        'units': 'meters',
        'standard_name': 'projection_range_coordinate',
        'long_name': 'range_to_measurement_volume',
        'axis': 'radial_range_coordinate',
        'spacing_is_constant': 'true',
        'comment': (
            'Coordinate variable for range. Range to center of each bin.')},

    'time': {
        'units': 'seconds',
        'standard_name': 'time',
        'long_name': 'time_in_seconds_since_volume_start',
        'calendar': 'gregorian',
        'comment': ('Coordinate variable for time. '
                    'Time at the center of each ray, in fractional seconds '
                    'since the global variable time_coverage_start')},

    'sweep_mode': {
        'units': 'unitless',
        'standard_name': 'sweep_mode',
        'long_name': 'sweep_mode',
        'comment': ('Options are: "sector", "coplane", "rhi", '
                    '"vertical_pointing", "idle", "azimuth_surveillance", '
                    '"elevation_surveillance", "sunscan", "pointing", '
                    '"manual_ppi", "manual_rhi"')},

    'sweep_number': {
        'units': 'count',
        'standard_name': 'sweep_number',
        'long_name': 'sweep_number'},

    # metadata for radar sweep information dictionaries
    'sweep_start_ray_index': {
        'long_name': 'index of first ray in sweep, 0-based',
        'units': 'count'},

    'sweep_end_ray_index': {
        'long_name': 'index of first ray in sweep, 0-based',
        'units': 'count'},

    'fixed_angle': {
        'long_name': 'target_angle_for_sweep',
        'units': 'degrees',
        'standard_name': 'target_fixed_angle'},

    # metadata for radar location dictionaries
    'latitude': {
        'standard_name': 'Latitude',
        'units': 'degrees_north'},

    'longitude': {
        'standard_name': 'Longitude',
        'units': 'degrees_east'},

    'altitude': {
        'standard_name': 'Altitude',
        'units': 'meters',
        'positive': 'up'},

    # metadata for instrument parameter dictionary
    'prt_mode': {
        'comments': ('Pulsing mode Options are: "fixed", "staggered", '
                     '"dual". Assumed "fixed" if missing.'),
        'meta_group': 'instrument_parameters'},

    'nyquist_velocity': {
        'units': 'meters_per_second',
        'comments': "Unambiguous velocity",
        'meta_group': 'instrument_parameters'},

    'prt': {
        'units': 'seconds',
        'comments': ("Pulse repetition time. For staggered prt, "
                     "also see prt_ratio."),
        'meta_group': 'instrument_parameters'},

    'unambiguous_range': {
        'units': 'meters',
        'comments': 'Unambiguous range',
        'meta_group': 'instrument_parameters'},

}

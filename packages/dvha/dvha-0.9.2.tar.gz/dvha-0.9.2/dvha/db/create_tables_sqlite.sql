CREATE TABLE IF NOT EXISTS Plans (mrn text, study_instance_uid text, birth_date date, age smallint, patient_sex char(1), sim_study_date date, physician varchar(50), tx_site varchar(50), rx_dose real, fxs int, patient_orientation varchar(3), plan_time_stamp timestamp, struct_time_stamp timestamp, dose_time_stamp timestamp, tps_manufacturer varchar(50), tps_software_name varchar(50), tps_software_version varchar(30), tx_modality varchar(30), tx_time time, total_mu real, dose_grid_res varchar(16), heterogeneity_correction varchar(30), baseline boolean, import_time_stamp timestamp, toxicity_grades text, protocol text, complexity real, ptv_cross_section_max real, ptv_cross_section_median real, ptv_spread_x real, ptv_spread_y real, ptv_spread_z real, ptv_surface_area real, ptv_volume real, ptv_max_dose real, ptv_min_dose real);
CREATE TABLE IF NOT EXISTS DVHs (mrn text, study_instance_uid text, institutional_roi varchar(50), physician_roi varchar(50), roi_name varchar(50), roi_type varchar(20), volume real, min_dose real, mean_dose real, max_dose real, dvh_string text, roi_coord_string text, dist_to_ptv_min real, dist_to_ptv_mean real, dist_to_ptv_median real, dist_to_ptv_max real, surface_area real, ptv_overlap real, import_time_stamp timestamp, centroid varchar(35), dist_to_ptv_centroids real, dth_string text, spread_x real, spread_y real, spread_z real, cross_section_max real, cross_section_median real, centroid_dist_to_iso_min real, centroid_dist_to_iso_max real, toxicity_grade smallint);
CREATE TABLE IF NOT EXISTS Beams (mrn text, study_instance_uid text, beam_number int, beam_name varchar(30), fx_grp_number smallint, fx_count int, fx_grp_beam_count smallint, beam_dose real, beam_mu real, radiation_type varchar(30), beam_energy_min real, beam_energy_max real, beam_type varchar(30), control_point_count int, gantry_start real, gantry_end real, gantry_rot_dir varchar(5), gantry_range real, gantry_min real, gantry_max real, collimator_start real, collimator_end real, collimator_rot_dir varchar(5), collimator_range real, collimator_min real, collimator_max real, couch_start real, couch_end real, couch_rot_dir varchar(5), couch_range real, couch_min real, couch_max real, beam_dose_pt varchar(35), isocenter varchar(35), ssd real, treatment_machine varchar(30), scan_mode varchar(30), scan_spot_count real, beam_mu_per_deg real, beam_mu_per_cp real, import_time_stamp timestamp, area_min real, area_mean real, area_median real, area_max real, x_perim_min real, x_perim_mean real, x_perim_median real, x_perim_max real, y_perim_min real, y_perim_mean real, y_perim_median real, y_perim_max real, complexity_min real, complexity_mean real, complexity_median real, complexity_max real, cp_mu_min real, cp_mu_mean real, cp_mu_median real, cp_mu_max real, complexity real, tx_modality varchar(30), perim_min real, perim_mean real, perim_median real, perim_max real);
CREATE TABLE IF NOT EXISTS Rxs (mrn text, study_instance_uid text, plan_name varchar(50), fx_grp_name varchar(30), fx_grp_number smallint, fx_grp_count smallint, fx_dose real, fxs smallint, rx_dose real, rx_percent real, normalization_method varchar(30), normalization_object varchar(30), import_time_stamp timestamp);
CREATE TABLE IF NOT EXISTS DICOM_Files (mrn text, study_instance_uid text, folder_path text, plan_file text, structure_file text, dose_file text, import_time_stamp timestamp);

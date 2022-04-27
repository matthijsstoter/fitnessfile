import pathlib
import os
from heartrate.heartrate import HeartRate

from trainingfile import readers, trainingfile
from heartrate.trimp import TRIMPEdwards, TRIMPMod, TRIMPBanister


main_dir = pathlib.Path(os.getcwd())
data_dir = main_dir / "data"

files: list[pathlib.Path] = [pathlib.Path(f) for f in os.listdir(data_dir) if f != ".DS_Store"]

for file in files:
    if file.suffix == ".fit":
        filepath = data_dir / file
        reader = readers.FitFileReader(filepath=filepath)
        tr_file = trainingfile.TrainingFile(reader=reader)
        tr_file.to_excel(data_dir / "exports.xlsx")
        hr = tr_file.heart_rate()

        hr = HeartRate(tr_file.data["heart_rate"])

        print(filepath)

        reader = readers.CSVFileReader(filepath)
        trainingfile.TrainingFile(reader)


        if type(hr) == HeartRate:

            hr_max = 200
            hr_min = 50


            # print(
            #     hr.compute_delta_hr_ratio(hr_max=hr_max, hr_rest=hr_min),
            # hr.compute_factor_based_trimp(trimp=TRIMPBanister(), hr_max=hr_max, hr_min=hr_min, gender="Male"),
            # hr.compute_delta_hr_ratio(hr_max=hr_max, hr_rest=hr_min),
            # hr.compute_heartrate_zones(hr_max=hr_max, zones=TRIMPEdwards().zones),
            # hr.compute_heartratereserve_zones(hr_max=hr_max, hr_min=hr_min, zones=TRIMPEdwards().zones),
            # hr.compute_percentage_heartrate_reserve(hr_max=hr_max, hr_min=hr_min),
            # hr.compute_percentage_heartrate_max(hr_max=hr_max))



    
    # if file.suffix == ".csv":
    #     filepath = data_dir / file
    #     reader = readers.CSVFileReader(filepath=filepath)
    #     tr_file = trainingfile.TrainingFile(reader=reader)
    #     hr = tr_file.heart_rate()

    #     print(hr)
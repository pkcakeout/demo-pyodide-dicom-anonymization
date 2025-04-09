import sys
import argparse

from dicomanonymizer import anonymize, keep, delete_or_empty_or_replace
from dicomanonymizer.dicom_anonymization_databases.dicomfields_2024b import ALL_TAGS, D_TAGS, Z_TAGS


def dicomanonymizer_main(in_file, out_file):
    deletePrivateTags = False

    input_dicom_path = in_file
    output_dicom_path = out_file

    extra_anonymization_rules = {}

    # Per https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html
    # it is all right to retain only the year part of the birth date for
    # de-identification purposes.
    def set_date_to_year(dataset, tag):
        element = dataset.get(tag)
        if element is not None:
            element.value = f"{element.value[:4]}0101" # YYYYMMDD format

    # ALL_TAGS variable is defined on file dicomfields.py
    # the 'keep' method is already defined into the dicom-anonymizer
    # It will overrides the default behaviour
    for i in D_TAGS + Z_TAGS:
        extra_anonymization_rules[i] = delete_or_empty_or_replace

    extra_anonymization_rules[(0x0010, 0x0030)] = set_date_to_year # Patient's Birth Date

    # Launch the anonymization
    anonymize(
        input_dicom_path,
        output_dicom_path,
        extra_anonymization_rules,
        delete_private_tags=True,
    )

def main():
    print("This platform is", sys.platform)

    import mymodule
    print("string_from_my_module:", mymodule.string_from_my_module)

    import os
    print("Contents of base directory:")
    for item in os.listdir("/"):
        s = os.stat(f"/{item}")
        print(f"{item} - {s.st_size} bytes")

    print("------- END -------")

    dicomanonymizer_main("/raw.dcm", "/output.dcm")

if __name__ == "__main__":
    main()
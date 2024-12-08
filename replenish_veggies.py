import os
from pathlib import Path

import argparse

from vegetable_classifier import identify_vegetables
from vegetable_price_detector import find_vegetables_and_prices

WORKSPACE = Path(os.environ.get("WORKSPACE", ""))


def main(img_fridge_contents: str, img_deals_flyer: str):
    img_fridge_contents_file_path = (WORKSPACE / img_fridge_contents).as_posix()
    print(f'[INFO] Refrigerator contents are captured in: "{img_fridge_contents_file_path}".')
    img_deals_flyer_file_path = (WORKSPACE / img_deals_flyer).as_posix()
    print(f'[INFO] Safeway specials are shown in this flyer: "{img_deals_flyer_file_path}".')

    print(f'[INFO] Scanning the refrigerator and classifying the vegetables...')
    vegetables_in_fridge = identify_vegetables(image_path=img_fridge_contents_file_path)
    vegetable_counts = vegetables_in_fridge["vegetable_counts"]
    print('[INFO] DONE (obtained vegerable counts).')

    print(f'[INFO] Scanning the Safeway flyer for specials on produce...')
    vegetable_deals = find_vegetables_and_prices(image_path=img_deals_flyer_file_path)
    print('[INFO] DONE (captured the Safeway specials).')
    # print(f'[DEBUG] VEGETABLE_COUNTS:\n{vegetable_counts}')
    # print(f'[DEBUG] VEGETABLE_DEALS:\n{vegetable_deals}')

    for veg, count in vegetable_counts.items():
        msg = f'You have {count} {veg} in your refrigerator.'
        if veg in vegetable_deals:
            msg += f'  SALE SPECIAL!!!  You can get more {veg} for {vegetable_deals[veg]} '
        else:
            msg += f'  There are no specials on {veg} '

        msg += f'at Safeway today.'

        print(msg)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Find deals on veggies in your fridge.")
    parser.add_argument("--img_fridge_contents", type=str, help="fridge contents photo file name in your workspace directory")
    parser.add_argument("--img_deals_flyer", type=str, help="grocery deals flyer photo file name in your workspace directory")

    # Parse arguments
    args = parser.parse_args()
    args_dict = vars(args)

    main(**args_dict)


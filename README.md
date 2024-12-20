
The progrem "Replenish Vegetables" uses the VisionAgent from LandingAI to locate the vegetables in the photo of a refrigerator,
then check the deals and specials on produce in the Safeway weekly specials flyer, and match which vegetables in the fridge are on sale.

## Description
The goal of this exercise was to use the VisionAgent to generate the Computer Vision (CV) Python code for the detection and classification tasks
(scanning the fridge) as well as the object capture and OCR task (items and prices in the flyer), and use these two separate algorithms to write an application.

For the present case, the VisionAgent was used twice: [classification/categorization](https://va.landing.ai/agent/gcrgkLJ) with the prompt:

Identify and classify the different types of vegetables visible in the refrigerator, such as lettuce, carrots, and tomatoes. Focus on recognizing each vegetable and categorizing them based on their type.

and [detection/OCR](https://va.landing.ai/agent/Y6Yb9m3) with the prompt:

Find vegetables in this image (e.g., lettuce, carrots, tomatoes, etc.) and record their prices. Return the results in JSON format.

The code for each sub-task is placed into their respective modules.  The main program (in "replenish_veggies.py") then imports those methods, executes them with the corresponding image files as the
arguments, and combines the outputs to suggest which produce items in the fridge are on sale at Safeway and at what price.

## Instructions

### Installation
Create a separate directory and install VisionAgent:

```bash
pip install vision-agent
```

Set up your WORKSPACE environment directory, where the media (e.g., the images) will be expected to be stored.

```bash
export WORKSPACE='/Users/alexsherstinsky/Development/LandingAIVisionAgentExample/alex_workspace_test_0'
```

The above is an example; please adapt to your own environment.

### Usage
Make sure that the two images supplied with this ZIP archive are located in your WORKSPACE directory, and execute:
```bash
python replenish_veggies.py --img_fridge_contents RefrigeratorContents11142024as01.png --img_deals_flyer SafewayFlyer11142024as0.png
```

in your shell.

Execute 
```bash
python replenish_veggies.py --help
```

to see the arguments/usage.

## Remarks
The code generated by the VisionAgent was modified slightly so as to improve the code robustness as well as to condition the output to fit the purposes of integrating the results into the overall application.


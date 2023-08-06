## About
This plugin will assist in writing better testcode. It will push you to follow best practices.

## Installation

`pip install pylint-unittest`

## Usage
You can easily load the plugin with the `--load-plugins` flag like below.

`pylint --load-plugins=pylint-unittest YOUR_MODULE.py`

## Checkers
Below an overview of the checkers that come with this plugin. 


| Name | Message | Type | Description |
| --- | --- | --- | --- |
| AssertionsChecker | Missing assertion(s) in test - (missing-assertion) | Warning (W9999) | Checks if test method includes 'Assert' keyword or any type of assertion expression (from unittest.TestCase) |
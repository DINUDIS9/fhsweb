from flask import Flask, render_template, request
from flask_cors import CORS
from fix_host_save import sav_to_json, apply_fix
import io
import struct
import uuid
from typing import Any, Callable, Optional, Union
import argparse
import ctypes
import re
import zlib

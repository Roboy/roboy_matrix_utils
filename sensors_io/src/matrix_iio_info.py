#!/usr/bin/env python

import iio
import pdb
import math
import time


contexts = iio.scan_contexts()
uri = next(iter(contexts), None)
ctx = iio.Context(uri)
for dev in ctx.devices:
	for chn in dev.channels:
		print('\t\t\t%s: %s (%s)' % (chn.id, chn.name or "", 'output' if chn.output else 'input'))

		if len(chn.attrs) != 0:
			print('\t\t\t%u channel-specific attributes found:' % len(chn.attrs))

		for attr in chn.attrs:
			try:
				print('\t\t\t\t' + attr + ', value: ' + chn.attrs[attr].value)
			except OSError as e:
				print('Unable to read ' + attr + ': ' + e.strerror)


# python spearmint_sync.py --method=GPEIChooser kin

import sys, subprocess, re
from math import exp

def get_validation_loss( data ):
	pattern = 'RMSE: ([0-9.]+)'
	matches = re.search( pattern, data )

	validation_loss = float( matches.group( 1 ))
	return validation_loss

def run_test( params ):

	#debug_o = open( 'debug', 'wb' )
	#print >> debug_o, params
	
	parameters = []
	for p in ['layers', 'noise']:
		parameter = str( params[p][0] )
		parameters.append( parameter )	
	
	#print >> debug_o, parameters

	data = subprocess.check_output( ['octave', '-qf', 'run_denoise.m'] + parameters )
	# TODO: assert
	
	data = subprocess.check_output( ['r', 'run_rf.r'] + parameters )
	validation_loss = get_validation_loss( data )

	print validation_loss
	return validation_loss

def main( job_id, params ):
	print 'Job id:', str( job_id )
	print params
	print "layers: %s" % ( params['layers'][0] )
	print "noise: %s" % ( params['noise'][0] )
	
	return run_test( params )

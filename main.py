from baseline import *
from mtpm import *

if __name__ == '__main__':

	print 'Running baseline...'
	r = run_baseline()
	acc1 = r.run(measure_type = 'rr')
	acc2 = r.run(measure_type = 'conf')
	acc3 = r.run(measure_type = 'lev')
	acc4 = r.run(measure_type = 'chi')

	print '----------------------------------------------'

	r = run_model()
	acc = r.run_mtpm(path = 'test_sample/*.txt', maxlength = 9)

	print '\n----------------------------------------\n'
	
	print 'Change top of selected pairs'
	r = run_baseline()
	y1 = r.topOfSelection(measure_type = 'conf', maxtop = 30)
	print 'baseline with conf', y1
	r = run_model()
	y2 = r.topOfSelection(path = 'test_sample/*.txt', length = 1, maxtop = 30)
	print 'MTPM, l = 1', y2
	y3 = r.topOfSelection(path = 'test_sample/*.txt', length = 2, maxtop = 30)
	print 'MTPM, l = 2', y3
	y4 = r.topOfSelection(path = 'test_sample/*.txt', length = 3, maxtop = 30)
	print 'MTPM, l = 3', y4
	y5 = r.topOfSelection(path = 'test_sample/*.txt', length = 4, maxtop = 30)
	print 'MTPM, l = 4', y5
	y6 = r.topOfSelection(path = 'test_sample/*.txt', length = 5, maxtop = 30)
	print 'MTPM, l = 5', y6
	y7 = r.topOfSelection(path = 'test_sample/*.txt', length = 6, maxtop = 30)
	print 'MTPM, l = 6', y7
	y8 = r.topOfSelection(path = 'test_sample/*.txt', length = 7, maxtop = 30)
	print 'MTPM, l = 7', y8
	y9 = r.topOfSelection(path = 'test_sample/*.txt', length = 8, maxtop = 30)
	print 'MTPM, l = 8', y9
	y10 = r.topOfSelection(path = 'test_sample/*.txt', length = 9, maxtop = 30)
	print 'MTPM, l = 9', y10


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
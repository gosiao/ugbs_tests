#!/usr/bin/env python

import sys, os
import re
import math
import argparse


# ------------------------------------------------------------------------------

class et_set_by_l():
    def __init__(self, allexp, gs_by_l, decrease, fname):
        self.allexp    = [float(x) for x in allexp]
        self.gs_by_l   = gs_by_l

        self.newexp        = []
        self.newexp_by_l   = {}
        self.newexp_ranges = {}

        self.decrease      = decrease
        self.newexp_fname  = fname
        
    def calc_with_decrease(self):
        self.newexp.clear()
        self.newexp_by_l.clear()
        self.newexp_ranges.clear()
        for k, v in self.gs_by_l.items():
            fl_v  = [float(x) for x in v]
            v_max = max(fl_v)
            v_min = min(fl_v)
            #print(k, v_min, v_max)
            self.newexp_ranges[k] = []
            self.newexp_by_l[k] = []
            if len(fl_v) == 1:
                # only 1 exponent in guiding set, so find the closest one from allexp:
                mindiff = v_min
                for ie_all, e_all in enumerate(self.allexp):
                    newdiff = abs(e_all - fl_v[0]) 
                    if newdiff < mindiff:
                        mindiff = newdiff
                        self.newexp_by_l[k]   = [e_all]
                        self.newexp_ranges[k] = ie_all
            else:
                for ie_all, e_all in enumerate(self.allexp):
                    #print(k, ie_all, e_all)
                    if (e_all > v_min and e_all < v_max):
                        #print(k, v_min, v_max, ie_all, e_all)
                        self.newexp_by_l[k].append(e_all)
                        self.newexp_ranges[k].append(ie_all)
        for k, v in self.newexp_by_l.items():
            if len(v) > 1:
                #print('{}: {}, {}'.format(k, v, self.newexp_ranges[k]))
                ##i = self.newexp_ranges[k]
                #i = self.newexp_ranges[k][0]
                #j = self.newexp_ranges[k][-1]
                ##print('k: {}, ind: {}'.format(k, i))
                #print('k: {}, min_end_ind: {}, max_end_ind: {}'.format(k, i, j))
                i1 = self.newexp_ranges[k][-1]+1
                i2 = self.newexp_ranges[k][0]-1
                #print('k: {}, min_end_ind: {}, max_end_ind: {}'.format(k, i1, i2))
                # add one more exp on each end:
                if (i2 >= 0):
                    self.newexp_by_l[k].insert(0, self.allexp[i2])
                    self.newexp_ranges[k].insert(0, i2)
                if (i1 <= len(self.allexp)):
                    self.newexp_by_l[k].append(self.allexp[i1])
                    self.newexp_ranges[k].append(i1)
        with open(self.newexp_fname, 'w') as f:
            for k, v in self.newexp_by_l.items():
                if len(v) > 1:
                    e_range=str(min(self.newexp_ranges[k])+1)+'..'+str(max(self.newexp_ranges[k])+1)
                    f.write('FINAL SET: {}: {}\n'.format(k, e_range))
                    for e in v:
                        f.write(' {:<10.8E}\n'.format(e))
                else:
                    e_range=str(self.newexp_ranges[k]+1)
                    f.write('FINAL SET: {}: {}\n'.format(k, e_range))
                    e = v[0]
                    f.write(' {:<10.8E}\n'.format(e))
            #for e in v:
            #    print('FINAL SET: {}: {:<10.8E}'.format(k, e))
        #return self.newexp_by_l

    def calc_with_increase(self):
        self.newexp.clear()
        self.newexp_by_l.clear()
        self.newexp_ranges.clear()
        for k, v in self.gs_by_l.items():
            fl_v  = [float(x) for x in v]
            v_max = max(fl_v)
            v_min = min(fl_v)
            #print(k, v_min, v_max)
            self.newexp_ranges[k] = []
            self.newexp_by_l[k] = []
            if len(fl_v) == 1:
                # only 1 exponent in guiding set, so find the closest one from allexp:
                mindiff = v_min
                for ie_all, e_all in enumerate(self.allexp):
                    newdiff = abs(e_all - fl_v[0]) 
                    if newdiff < mindiff:
                        mindiff = newdiff
                        self.newexp_by_l[k]   = [e_all]
                        self.newexp_ranges[k] = ie_all
            else:
                for ie_all, e_all in enumerate(self.allexp):
                    #print('HERE: ', k, ie_all, e_all)
                    if (e_all > v_min and e_all < v_max):
                        #print(k, v_min, v_max, ie_all, e_all)
                        self.newexp_by_l[k].append(e_all)
                        self.newexp_ranges[k].append(ie_all)
        for k, v in self.newexp_by_l.items():
            if len(v) > 1:
                #print('{}: {}, {}'.format(k, v, self.newexp_ranges[k]))
                i1 = self.newexp_ranges[k][-1]+1
                i2 = self.newexp_ranges[k][0]-1
                # add one more exp on each end:
                if (i2 >= 0):
                    self.newexp_by_l[k].insert(0, self.allexp[i2])
                    self.newexp_ranges[k].insert(0, i2)
                if (i1 <= len(self.allexp)):
                    self.newexp_by_l[k].append(self.allexp[i1])
                    self.newexp_ranges[k].append(i1)
        with open(self.newexp_fname, 'w') as f:
            for k, v in self.newexp_by_l.items():
                if len(v) > 1:
                    e_range=str(min(self.newexp_ranges[k])+1)+'..'+str(max(self.newexp_ranges[k])+1)
                    f.write('FINAL SET: {}: {}\n'.format(k, e_range))
                    for e in v:
                        f.write(' {:<10.8E}\n'.format(e))
                else:
                    e_range=str(self.newexp_ranges[k]+1)
                    f.write('FINAL SET: {}: {}\n'.format(k, e_range))
                    e = v[0]
                    f.write(' {:<10.8E}\n'.format(e))
        #return self.newexp_by_l


class et_set():
    def __init__(self, start_exp, zeta, N_exp, decrease, fname):
        self.start_exp = start_exp
        self.zeta      = zeta
        self.N_exp     = N_exp
        self.decrease  = decrease

        self.ratio     = 0.0
        self.newexp    = []
        self.newexp_fname = fname

    def calc_ratio(self):
        self.ratio = math.pow(10, 1/float(self.zeta))
        #print('beta = {}'.format(self.ratio))
        
    def calc_with_decrease(self):
        self.newexp.clear()
        if self.ratio == 0:
            self.calc_ratio()
        for i in range(self.N_exp):
            nexp = self.start_exp / math.pow(self.ratio, i)
            self.newexp.append(nexp)
            #print('{:<10.8E}'.format(nexp))
        with open(self.newexp_fname, 'w') as f:
            for i, e in enumerate(self.newexp):
                f.write('{}: {:<10.8E}\n'.format(i+1, e))
        return self.newexp

    def calc_with_increase(self):
        self.newexp.clear()
        if self.ratio == 0:
            self.calc_ratio()
        temp = []
        for i in range(self.N_exp):
            nexp = self.start_exp * math.pow(self.ratio, i)
            temp.append(nexp)
            #print('before reversing: {:<10.8E}'.format(nexp))
        self.newexp = [x for x in temp[::-1]]
        #for nexp in self.newexp:
        #    print('after reversing: {:<10.8E}'.format(nexp))
        with open(self.newexp_fname, 'w') as f:
            for i, e in enumerate(self.newexp):
                f.write('{}: {:<10.8E}\n'.format(i+1, e))
        return self.newexp

    def select_range(self):
        if self.newexp == []:
            sys.exit('first generate the full set of exponents')
        #else:
            # use 



#class guide_set(et_set):
class guide_set():

    def __init__(self):
        self.gsinp = main_parser()
        self.allexp_list      = []
        self.element_exp_list = []
        self.element_exp_list_by_l = {}
        self.element_Nexp_by_l = {}
        self.gsinp_file_unit  = 21
        self.max_of_gs = 0.0
        self.min_of_gs = 0.0
        self.max_of_elset = 0.0
        self.min_of_elset = 0.0
        print('Guide basis set taken from file {} in dir {}'.format(self.gsinp.guide_bs_fname, self.gsinp.guide_bs_dir))

    def get_allexp(self):
        fgs = os.path.join(self.gsinp.guide_bs_dir, self.gsinp.guide_bs_fname)
        self.allexp_list.clear()
        with open(fgs, 'r') as f:
            lines = f.readlines()
            for line in lines:
                fl = re.findall("[+-]?\d+\.\d+E[+-]\d+", line)
                if fl:
                    self.allexp_list.append(fl[0])
        #print('all exp list:', self.allexp_list)

    def get_max_of_gs(self):
        if not self.allexp_list:
            self.get_allexp()
        self.max_of_gs = max([float(x) for x in self.allexp_list])
        #print('maximum exponent is {}'.format(self.max_of_gs))
        return self.max_of_gs

    def get_min_of_gs(self):
        if not self.allexp_list:
            self.get_allexp()
        self.min_of_gs = min([float(x) for x in self.allexp_list])
        #print('minimum exponent is {}'.format(self.min_of_gs))
        return self.min_of_gs

    def get_gs_element(self):
        el_line = 'a '+self.gsinp.atom_number
        fgs = os.path.join(self.gsinp.guide_bs_dir, self.gsinp.guide_bs_fname)
        self.element_exp_list.clear()
        l1 = 0
        l2 = 0
        with open(fgs, 'r') as f:
            lines = f.readlines()
            for iline, line in enumerate(lines):
                if el_line in line:
                    #print('l1: ', line)
                    l1 = iline
                    for jline, line in enumerate(lines[l1+1:]):
                        if 'a ' in line:
                            #print('l2: ', line)
                            l2 = l1+jline
                            break
            for line in lines[l1:l2]:
                #print('our line: ', line)
                fl = re.findall("[+-]?\d+\.\d+E[+-]\d+", line)
                if fl:
                    self.element_exp_list.append(fl[0])
        return self.element_exp_list

    def get_max_of_elset(self):
        if not self.element_exp_list:
            self.get_gs_element()
        self.max_of_elset = max([float(x) for x in self.element_exp_list])
        #print('maximum exponent is {}'.format(self.max_of_elset))
        return self.max_of_elset

    def get_min_of_elset(self):
        if not self.element_exp_list:
            self.get_gs_element()
        self.min_of_elset = min([float(x) for x in self.element_exp_list])
        #print('minimum exponent is {}'.format(self.min_of_elset))
        return self.min_of_elset

    def get_gs_element_by_l(self):
        #if not self.element_exp_list:
        #    self.get_gs_element()
        el_line = 'a '+self.gsinp.atom_number
        fgs = os.path.join(self.gsinp.guide_bs_dir, self.gsinp.guide_bs_fname)
        self.element_exp_list.clear()
        l1 = 0
        l2 = 0
        il = 0
        with open(fgs, 'r') as f:
            lines = f.readlines()
            for iline, line in enumerate(lines):
                if el_line in line:
                    #print('l1: ', line)
                    l1 = iline
                    for jline, line in enumerate(lines[l1+1:]):
                        if 'a ' in line:
                            #print('l2: ', line)
                            l2 = l1+jline
                            break
            for line in lines[l1+1:l2]:
                intn = re.findall("(?<![\.\d])[0-9]+(?![\.\d])", line)
                fl = re.findall("[+-]?\d+\.\d+E[+-]\d+", line)
                if intn and not fl:
                    #print('HERE: ',intn[0])
                    self.element_Nexp_by_l[il] = int(intn[0])
                    il += 1
                #print('our line: ', line)
            for line in lines[l1+1:l2]:
                fl = re.findall("[+-]?\d+\.\d+E[+-]\d+", line)
                if fl:
                    self.element_exp_list.append(fl[0])
            i1 = 0
            for k, v in self.element_Nexp_by_l.items():
                i2 = i1+v
                self.element_exp_list_by_l[k] = self.element_exp_list[i1:i2]
                #print('tu: ', k, v, i1, i2)
                i1 = i2
            #for k, v in self.element_exp_list_by_l.items():
            #    print('HELLO! {} : {}'.format(k, v))
        return self.element_exp_list_by_l




# ------------------------------------------------------------------------------

def main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--atom_number', action='store')
    parser.add_argument('--zeta', action='store', type=int)
    parser.add_argument('--guide_bs_dir', action='store')
    parser.add_argument('--guide_bs_fname', action='store')
    parser.add_argument('--choose_start_expval', action='store', choices=['max_of_gs', 'min_of_gs', 'max_of_atomgs', 'min_of_atomgs', 'custom'])
    parser.add_argument('--choose_start_Nexp', action='store', type=int)
    parser.add_argument('--decrease', action='store', choices=['y', 'n'])
    parser.add_argument('--result_bs_allexp_fname', action='store')
    parser.add_argument('--result_bs_elementexp_fname', action='store')
    parser.add_argument('--mol_template_dir', action='store')
    parser.add_argument('--mol_template', action='store')
    args=parser.parse_args()
    #print(vars(args))
    if len(sys.argv) == 1:
        print(parser.format_help().strip())
        sys.exit()
    return args

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    args = main_parser()

    # get data from 'guide basis set'
    gs_data=guide_set()
    max_allexp = gs_data.get_max_of_gs()
    min_allexp = gs_data.get_min_of_gs()
    element_set = gs_data.get_gs_element()
    element_set_by_l = gs_data.get_gs_element_by_l()
    #print('element set: ', element_set)
    max_element_exp = max([float(x) for x in element_set])
    min_element_exp = min([float(x) for x in element_set])


    # generate new exponents; generic set
    if args.decrease == 'y':
        if args.choose_start_expval == 'max_of_gs':
            start_exp = max_allexp
            gen_data=et_set(start_exp, args.zeta, args.choose_start_Nexp, True, args.result_bs_allexp_fname)
            allexp = gen_data.calc_with_decrease()
        elif args.choose_start_expval == 'max_of_atomgs':
            start_exp = max_element_exp
            gen_data=et_set(start_exp, args.zeta, args.choose_start_Nexp, True, args.result_bs_allexp_fname)
            allexp = gen_data.calc_with_decrease()
    elif args.decrease == 'n':
        if args.choose_start_expval == 'min_of_gs':
            start_exp = min_allexp
            gen_data=et_set(start_exp, args.zeta, args.choose_start_Nexp, False, args.result_bs_allexp_fname)
            allexp = gen_data.calc_with_increase()
        elif args.choose_start_expval == 'min_of_atomgs':
            start_exp = min_element_exp
            gen_data=et_set(start_exp, args.zeta, args.choose_start_Nexp, False, args.result_bs_allexp_fname)
            allexp = gen_data.calc_with_increase()


    # generate new exponents; atom specific
    if not element_set:
        sys.exit('element_set not set')
    else:
        if args.decrease == 'y':
            if args.choose_start_expval == 'max_of_gs':
                start_exp = max_allexp
                if (start_exp < max([float(x) for x in element_set])):
                    sys.exit('max exponent for this element is smaller than the established start_exp, quitting')
                else:
                    gen_specific=et_set_by_l(allexp, element_set_by_l, True, args.result_bs_elementexp_fname)
                    gen_specific.calc_with_decrease()
            elif args.choose_start_expval == 'max_of_atomgs':
                start_exp = max_element_exp
                if (start_exp < max([float(x) for x in element_set])):
                    sys.exit('max exponent for this element is smaller than the established start_exp, quitting')
                else:
                    gen_specific=et_set_by_l(allexp, element_set_by_l, True, args.result_bs_elementexp_fname)
                    gen_specific.calc_with_decrease()
        elif args.decrease == 'n':
            if args.choose_start_expval == 'min_of_gs':
                start_exp = min_allexp
                if (start_exp > min([float(x) for x in element_set])):
                    sys.exit('min exponent for this element is larger than the established start_exp, quitting')
                else:
                    gen_specific=et_set_by_l(allexp, element_set_by_l, False, args.result_bs_elementexp_fname)
                    gen_specific.calc_with_increase()
            elif args.choose_start_expval == 'min_of_atomgs':
                start_exp = min_element_exp
                if (start_exp > min([float(x) for x in element_set])):
                    sys.exit('min exponent for this element is larger than the established start_exp, quitting')
                else:
                    gen_specific=et_set_by_l(allexp, element_set_by_l, False, args.result_bs_elementexp_fname)
                    gen_specific.calc_with_increase()







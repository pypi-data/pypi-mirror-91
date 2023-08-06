#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.



from test_utils import NotebookTest



class TestWorkflow(NotebookTest):

    def test_no_output(self, notebook):
        '''Test no output from workflow cell'''
        assert not notebook.check_output('''
            [1]
            print('hellp world')
            ''', kernel='SoS')

    def test_task(self, notebook):
        '''Test the execution of tasks with -s force'''
        output = notebook.check_output('''\
            %run -s force
            [10]
            input: for_each={'i': range(1)}
            task: queue='localhost'
            python: expand=True
            import time
            print("this is {i}")
            time.sleep({i})

            [20]
            input: for_each={'i': range(2)}
            task:  queue='localhost'
            python: expand=True
            import time
            print("this aa is {i}")
            time.sleep({i})
            ''', kernel='SoS')
        assert "Ran for < 5 seconds" in output and 'completed' in output


    def test_background_mode(self, notebook):
        '''test executing sos workflows in background'''
        idx = notebook.call('''\
            %run &
            import time
            for i in range(5):
                print('output {}'.format(i));time.sleep(1)
            ''', kernel='SoS')
        output = notebook.get_cell_output(idx)
        assert 'output 4' not in output
        import time
        time.sleep(10)
        output = notebook.get_cell_output(idx)
        assert 'output 4' in output


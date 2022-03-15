# Permitted additional libraries
import unittest # for running unit tests
from random import uniform # for fuzz testing
import io # used to redirect stdout for testing
import sys # used to redirect stdout for testing

# CookieLog class + most_active_cookie imports (by Bryce Wong)
from CookieLog import CookieLog
from most_active_cookie import main

class TestStringMethods(unittest.TestCase):

    # most_active_cookie FUNCTIONALITY
    # NOTE: \n included at the end of expected outputs due to print(...) appending a \n to outputted values

    ### Test provided examples given by Quantcast ###
    def test_MAC_naive(self):
        # 2018-12-07 input
        output = io.StringIO()
        sys.stdout = output  
        main(['cookie_log.csv', '-d', '2018-12-07'])
        self.assertEqual(output.getvalue(), '4sMM2LxV07bPJzwf\n')

        # 2018-12-08 input
        output = io.StringIO()
        sys.stdout = output
        main(['cookie_log.csv', '-d', '2018-12-08'])
        self.assertEqual(output.getvalue(), 'SAZuXPGUrfbcn5UA\n4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG\n')

         # 2018-12-09 input
        output = io.StringIO()
        sys.stdout = output
        main(['cookie_log.csv', '-d', '2018-12-09'])
        self.assertEqual(output.getvalue(), 'AtY0laUfhglK3lC7\n')

    ### Secondary test file ###
    def test_MAC_custom(self):
        # 2018-12-07 input
        output = io.StringIO()
        sys.stdout = output  
        main(['test_data/cookie_log_2.csv', '-d', '2018-12-06'])
        self.assertEqual(output.getvalue(), 'SAZuXPGUrfbcn5UA\n')

        # 2018-12-08 input
        output = io.StringIO()
        sys.stdout = output
        main(['test_data/cookie_log_2.csv', '-d', '2018-12-07'])
        self.assertEqual(output.getvalue(), 'AtY0laUfhglK3lC7\n')

         # 2018-12-09 input
        output = io.StringIO()
        sys.stdout = output
        main(['test_data/cookie_log_2.csv', '-d', '2018-12-08'])
        self.assertEqual(output.getvalue(), '4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG\n')

    ### NOTE: Fuzztesting with different files covered in CookieLog tests below ###

    
    # most_active_cookie ERROR/EDGE CASES

    ### Tests for invalid input file ###
    def test_MAC_invalid_file(self):
        with self.assertRaises(AssertionError):
            main(['foobar.csv', '-d', '2018-12-08'])

    ### Tests for invalid flag in first slot ###
    def test_MAC_invalid_flag(self):
        with self.assertRaises(AssertionError):
            main(['-d', '2018-12-08', 'cookie_log.csv'])

    ### Tests for missing flag in second slot + wrong flag placement ###
    def test_MAC_missing_flag(self):
        with self.assertRaises(AssertionError):
            main(['cookie_log.csv', '2018-12-08'])

        with self.assertRaises(AssertionError):
            main(['cookie_log.csv', '2018-12-08', '-d'])

     ### Tests for too many arguments ###
    def test_MAC_invalid_arg_count(self):
        with self.assertRaises(AssertionError):
            main(['cookie_log.csv', '-d', '2018-12-07', '2018-12-08'])

        with self.assertRaises(AssertionError):
            main(['test_data/cookie_log.csv', 'test_data/cookie_log2.csv', '-d', '2018-12-07', '2018-12-08'])


    # CookieLog FUNCTIONALITY

    ### Test provided examples given by Quantcast ###
    def test_CL_naive(self):
        cl = CookieLog()
        cl.add_cookies_from_file("cookie_log.csv")

        self.assertEqual(cl.most_active_cookie("2018-12-07"), '4sMM2LxV07bPJzwf')
        self.assertEqual(cl.most_active_cookie("2018-12-08"), \
                'SAZuXPGUrfbcn5UA\n4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG')
        self.assertEqual(cl.most_active_cookie("2018-12-09"), 'AtY0laUfhglK3lC7')

    ### Test addition of multiple files to CookieLog object ###
    def test_CL_multiple_naive(self):
        cl = CookieLog()
        cl.add_cookies_from_file("test_data/cookie_log.csv")
        cl.add_cookies_from_file("test_data/cookie_log_2.csv")
        
        # New date from second csv file
        self.assertEqual(cl.most_active_cookie("2018-12-06"), 'SAZuXPGUrfbcn5UA')

        # Changed results with new log additions
        self.assertEqual(cl.most_active_cookie("2018-12-07"), '4sMM2LxV07bPJzwf\nAtY0laUfhglK3lC7')
        self.assertEqual(cl.most_active_cookie("2018-12-08"), '4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG')

        # Other entries should remain unaffected
        self.assertEqual(cl.most_active_cookie("2018-12-09"), 'AtY0laUfhglK3lC7')

    ### Continually add (cookie, timestamp) pairs to CookieLog randomly; check that results are consistent ###
    def test_CL_fuzzy_inserts(self):
        # Initialize default timestamps and cookie values
        timestamps = [f"2018-0{a}-0{b}" for a in range(1, 5) for b in range(1, 10)]
        cookies = ['a', 'b', 'c', 'd', 'e']

        # Execute fuzz test 10 times
        for _ in range(10):

            # Keep track of current time : cookie mappings (with counter for each cookie instance)
            mappings = {}
            for time in timestamps:
                mappings[time] = [0, 0, 0, 0, 0]
        
            # Initialize CookieLog object
            cl = CookieLog()
            cl.initialized = True # not passing in file for CookieLog, must set initialized manually

            # Add 50k values to CookieLog object
            for _ in range(50000):
                time_index = round(uniform(0, len(timestamps) - 1))
                t = timestamps[time_index]

                cookie_index = round(uniform(0, len(cookies) - 1))
                c = cookies[cookie_index]
                
                # Add mapping to CookieLog + local mappings
                mappings[t][cookie_index] += 1
                cl.add_to_map(c, t)
            
            # Verify values
            for time in timestamps:
                # get sorted output from CookieLog (sorted because cookie order depends on time of addition)
                outputs = sorted(cl.most_active_cookie(time).split("\n"))
                expected = [cookies[i] for i in range(len(cookies)) if mappings[time][i] == max(mappings[time])]
                
                # confirm that outputs match
                self.assertEqual(outputs, expected)


    # CookieLog ERROR/EDGE CASES

    ### Test that an assertion error is raised with no data initialized in CookieLog
    def test_no_initialization(self):
        cl = CookieLog()
        with self.assertRaises(AssertionError):
            cl.most_active_cookie("2018-11-05")

    ### Test that an assertion error is raised on an invalid date input ###
    def test_invalid_date(self):
        cl = CookieLog()
        cl.add_cookies_from_file("test_data/cookie_log.csv")

        with self.assertRaises(AssertionError):
            cl.most_active_cookie("2018-11-05")

        with self.assertRaises(AssertionError):
            cl.most_active_cookie("foobar")


# Execute unit tests
if __name__ == '__main__':
    unittest.main()
""" Holds test data for test cases."""

from collections import OrderedDict

test_army_data = OrderedDict([('army',
                               OrderedDict([('armyone',
                                             OrderedDict([('TBI',
                                                           OrderedDict([('battalion_name', 'test_battalion_one'),
                                                                        ('rank', 2),
                                                                        ('base_units', 40)])),
                                                          ('TBII',
                                                           OrderedDict([('battalion_name', 'test_battalion_two'),
                                                                        ('rank', 1),
                                                                        ('base_units', 20)]))])),
                                            ('armytwo',
                                             OrderedDict([('TBI',
                                                           OrderedDict([('battalion_name', 'test_battalion_one'),
                                                                        ('rank', 2),
                                                                        ('base_units', 10)])),
                                                          ('TBII',
                                                           OrderedDict([('battalion_name', 'test_battalion_two'),
                                                                        ('rank', 1),
                                                                        ('base_units',
                                                                         5)]))]))])),
                              ])

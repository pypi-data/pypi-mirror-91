import unittest
import pandas as pd
import app


class MoveTests(unittest.TestCase):

    def test_five_plus_five(self):
        assert 5 + 5 == 10

    def test_ont_plus_one(self):
        assert not 1+ 1 == 3
        
    def test_getUniqOS(self):
        df = pd.read_csv(r'../data.csv')
        list1 = app.getUniqOS(df)
        list2 = app.getUniqOS(df)
        self.assertEqual(list1, list2)
        self.assertIn('ANDROID', list2)
        self.assertIn('IOS', list2)

    def test_getUniqCountries(self):
        df = pd.read_csv(r'../data.csv')
        list1 = app.getUniqOS(df)
        list2 = app.getUniqCountries(df)
        self.assertNotEqual(list1, list2)
        self.assertIn('Brazil', list2)
        self.assertIn('India',list2)

    def test_indiaStates(self):
        df = pd.read_csv(r'../data.csv')
        ios_india_state_count, and_india_state_count, india_uniq_states = app.indiaStates(df)
        
        self.assertIn('Telangana', ios_india_state_count)
        self.assertIn('Punjab', and_india_state_count)
        self.assertIn('Sikkim', india_uniq_states)

    def test_indiaStates(self):
        df = pd.read_csv(r'../data.csv')
        brands = app.phone_brands(df)
        
        self.assertIn('Huawei', brands)
        self.assertIn('Apple', brands)
        self.assertIn('LG', brands)

    def test_topBrandsandCountries(self):
        df = pd.read_csv(r'../data.csv')
        countries_uniq = app.getUniqCountries(df)
        top_countries,apple,samsung,huawei = app.topBrandsandCountries(df,countries_uniq)

        self.assertIn('Spain',top_countries)
        self.assertListEqual([72, 70, 1478, 50, 214, 438, 205] , apple)
        self.assertListEqual([1161, 377, 30, 338, 1041, 708, 351] , samsung)
        self.assertListEqual([1, 192, 273, 231, 114, 606, 254] , huawei)


    
if __name__ == "__main__":
    unittest.main()
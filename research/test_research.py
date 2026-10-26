import unittest
import numpy as np
import pandas as pd
from asnya_research import synthetic_prices, validate_prices, backtest, select_on_training, fingerprint

class ResearchTests(unittest.TestCase):
    def test_compounding_and_entry_cost(self):
        data = pd.DataFrame({'date':pd.bdate_range('2020-01-01',periods=300), 'close':np.arange(100.,400.)})
        path, metrics = backtest(data, 2, 3, 0)
        self.assertAlmostEqual(metrics['total_return'], 399/102-1)
        self.assertEqual(metrics['position_changes'],1)
        self.assertEqual(metrics['max_drawdown'],0)
        cost_path,_=backtest(data,2,3,100)
        self.assertAlmostEqual(cost_path.equity.iloc[1],100*(103/102-.01))
        self.assertLess(cost_path.equity.iloc[-1],path.equity.iloc[-1])

    def test_no_future_price_or_test_selection_leakage(self):
        data=synthetic_prices(); changed=data.copy();changed.loc[600:,'close']*=2
        before,_=backtest(data);after,_=backtest(changed)
        pd.testing.assert_frame_equal(before.iloc[:541],after.iloc[:541])
        self.assertEqual(before.loc[541,'position'],after.loc[541,'position'])
        candidates=[(10,40),(20,60),(40,120)]
        a,rank_a=select_on_training(data,504,candidates)
        b,rank_b=select_on_training(changed,504,candidates)
        self.assertEqual(a,b);pd.testing.assert_frame_equal(rank_a,rank_b)
        test,_=backtest(data,**a,start=504)
        self.assertEqual(test.date.iloc[1],data.date.iloc[504])
        self.assertEqual(test.equity.iloc[0],100)

    def test_validation_and_reproducibility(self):
        data=synthetic_prices();self.assertEqual(fingerprint(data),fingerprint(synthetic_prices()))
        for value in [np.nan, np.inf, 0, -1]:
            changed=data.copy();changed.loc[10,'close']=value
            with self.assertRaises(ValueError):validate_prices(changed)
        changed=data.copy();changed.loc[1,'date']=changed.date.iloc[0]
        with self.assertRaises(ValueError):validate_prices(changed)
        with self.assertRaises(ValueError):backtest(data,60,20)
        with self.assertRaises(ValueError):backtest(data,cost_bps=-1)
        with self.assertRaises(ValueError):select_on_training(data,740,[(20,60)])

if __name__=='__main__':unittest.main()

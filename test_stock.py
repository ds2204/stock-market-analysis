import unittest
from unittest.mock import Mock, patch
import math
import stockMarketAnalysis as s
class StockTests(unittest.TestCase):
 def test_rsi(self):
  self.assertEqual(s.calculate_rsi(list(range(1,21))),100)
  self.assertEqual(s.calculate_rsi(list(range(21,1,-1))),0)
  self.assertEqual(s.calculate_rsi([5]*20),50)
  self.assertTrue(math.isnan(s.calculate_rsi([1,2])))
 def test_trend_and_missing(self):
  self.assertEqual(s.calculate_trend([3,3])[0],'Flat')
  self.assertEqual(s.calculate_trend([1])[0],'Unavailable')
  self.assertTrue(math.isnan(s.calculate_moving_averages([1,2])[0]))
 def test_order_and_volume(self):
  data=[['2024-01-02',2,3,1,2,20],['2024-01-01',1,2,1,1,10]]
  a=s.get_insights(data,'test');b=s.get_insights(data[::-1],'test')
  self.assertEqual(a['price_change'],b['price_change'])
  self.assertEqual(a['price_change'],1)
  self.assertEqual((a['min_volume'],a['max_volume']),(10,20))
  self.assertIn('10 to 20 shares',s.generate_graph_description(a))
  with self.assertRaises(ValueError):s.get_insights([],'empty')
 def test_no_import_cloud(self):
  self.assertIsNone(s.dynamodb);self.assertIsNone(s.ses_client)
 def test_pagination(self):
  db=Mock();db.Table.return_value.scan.side_effect=[{'Items':[{'emailID':'sender','emailAddress':'sender@example.com'}],'LastEvaluatedKey':{'id':'a'}},{'Items':[{'emailID':'recipient1','emailAddress':'recipient@example.com'}]}]
  with patch.object(s,'dynamodb',db):self.assertEqual(s.get_email_credentials(),('sender@example.com',['recipient@example.com']))
 def test_send_failure(self):
  client=Mock();client.send_raw_email.side_effect=RuntimeError('simulated')
  with patch.object(s,'ses_client',client),patch.object(s,'get_email_credentials',return_value=('sender@example.com',['recipient@example.com'])):
   with self.assertRaises(RuntimeError):s.send_email_with_attachment('<p>test</p>')
 def test_no_data_no_email(self):
  with patch.object(s,'get_stock_data',return_value=[]),patch.object(s,'send_email_with_attachment') as send:
   self.assertEqual(s.lambda_handler({'tickers':{'AAPL':'Apple'}},{})['statusCode'],502);send.assert_not_called()
 def test_escape(self):
  html=s.generate_html_content('<bad>','<script>alert(1)</script>',{},{});self.assertNotIn('<script>',html)
 def test_plot(self):
  result=s.plot_and_encode({'test':[['2024-01-02',2,3,1,2,20],['2024-01-01',1,2,1,1,10]]})
  self.assertTrue(result['stock_analysis_test'].startswith('iVBOR'))
if __name__=='__main__':unittest.main()

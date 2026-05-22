from __future__ import annotations
import csv, shutil, tempfile, unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import store_ops

class StoreOpsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
    def tearDown(self):
        shutil.rmtree(self.tmp)
    def test_sample_pipeline_outputs_core_files(self):
        sample = self.tmp / 'market.csv'
        store_ops.sample_data(sample)
        out = self.tmp / 'ops'
        store_ops.run_pipeline(sample, out)
        self.assertTrue((out / 'product_scores.csv').exists())
        self.assertTrue((out / 'content_calendar.csv').exists())
        self.assertTrue((out / 'kpi_tracker.csv').exists())
        self.assertTrue((out / 'store-ops-dashboard.html').exists())
        self.assertTrue(any((out / 'listings').glob('*.md')))
    def test_scoring_decision_bands(self):
        s = store_ops.score_row({'keyword':'x','product':'y','demand':'95','competition':'10','margin':'95','production':'95','repeat':'80','risk':'5','price':'10000','cost':'1000'})
        self.assertEqual(s.decision, 'launch test')
        self.assertGreaterEqual(s.opportunity_score, 80)
    def test_korean_aliases_are_supported(self):
        s = store_ops.score_row({'키워드':'식단표','상품명':'냉장고 식단표','수요':'70','경쟁':'30','가격':'5000','원가':'500'})
        self.assertEqual(s.keyword, '식단표')
        self.assertEqual(s.product, '냉장고 식단표')
        self.assertGreater(s.gross_profit, 0)
    def test_listing_contains_approval_checklist(self):
        sample = self.tmp / 'market.csv'; out = self.tmp / 'ops'
        store_ops.sample_data(sample)
        scores = store_ops.analyze_market(sample, out)
        paths = store_ops.generate_listings(scores, out / 'listings', limit=1)
        text = paths[0].read_text(encoding='utf-8')
        self.assertIn('Approval Checklist', text)
        self.assertIn('legal_approved=true', text)

if __name__ == '__main__':
    unittest.main()

class StoreOps100PointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
    def tearDown(self):
        shutil.rmtree(self.tmp)
    def _pipeline(self):
        sample = self.tmp / 'market.csv'
        store_ops.sample_data(sample)
        out = self.tmp / 'ops'
        store_ops.run_pipeline(sample, out)
        return out
    def test_100_pipeline_outputs_import_and_risk_files(self):
        out = self._pipeline()
        self.assertTrue((out / 'store_import.csv').exists())
        self.assertTrue((out / 'risk_scan.csv').exists())
        self.assertTrue((out / 'operator_review_queue.csv').exists())
        self.assertTrue((out / '100_POINT_OPERATIONS_RUNBOOK.md').exists())
    def test_101_printable_outputs_pdf_html_txt(self):
        paths = store_ops.generate_printables('테스트 상품', self.tmp / 'printables', '민준')
        suffixes = {p.suffix for p in paths}
        self.assertIn('.pdf', suffixes)
        self.assertIn('.html', suffixes)
        self.assertIn('.txt', suffixes)
    def test_102_risk_scanner_flags_guarantee(self):
        result = store_ops.scan_text_risk('성적 향상 100% 보장되는 포켓몬 캐릭터 자료')
        self.assertEqual(result['severity'], 'high')
        self.assertGreaterEqual(result['finding_count'], 2)
    def test_103_scan_listing_risks_writes_csv(self):
        d = self.tmp / 'listings'; d.mkdir()
        (d / 'bad.md').write_text('무조건 성적 향상 보장', encoding='utf-8')
        out = store_ops.scan_listing_risks(d, self.tmp / 'risk.csv')
        rows = store_ops.read_csv(out)
        self.assertEqual(rows[0]['severity'], 'high')
    def test_104_export_store_import_is_unpublished(self):
        out = self._pipeline()
        rows = store_ops.read_csv(out / 'store_import.csv')
        self.assertTrue(rows)
        self.assertTrue(all(r['visibility'] == 'unpublished' for r in rows))
        self.assertIn('operator', rows[0]['approval_required'])
    def test_105_kpi_evaluation_scale_decision(self):
        kpi = self.tmp / 'kpi.csv'
        store_ops.write_csv(kpi, [{'date':'2026-01-01','channel':'smartstore','product':'A','views':1000,'clicks':100,'orders':5,'revenue':100000,'ad_spend':20000,'returns':0,'cs_tickets':1}], ['date','channel','product','views','clicks','orders','revenue','ad_spend','returns','cs_tickets'])
        out = store_ops.evaluate_kpi(kpi, self.tmp / 'decision.csv')
        self.assertEqual(store_ops.read_csv(out)[0]['ops_decision'], 'scale cautiously')
    def test_106_kpi_evaluation_thumbnail_decision(self):
        kpi = self.tmp / 'kpi.csv'
        store_ops.write_csv(kpi, [{'date':'2026-01-01','channel':'blog','product':'A','views':500,'clicks':2,'orders':0,'revenue':0,'ad_spend':0,'returns':0,'cs_tickets':0}], ['date','channel','product','views','clicks','orders','revenue','ad_spend','returns','cs_tickets'])
        out = store_ops.evaluate_kpi(kpi, self.tmp / 'decision.csv')
        self.assertEqual(store_ops.read_csv(out)[0]['ops_decision'], 'improve thumbnail/title')
    def test_107_review_queue_contains_platform_approval(self):
        out = self._pipeline()
        rows = store_ops.read_csv(out / 'operator_review_queue.csv')
        self.assertTrue(any('platform import approval' in r['review_type'] for r in rows))
    def test_108_runbook_has_hard_stop_rules(self):
        p = store_ops.render_ops_runbook(self.tmp / 'RUNBOOK.md')
        text = p.read_text(encoding='utf-8')
        self.assertIn('Hard Stop Rules', text)
        self.assertIn('100-Point Definition', text)
    def test_109_cli_generate_printables(self):
        import subprocess
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'generate-printables', '테스트', '--output', str(self.tmp / 'p')], text=True, capture_output=True, check=True)
        self.assertIn('reward-board.pdf', proc.stdout)
    def test_110_cli_scan_risks(self):
        d = self.tmp / 'l'; d.mkdir(); (d / 'x.md').write_text('환불 불가', encoding='utf-8')
        import subprocess
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'scan-risks', str(d), '--output', str(self.tmp / 'r.csv')], check=True)
        self.assertTrue((self.tmp / 'r.csv').exists())
    def test_111_pipeline_dashboard_still_renders(self):
        out = self._pipeline()
        text = (out / 'store-ops-dashboard.html').read_text(encoding='utf-8')
        self.assertIn('AI Store Operations Dashboard', text)
    def test_112_store_import_contains_risk_severity(self):
        out = self._pipeline()
        rows = store_ops.read_csv(out / 'store_import.csv')
        self.assertIn('risk_severity', rows[0])
    def test_113_printable_pdf_has_pdf_header(self):
        paths = store_ops.generate_printables('테스트 상품', self.tmp / 'printables')
        pdf = next(p for p in paths if p.suffix == '.pdf')
        self.assertTrue(pdf.read_bytes().startswith(b'%PDF'))
    def test_114_review_queue_contains_print_review(self):
        out = self._pipeline()
        rows = store_ops.read_csv(out / 'operator_review_queue.csv')
        self.assertTrue(any(r['review_type'] == 'print/readability' for r in rows))
    def test_115_ops_runbook_generated_by_pipeline(self):
        out = self._pipeline()
        self.assertIn('Daily Loop', (out / '100_POINT_OPERATIONS_RUNBOOK.md').read_text(encoding='utf-8'))

class StoreOpsLiveIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
    def tearDown(self):
        shutil.rmtree(self.tmp)
    def _ops(self):
        sample = self.tmp / 'market.csv'
        store_ops.sample_data(sample)
        out = self.tmp / 'ops'
        store_ops.run_pipeline(sample, out)
        return out
    def test_200_pipeline_outputs_ip_and_platform_staging(self):
        out = self._ops()
        self.assertTrue((out / 'ip_precheck.csv').exists())
        self.assertTrue((out / 'image_generation_plan.csv').exists())
        self.assertTrue((out / 'platform_api_staging/naver_api_staging.csv').exists())
        self.assertTrue((out / 'platform_api_staging/coupang_api_staging.csv').exists())
        self.assertTrue((out / 'platform_api_staging/shopify_api_staging.csv').exists())
    def test_201_ip_precheck_blocks_famous_character(self):
        r = store_ops.ip_precheck_text('포켓몬 캐릭터 칭찬스티커 디자인')
        self.assertEqual(r['severity'], 'high')
        self.assertIn('blocked', r['status'])
    def test_202_ip_precheck_writes_search_queries(self):
        p = self.tmp / 'listing.md'; p.write_text('특허 구조 캐릭터 스티커', encoding='utf-8')
        out = store_ops.ip_precheck(p, self.tmp / 'ip.csv')
        rows = store_ops.read_csv(out)
        self.assertIn('KIPRIS', rows[0]['search_queries'])
    def test_203_image_plan_never_allows_public_use_by_default(self):
        out = self._ops()
        rows = store_ops.read_csv(out / 'image_generation_plan.csv')
        self.assertTrue(rows)
        self.assertTrue(all(r['public_use_allowed'] == 'no' for r in rows))
        self.assertIn('copyrighted', rows[0]['negative_prompt'])
    def test_204_platform_payloads_have_live_publish_false(self):
        out = self._ops()
        rows = store_ops.read_csv(out / 'platform_api_staging/naver_api_staging.csv')
        self.assertTrue(rows)
        self.assertTrue(all(r['live_publish_allowed'] == 'false' for r in rows))
    def test_205_ingest_orders_outputs_fulfillment_cs_shipping(self):
        orders = self.tmp / 'orders.csv'
        store_ops.write_csv(orders, [{'order_id':'O1','product':'A','status':'paid','paid':'true','customer_message':'배송 언제 되나요?'}], ['order_id','product','status','paid','customer_message'])
        paths = store_ops.ingest_orders(orders, self.tmp / 'order_ops')
        names = {p.name for p in paths}
        self.assertIn('fulfillment_queue.csv', names)
        self.assertIn('cs_triage.csv', names)
        self.assertIn('shipping_update_staging.csv', names)
    def test_206_cs_refund_message_escalates_to_operator(self):
        orders = self.tmp / 'orders.csv'
        store_ops.write_csv(orders, [{'order_id':'O2','product':'A','status':'paid','paid':'true','customer_message':'환불 안되면 고소합니다'}], ['order_id','product','status','paid','customer_message'])
        store_ops.ingest_orders(orders, self.tmp / 'order_ops')
        rows = store_ops.read_csv(self.tmp / 'order_ops/cs_triage.csv')
        self.assertEqual(rows[0]['triage'], 'operator_escalation')
    def test_207_live_runbook_mentions_webhook_and_rollback(self):
        p = store_ops.render_live_integration_runbook(self.tmp / 'LIVE.md')
        text = p.read_text(encoding='utf-8')
        self.assertIn('webhook', text.lower())
        self.assertIn('rollback', text.lower())
    def test_208_cli_ip_precheck(self):
        import subprocess
        p = self.tmp / 'x.md'; p.write_text('디즈니 캐릭터', encoding='utf-8')
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'ip-precheck', str(p), '--output', str(self.tmp / 'ip.csv')], check=True)
        self.assertTrue((self.tmp / 'ip.csv').exists())
    def test_209_cli_platform_payloads(self):
        import subprocess
        out = self._ops()
        target = self.tmp / 'payloads2'
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'platform-payloads', str(out / 'product_scores.csv'), str(out / 'listings'), '--output', str(target)], check=True)
        self.assertTrue((target / 'shopify_api_staging.csv').exists())

class StoreOpsConnectorStateKillSwitchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
    def tearDown(self):
        shutil.rmtree(self.tmp)
    def _ops(self):
        sample = self.tmp / 'market.csv'
        store_ops.sample_data(sample)
        out = self.tmp / 'ops'
        store_ops.run_pipeline(sample, out)
        return out
    def test_300_connector_manifest_separates_platforms(self):
        paths = store_ops.build_connector_manifest(self.tmp / 'connectors')
        names = {p.name for p in paths}
        self.assertIn('connector_manifest.json', names)
        self.assertIn('naver_connector_contract.md', names)
        self.assertIn('coupang_connector_contract.md', names)
        self.assertIn('shopify_connector_contract.md', names)
    def test_301_connector_matrix_blocks_live_by_default(self):
        store_ops.build_connector_manifest(self.tmp / 'connectors')
        rows = store_ops.read_csv(self.tmp / 'connectors/api_connector_matrix.csv')
        self.assertTrue(rows)
        self.assertTrue(all(r['live_allowed'] == 'false' for r in rows))
    def test_302_order_state_machine_paid_to_prepare_when_proof_ok(self):
        result = store_ops.transition_order_state('paid', 'paid', paid=True, proof_ok=True)
        self.assertEqual(result['to_state'], 'prepare')
        self.assertEqual(result['live_update_allowed'], 'false')
    def test_303_order_state_machine_refund_goes_to_review(self):
        result = store_ops.transition_order_state('shipped', 'refund_requested', paid=True)
        self.assertEqual(result['to_state'], 'refund_review')
    def test_304_order_state_machine_csv_output(self):
        orders = self.tmp / 'orders.csv'
        store_ops.write_csv(orders, [{'order_id':'O3','state':'paid','event':'paid','paid':'true','proof_ok':'true'}], ['order_id','state','event','paid','proof_ok'])
        out = store_ops.create_order_state_machine(orders, self.tmp / 'states.csv')
        rows = store_ops.read_csv(out)
        self.assertEqual(rows[0]['to_state'], 'prepare')
        self.assertEqual(rows[0]['operator_gate'], 'required_before_live_platform_update')
    def test_305_cs_classifier_detects_legal_threat(self):
        c = store_ops.classify_cs_message('환불 안 해주면 고소하고 신고하겠습니다')
        self.assertEqual(c['category'], 'legal_threat')
        self.assertEqual(c['triage'], 'operator_escalation')
        self.assertEqual(c['auto_reply_allowed'], 'no')
    def test_306_ingest_orders_adds_cs_category_and_rules(self):
        orders = self.tmp / 'orders.csv'
        store_ops.write_csv(orders, [{'order_id':'O4','product':'A','status':'paid','paid':'true','customer_message':'PDF 다운로드 링크가 안 와요'}], ['order_id','product','status','paid','customer_message'])
        store_ops.ingest_orders(orders, self.tmp / 'order_ops')
        rows = store_ops.read_csv(self.tmp / 'order_ops/cs_triage.csv')
        self.assertEqual(rows[0]['category'], 'download_access')
        self.assertIn('download_access', rows[0]['matched_rules'])
    def test_307_auto_pause_hard_pauses_on_high_risk(self):
        kpi = self.tmp / 'kpi.csv'
        risk = self.tmp / 'risk.csv'
        store_ops.write_csv(kpi, [{'date':'2026-01-01','product':'A','views':100,'clicks':10,'orders':1,'returns':0,'revenue':10000,'ad_spend':0,'cs_tickets':0}], ['date','product','views','clicks','orders','returns','revenue','ad_spend','cs_tickets'])
        store_ops.write_csv(risk, [{'file':'x','severity':'high'}], ['file','severity'])
        out = store_ops.auto_pause_rules(kpi, None, risk, self.tmp / 'pause.csv')
        rows = store_ops.read_csv(out)
        self.assertEqual(rows[0]['kill_switch_action'], 'hard_pause')
    def test_308_auto_pause_low_roas_pauses_ads(self):
        kpi = self.tmp / 'kpi.csv'
        store_ops.write_csv(kpi, [{'date':'2026-01-01','product':'A','views':1000,'clicks':100,'orders':1,'returns':0,'revenue':10000,'ad_spend':50000,'cs_tickets':0}], ['date','product','views','clicks','orders','returns','revenue','ad_spend','cs_tickets'])
        out = store_ops.auto_pause_rules(kpi, None, None, self.tmp / 'pause.csv')
        self.assertEqual(store_ops.read_csv(out)[0]['kill_switch_action'], 'pause_ads')
    def test_309_audit_log_contains_payload_hash_and_rollback(self):
        out = self._ops()
        rows = store_ops.read_csv(out / 'audit_log.csv')
        self.assertTrue(rows)
        self.assertIn('payload_hash', rows[0])
        self.assertIn('rollback_note', rows[0])
    def test_310_pipeline_outputs_connector_and_pause_artifacts(self):
        out = self._ops()
        self.assertTrue((out / 'connector_contracts/connector_manifest.json').exists())
        self.assertTrue((out / 'auto_pause_decisions.csv').exists())
        self.assertTrue((out / 'audit_log.csv').exists())
    def test_311_cli_connector_manifest(self):
        import subprocess
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'connector-manifest', '--output', str(self.tmp / 'c')], check=True)
        self.assertTrue((self.tmp / 'c/connector_manifest.json').exists())
    def test_312_cli_order_state_machine(self):
        import subprocess
        orders = self.tmp / 'orders.csv'
        store_ops.write_csv(orders, [{'order_id':'O5','state':'created','event':'paid','paid':'true'}], ['order_id','state','event','paid'])
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'order-state-machine', str(orders), '--output', str(self.tmp / 'states.csv')], check=True)
        self.assertTrue((self.tmp / 'states.csv').exists())
    def test_313_cli_auto_pause(self):
        import subprocess
        kpi = self.tmp / 'kpi.csv'
        store_ops.write_csv(kpi, [{'date':'2026-01-01','product':'A','views':500,'clicks':2,'orders':0,'returns':0,'revenue':0,'ad_spend':0,'cs_tickets':0}], ['date','product','views','clicks','orders','returns','revenue','ad_spend','cs_tickets'])
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'auto-pause', str(kpi), '--output', str(self.tmp / 'pause.csv')], check=True)
        self.assertTrue((self.tmp / 'pause.csv').exists())
    def test_314_cli_audit_log(self):
        import subprocess
        out = self._ops()
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'store_ops.py'), 'audit-log', str(out), '--output', str(self.tmp / 'audit.csv')], check=True)
        self.assertTrue((self.tmp / 'audit.csv').exists())

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal
from unittest import TestCase

from lexnlp.extract.en.money import get_money
from lexnlp.extract.en.durations import get_durations


class MoneyDurationIssueTest(TestCase):

    def test_money_and_duration_from_issue_example(self):
        text = (
            "The amount of 120.000 USD should be paid in 12 equal monthly instalments "
            "starting with Jun 16, 2024."
        )

        # Money
        money = list(get_money(text, return_sources=False))
        self.assertTrue(len(money) >= 1, "Expected at least one money match")
        # amount should parse to Decimal('120.000') with default float_digits=4
        self.assertEqual(money[0][1], 'USD')
        self.assertEqual(money[0][0], Decimal('120.000'))

        # Durations
        durations = list(get_durations(text, return_sources=False))
        self.assertTrue(len(durations) >= 1, "Expected at least one duration match")
        # look for months/12
        found_month = any(d[0] in ('month', 'months') and d[1] == Decimal(12) for d in durations)
        self.assertTrue(found_month, f"Expected a 12-month duration in {durations}")

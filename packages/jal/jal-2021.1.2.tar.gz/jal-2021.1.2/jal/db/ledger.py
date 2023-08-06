import logging

from datetime import datetime
from jal.constants import Setup, BookAccount, TransactionType, ActionSubtype, TransferSubtype, CorporateAction, \
    PredefinedCategory, PredefinedPeer
from PySide2.QtCore import Qt, QDate, QDateTime
from PySide2.QtWidgets import QDialog, QMessageBox
from jal.db.helpers import executeSQL, readSQL, readSQLrecord
from jal.db.routines import calculateBalances, calculateHoldings
from jal.ui_custom.helpers import g_tr
from jal.ui.ui_rebuild_window import Ui_ReBuildDialog


class RebuildDialog(QDialog, Ui_ReBuildDialog):
    def __init__(self, parent, frontier):
        QDialog.__init__(self)
        self.setupUi(self)

        self.LastRadioButton.toggle()
        self.frontier = frontier
        frontier_text = datetime.fromtimestamp(frontier).strftime('%d/%m/%Y')
        self.FrontierDateLabel.setText(frontier_text)
        self.CustomDateEdit.setDate(QDate.currentDate())

        # center dialog with respect to parent window
        x = parent.x() + parent.width()/2 - self.width()/2
        y = parent.y() + parent.height()/2 - self.height()/2
        self.setGeometry(x, y, self.width(), self.height())

    def isFastAndDirty(self):
        return self.FastAndDirty.isChecked()

    def getTimestamp(self):
        if self.LastRadioButton.isChecked():
            return self.frontier
        elif self.DateRadionButton.isChecked():
            return self.CustomDateEdit.dateTime().toSecsSinceEpoch()
        else:  # self.AllRadioButton.isChecked()
            return 0


# ===================================================================================================================
# TODO Check are there positive lines for Incomes
# TODO Check are there negative lines for Costs
# ===================================================================================================================
class Ledger:
    SILENT_REBUILD_THRESHOLD = 50

    def __init__(self, db):
        self.db = db
        self.current = {}
        self.current_seq = -1
        self.balances_view = None
        self.holdings_view = None
        self.balance_active_only = 1
        self.balance_currency = None
        self.balance_date = QDateTime.currentSecsSinceEpoch()
        self.holdings_date = QDateTime.currentSecsSinceEpoch()
        self.holdings_currency = None

    def setViews(self, balances, holdings):
        self.balances_view = balances
        self.holdings_view = holdings

    def setActiveBalancesOnly(self, active_only):
        if self.balance_active_only != active_only:
            self.balance_active_only = active_only
            self.updateBalancesView()

    def setBalancesDate(self, balance_date):
        if self.balance_date != balance_date:
            self.balance_date = balance_date
            self.updateBalancesView()

    def setBalancesCurrency(self, currency_id, currency_name):
        if self.balance_currency != currency_id:
            self.balance_currency = currency_id
            balances_model = self.balances_view.model()
            balances_model.setHeaderData(balances_model.fieldIndex("balance_adj"), Qt.Horizontal,
                                         g_tr('Ledger', "Balance, ") + currency_name)
            self.updateBalancesView()

    def updateBalancesView(self):
        calculateBalances(self.db, self.balance_date, self.balance_currency, self.balance_active_only)
        self.balances_view.model().select()

    def setHoldingsDate(self, holdings_date):
        if self.holdings_date != holdings_date:
            self.holdings_date = holdings_date
            self.updateHoldingsView()

    def setHoldingsCurrency(self, currency_id, currency_name):
        if self.holdings_currency != currency_id:
            self.holdings_currency = currency_id
            holidings_model = self.holdings_view.model()
            holidings_model.setHeaderData(holidings_model.fieldIndex("value_adj"), Qt.Horizontal,
                                          g_tr('Ledger', "Value, ") + currency_name)
            self.updateHoldingsView()

    def updateHoldingsView(self):
        calculateHoldings(self.db, self.holdings_date, self.holdings_currency)
        holdings_model = self.holdings_view.model()
        holdings_model.select()
        for row in range(holdings_model.rowCount()):
            if holdings_model.data(holdings_model.index(row, 1)):
                self.holdings_view.setSpan(row, 3, 1, 3)
        self.holdings_view.show()

    # Returns timestamp of last operations that were calculated into ledger
    def getCurrentFrontier(self):
        current_frontier = readSQL(self.db, "SELECT ledger_frontier FROM frontier")
        if current_frontier == '':
            current_frontier = 0
        return current_frontier

    # Add one more transaction to 'book' of ledger.
    # If book is Assets and value is not None then amount contains Asset Quantity and Value contains amount
    #    of money in current account currency. Otherwise Amount contains only money value.
    # Method uses Account, Asset,Peer, Category and Tag values from current transaction
    def appendTransaction(self, book, amount, value=None):
        seq_id = self.current_seq
        timestamp = self.current['timestamp']
        if book == BookAccount.Assets:
            asset_id = self.current['asset']
        else:
            asset_id = self.current['currency']
        account_id = self.current['account']
        if book == BookAccount.Costs or book == BookAccount.Incomes:
            peer_id = self.current['peer']
            category_id = self.current['category']
            tag_id = None if self.current['tag'] == '' else self.current['tag']
        else:
            peer_id = None
            category_id = None
            tag_id = None
        try:
            old_sid, old_amount, old_value = readSQL(self.db,
                "SELECT sid, sum_amount, sum_value FROM ledger_sums "
                "WHERE book_account = :book AND asset_id = :asset_id "
                "AND account_id = :account_id AND sid <= :seq_id "
                "ORDER BY sid DESC LIMIT 1",
                [(":book", book), (":asset_id", asset_id), (":account_id", account_id), (":seq_id", seq_id)])
        except:
            old_sid = -1
            old_amount = 0.0
            old_value = 0.0
        new_amount = old_amount + amount
        if value is None:
            new_value = old_value
        else:
            new_value = old_value + value
        if (abs(new_amount - old_amount) + abs(new_value - old_value)) <= (2 * Setup.CALC_TOLERANCE):
            return  # we have zero amount - no reason to put it into ledger

        _ = executeSQL(self.db, "INSERT INTO ledger (timestamp, sid, book_account, asset_id, account_id, "
                                "amount, value, peer_id, category_id, tag_id) "
                                "VALUES(:timestamp, :sid, :book, :asset_id, :account_id, "
                                ":amount, :value, :peer_id, :category_id, :tag_id)",
                       [(":timestamp", timestamp), (":sid", seq_id), (":book", book), (":asset_id", asset_id),
                        (":account_id", account_id), (":amount", amount), (":value", value),
                        (":peer_id", peer_id), (":category_id", category_id), (":tag_id", tag_id)])
        if seq_id == old_sid:
            _ = executeSQL(self.db, "UPDATE ledger_sums SET sum_amount = :new_amount, sum_value = :new_value"
                                    " WHERE sid = :sid AND book_account = :book"
                                    " AND asset_id = :asset_id AND account_id = :account_id",
                           [(":new_amount", new_amount), (":new_value", new_value), (":sid", seq_id),
                            (":book", book), (":asset_id", asset_id), (":account_id", account_id)])
        else:
            _ = executeSQL(self.db, "INSERT INTO ledger_sums(sid, timestamp, book_account, "
                                    "asset_id, account_id, sum_amount, sum_value) "
                                    "VALUES(:sid, :timestamp, :book, :asset_id, "
                                    ":account_id, :new_amount, :new_value)",
                           [(":sid", seq_id), (":timestamp", timestamp), (":book", book), (":asset_id", asset_id),
                            (":account_id", account_id), (":new_amount", new_amount), (":new_value", new_value)])
        self.db.commit()

    # TODO check that condition <= is really correct for timestamp in this function
    # Returns Amount measured in current account currency or asset_id that 'book' has at current ledger frontier
    def getAmount(self, book, asset_id=None):
        if asset_id is None:
            amount = readSQL(self.db,
                               "SELECT sum_amount FROM ledger_sums WHERE book_account = :book AND "
                               "account_id = :account_id AND timestamp <= :timestamp ORDER BY sid DESC LIMIT 1",
                               [(":book", book), (":account_id", self.current['account']),
                                (":timestamp", self.current['timestamp'])])
        else:
            amount = readSQL(self.db, "SELECT sum_amount FROM ledger_sums WHERE book_account = :book "
                                        "AND account_id = :account_id AND asset_id = :asset_id "
                                        "AND timestamp <= :timestamp ORDER BY sid DESC LIMIT 1",
                               [(":book", book), (":account_id", self.current['account']),
                                (":asset_id", asset_id), (":timestamp", self.current['timestamp'])])
        amount = float(amount) if amount is not None else 0.0
        return amount

    def takeCredit(self, operation_amount):
        money_available = self.getAmount(BookAccount.Money)
        credit = 0
        if money_available < operation_amount:
            credit = operation_amount - money_available
            self.appendTransaction(BookAccount.Liabilities, -credit)
        return credit

    def returnCredit(self, operation_amount):
        current_credit_value = -1.0 * self.getAmount(BookAccount.Liabilities)
        debit = 0
        if current_credit_value > 0:
            if current_credit_value >= operation_amount:
                debit = operation_amount
            else:
                debit = current_credit_value
        if debit > 0:
            self.appendTransaction(BookAccount.Liabilities, debit)
        return debit

    def processActionDetails(self):
        query = executeSQL(self.db, "SELECT sum as amount, category_id, tag_id FROM action_details AS d WHERE pid=:pid",
                           [(":pid", self.current['id'])])
        while query.next():
            amount, self.current['category'], self.current['tag'] = readSQLrecord(query)
            book = BookAccount.Costs if amount < 0 else BookAccount.Incomes
            self.appendTransaction(book, -amount)

    def processAction(self):
        action_amount = self.current['amount']
        if action_amount < 0:
            credit_taken = self.takeCredit(-action_amount)
            self.appendTransaction(BookAccount.Money, -(-action_amount - credit_taken))
        else:
            credit_returned = self.returnCredit(action_amount)
            if credit_returned < action_amount:
                self.appendTransaction(BookAccount.Money, action_amount - credit_returned)
        if self.current['subtype'] == ActionSubtype.SingleIncome:
            self.appendTransaction(BookAccount.Incomes, -action_amount)
        elif self.current['subtype'] == ActionSubtype.SingleSpending:
            self.appendTransaction(BookAccount.Costs, -action_amount)
        else:
            self.processActionDetails()

    def processDividend(self):
        if self.current['peer'] == '':
            logging.error(g_tr('Ledger', "Can't process dividend as bank isn't set for investment account"))
            return
        dividend_amount = self.current['amount']
        tax_amount = self.current['fee_tax']
        credit_returned = self.returnCredit(dividend_amount - tax_amount)
        if credit_returned < dividend_amount:
            self.appendTransaction(BookAccount.Money, dividend_amount - credit_returned)
        self.appendTransaction(BookAccount.Incomes, -dividend_amount)
        if tax_amount:
            self.appendTransaction(BookAccount.Money, -tax_amount)
            self.current['category'] = PredefinedCategory.Taxes
            self.appendTransaction(BookAccount.Costs, tax_amount)

    def processBuy(self):
        seq_id = self.current_seq
        account_id = self.current['account']
        asset_id = self.current['asset']
        qty = self.current['amount']
        price = self.current['price']
        trade_value = round(price * qty, 2) + self.current['fee_tax'] + self.current['coupon']
        sell_qty = 0
        sell_value = 0
        if self.getAmount(BookAccount.Assets, asset_id) < 0:        # Match deals if we have something sold before
            # Get information about last deal
            query = executeSQL(self.db,
                               "SELECT d.open_sid AS open, ABS(o.qty) - SUM(d.qty) AS remainder FROM deals AS d "
                               "LEFT JOIN sequence AS os ON os.type=3 AND os.id=d.open_sid "
                               "JOIN trades AS o ON o.id = os.operation_id "
                               "WHERE d.account_id=:account_id AND d.asset_id=:asset_id "
                               "GROUP BY d.open_sid "
                               "ORDER BY d.close_sid DESC, d.open_sid DESC LIMIT 1",
                               [(":account_id", account_id), (":asset_id", asset_id)])
            last_sid = 0  # Take all Sell operations by default
            reminder = 0
            if query.next():
                # Get sid of Sell trade from the last deal and non-matched reminder of last Sell trade
                last_sid, reminder = readSQLrecord(query)
                # if last Sell is fully matched (reminder>=0) we start from next trade, otherwise we need to shift by 1
                if reminder < 0:
                    last_sid = last_sid - 1
            query = executeSQL(self.db,
                               "SELECT s.id, -t.qty, t.price FROM trades AS t "
                               "LEFT JOIN sequence AS s ON s.type = 3 AND s.operation_id=t.id "
                               "WHERE t.qty < 0 AND t.asset_id = :asset_id AND t.account_id = :account_id "
                               "AND s.id < :sid AND s.id > :last_sid",
                               [(":asset_id", asset_id), (":account_id", account_id),
                                (":sid", seq_id), (":last_sid", last_sid)])
            while query.next():   # Perform match ("closure") of previous Sell trades
                deal_sid, deal_qty, deal_price = readSQLrecord(query)
                if reminder < 0:
                    next_deal_qty = reminder
                    reminder = 0
                else:
                    next_deal_qty = deal_qty
                if (sell_qty + next_deal_qty) >= qty:  # we are buying less or the same amount as was sold previously
                    next_deal_qty = qty - sell_qty
                _ = executeSQL(self.db, "INSERT INTO deals(account_id, asset_id, open_sid, close_sid, qty) "
                                        "VALUES(:account_id, :asset_id, :open_sid, :close_sid, :qty)",
                               [(":account_id", account_id), (":asset_id", asset_id), (":open_sid", deal_sid),
                                (":close_sid", seq_id), (":qty", -next_deal_qty)])
                sell_qty = sell_qty + next_deal_qty
                sell_value = sell_value + (next_deal_qty * deal_price)
                if sell_qty == qty:
                    break
        credit_taken = self.takeCredit(trade_value)
        if trade_value != credit_taken:
            self.appendTransaction(BookAccount.Money, -(trade_value - credit_taken))
        if sell_qty > 0:  # Add result of closed deals
            self.appendTransaction(BookAccount.Assets, sell_qty, sell_value)
            self.current['category'] = PredefinedCategory.Profit
            self.appendTransaction(BookAccount.Incomes, ((price * sell_qty) - sell_value))
        if sell_qty < qty:  # Add new long position
            self.appendTransaction(BookAccount.Assets, (qty - sell_qty), (qty - sell_qty) * price)
        if self.current['coupon']:
            self.current['category'] = PredefinedCategory.Dividends
            self.appendTransaction(BookAccount.Costs, self.current['coupon'])
        if self.current['fee_tax']:
            self.current['category'] = PredefinedCategory.Fees
            self.appendTransaction(BookAccount.Costs, self.current['fee_tax'])

    def processSell(self):
        seq_id = self.current_seq
        account_id = self.current['account']
        asset_id = self.current['asset']
        qty = -self.current['amount']
        price = self.current['price']
        trade_value = round(price * qty, 2) - self.current['fee_tax'] + self.current['coupon']
        buy_qty = 0
        buy_value = 0
        if self.getAmount(BookAccount.Assets, asset_id) > 0:    # Match deals if we have something bought before
            # Get information about last deal
            query = executeSQL(self.db,
                               "SELECT d.open_sid AS open, ABS(coalesce(o.qty, ca.qty_new))- SUM(d.qty) AS remainder "
                               "FROM deals AS d "
                               "LEFT JOIN sequence AS os ON os.id=d.open_sid "
                               "LEFT JOIN trades AS o ON o.id = os.operation_id AND os.type = 3 "
                               "LEFT JOIN corp_actions AS ca ON ca.id = os.operation_id AND os.type = 5 "
                               "WHERE d.account_id=:account_id AND d.asset_id=:asset_id "
                               "GROUP BY d.open_sid "
                               "ORDER BY d.close_sid DESC, d.open_sid DESC LIMIT 1",
                               [(":account_id", account_id), (":asset_id", asset_id)])
            last_sid = 0  # Take all Buy operations by default
            reminder = 0
            if query.next():     # Perform match ("closure") of previous Buy trades
                # Get sid of Buy trade from the last deal and non-matched reminder of last Buy trade
                last_sid, reminder = readSQLrecord(query)
                # if last Buy is fully matched (reminder<=0) we start from next trade, otherwise we need to shift by 1
                if reminder > 0:
                    last_sid = last_sid - 1
            query = executeSQL(self.db,
                               "SELECT * FROM ("
                               "SELECT s.id, t.qty, t.price FROM trades AS t "
                               "LEFT JOIN sequence AS s ON s.type = 3 AND s.operation_id=t.id "
                               "WHERE t.qty > 0 AND t.asset_id = :asset_id AND t.account_id = :account_id "
                               "AND s.id < :sid AND s.id > :last_sid "
                               "UNION ALL "
                               "SELECT s.id, c.qty_new, coalesce(l.value/c.qty_new, 0) AS price FROM corp_actions AS c "
                               "LEFT JOIN sequence AS s ON s.type = 5 AND s.operation_id=c.id " 
                               "LEFT JOIN ledger AS l ON s.id = l.sid AND l.asset_id=c.asset_id_new AND l.value > 0 "
                               "WHERE c.qty_new > 0 AND c.asset_id_new = :asset_id AND c.account_id = :account_id "
                               "AND s.id < :sid AND s.id > :last_sid " 
                               ")ORDER BY id",
                               [(":asset_id", asset_id), (":account_id", account_id),
                                (":sid", seq_id), (":last_sid", last_sid)])
            while query.next():    # Perform match ("closure") of previous Buy trades
                deal_sid, deal_qty, deal_price = readSQLrecord(query)  # deal_sid -> trade_sid
                if reminder > 0:
                    next_deal_qty = reminder
                    reminder = 0
                else:
                    next_deal_qty = deal_qty
                if (buy_qty + next_deal_qty) >= qty:  # we are selling less or the same amount as was bought previously
                    next_deal_qty = qty - buy_qty
                _ = executeSQL(self.db, "INSERT INTO deals(account_id, asset_id, open_sid, close_sid, qty) "
                                        "VALUES(:account_id, :asset_id, :open_sid, :close_sid, :qty)",
                               [(":account_id", account_id), (":asset_id", asset_id), (":open_sid", deal_sid),
                                (":close_sid", seq_id), (":qty", next_deal_qty)])
                buy_qty = buy_qty + next_deal_qty
                buy_value = buy_value + (next_deal_qty * deal_price)
                if buy_qty == qty:
                    break
        credit_returned = self.returnCredit(trade_value)
        if credit_returned < trade_value:
            self.appendTransaction(BookAccount.Money, (trade_value - credit_returned))
        if buy_qty > 0:  # Add result of closed deals
            self.appendTransaction(BookAccount.Assets, -buy_qty, -buy_value)
            self.current['category'] = PredefinedCategory.Profit
            self.appendTransaction(BookAccount.Incomes, (buy_value - (price * buy_qty)))
        if buy_qty < qty:  # Add new short position
            self.appendTransaction(BookAccount.Assets, (buy_qty - qty), (buy_qty - qty) * price)
        if self.current['coupon']:
            self.current['category'] = PredefinedCategory.Dividends
            self.appendTransaction(BookAccount.Incomes, -self.current['coupon'])
        if self.current['fee_tax']:
            self.current['category'] = PredefinedCategory.Fees
            self.appendTransaction(BookAccount.Costs, self.current['fee_tax'])

    def processTrade(self):
        if self.current['peer'] == '':
            logging.error(g_tr('Ledger', "Can't process trade as bank isn't set for investment account"))
            return
        operationTrade = {
            -1: self.processSell,
            1: self.processBuy
        }
        operationTrade[self.current['subtype']]()

    def processTransferOut(self):
        amount = -self.current['amount']
        credit_taken = self.takeCredit(amount)
        self.appendTransaction(BookAccount.Money, -(amount - credit_taken))
        self.appendTransaction(BookAccount.Transfers, amount)

    def processTransferIn(self):
        amount = self.current['amount']
        credit_returned = self.returnCredit(amount)
        if credit_returned < amount:
            self.appendTransaction(BookAccount.Money, (amount - credit_returned))
        self.appendTransaction(BookAccount.Transfers, -amount)

    def processTransferFee(self):
        fee = -self.current['amount']
        credit_taken = self.takeCredit(fee)
        self.current['peer'] = PredefinedPeer.Financial
        self.appendTransaction(BookAccount.Money, -(fee - credit_taken))
        self.current['category'] = PredefinedCategory.Fees
        self.appendTransaction(BookAccount.Costs, fee)

    def processTransfer(self):
        operationTransfer = {
            TransferSubtype.Outgoing: self.processTransferOut,
            TransferSubtype.Fee: self.processTransferFee,
            TransferSubtype.Incoming: self.processTransferIn
        }
        operationTransfer[self.current['subtype']]()

    def processAssetConversion(self):
        seq_id = self.current_seq
        account_id = self.current['account']
        asset_id = self.current['asset']
        qty = self.current['amount']
        buy_qty = 0
        buy_value = 0
        if self.getAmount(BookAccount.Assets, asset_id) < (qty - 2*Setup.CALC_TOLERANCE):
            logging.fatal(g_tr('Ledger', "Conversion failed. Asset amount is not enogh. Date: ")
                          + f"{datetime.fromtimestamp(self.current['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
            return
        query = executeSQL(self.db,
                           "SELECT d.open_sid AS open, ABS(coalesce(o.qty, ca.qty_new))- SUM(d.qty) AS remainder "
                           "FROM deals AS d "
                           "LEFT JOIN sequence AS os ON os.id=d.open_sid "
                           "LEFT JOIN trades AS o ON o.id = os.operation_id AND os.type = 3 "
                           "LEFT JOIN corp_actions AS ca ON ca.id = os.operation_id AND os.type = 5 "
                           "WHERE d.account_id=:account_id AND d.asset_id=:asset_id "
                           "GROUP BY d.open_sid "
                           "ORDER BY d.close_sid DESC, d.open_sid DESC LIMIT 1",
                           [(":account_id", account_id), (":asset_id", asset_id)])
        last_sid = 0  # Take all Buy operations by default
        reminder = 0
        if query.next():  # Perform match ("closure") of previous Buy trades
            # Get sid of Buy trade from the last deal and non-matched reminder of last Buy trade
            last_sid, reminder = readSQLrecord(query)
            # if last Buy is fully matched (reminder<=0) we start from next trade, otherwise we need to shift by 1
            if reminder > 0:
                last_sid = last_sid - 1
        query = executeSQL(self.db,
                           "SELECT * FROM ("
                           "SELECT s.id, t.qty, t.price FROM trades AS t "
                           "LEFT JOIN sequence AS s ON s.type = 3 AND s.operation_id=t.id "
                           "WHERE t.qty > 0 AND t.asset_id = :asset_id AND t.account_id = :account_id "
                           "AND s.id < :sid AND s.id > :last_sid "
                           "UNION ALL "
                           "SELECT s.id, c.qty_new, coalesce(l.value/c.qty_new, 0) AS price FROM corp_actions AS c "
                           "LEFT JOIN sequence AS s ON s.type = 5 AND s.operation_id=c.id "
                           "LEFT JOIN ledger AS l ON s.id = l.sid AND l.asset_id=c.asset_id_new AND l.value > 0 "
                           "WHERE c.qty_new > 0 AND c.asset_id_new = :asset_id AND c.account_id = :account_id "
                           "AND s.id < :sid AND s.id > :last_sid "
                           ")ORDER BY id",
                           [(":asset_id", asset_id), (":account_id", account_id),
                            (":sid", seq_id), (":last_sid", last_sid)])
        while query.next():
            deal_sid, deal_qty, deal_price = readSQLrecord(query)  # deal_sid -> trade_sid
            if reminder > 0:
                next_deal_qty = reminder
                reminder = 0
            else:
                next_deal_qty = deal_qty
            if (buy_qty + next_deal_qty) >= qty:  # we are selling less or the same amount as was bought previously
                next_deal_qty = qty - buy_qty
            _ = executeSQL(self.db, "INSERT INTO deals(account_id, asset_id, open_sid, close_sid, qty) "
                                    "VALUES(:account_id, :asset_id, :open_sid, :close_sid, :qty)",
                           [(":account_id", account_id), (":asset_id", asset_id), (":open_sid", deal_sid),
                            (":close_sid", seq_id), (":qty", next_deal_qty)])
            buy_qty = buy_qty + next_deal_qty
            buy_value = buy_value + (next_deal_qty * deal_price)
            if buy_qty == qty:
                break
        # Withdraw value with old quantity of old asset before conversion
        self.appendTransaction(BookAccount.Assets, -buy_qty, -buy_value)
        # Create the same value with new quantity of new asset after conversion
        self.current['asset'] = self.current['peer']
        self.appendTransaction(BookAccount.Assets, self.current['price'], buy_value)

    # Spin-Off is equal to Buy operation with 0 price
    def processAssetEmission(self):
        operation_details = self.current
        # Values for TIMESTAMP, ACCOUNT_ID remains the same
        self.current['asset'] = operation_details['peer']
        self.current['amount'] = operation_details['price']
        self.current['price'] = 0
        self.current['category'] = 0
        self.current['coupon'] = 0
        self.current['peer'] = None
        self.current['fee_tax'] = 0
        self.current['tag'] = 0
        self.processBuy()

    def processCorporateAction(self):
        operationCorpAction = {
            CorporateAction.Merger: self.processAssetConversion,
            CorporateAction.Split: self.processAssetConversion,
            CorporateAction.SymbolChange: self.processAssetConversion,
            CorporateAction.SpinOff: self.processAssetEmission,
            CorporateAction.StockDividend: self.processAssetEmission
        }
        operationCorpAction[self.current['subtype']]()

    # Rebuild transaction sequence and recalculate all amounts
    # timestamp:
    # -1 - re-build from last valid operation (from ledger frontier)
    #      will asks for confirmation if we have more than SILENT_REBUILD_THRESHOLD operations require rebuild
    # 0 - re-build from scratch
    # any - re-build all operations after given timestamp
    def rebuild(self, from_timestamp=-1, fast_and_dirty=False, silent=True):
        operationProcess = {
            TransactionType.Action: self.processAction,
            TransactionType.Dividend: self.processDividend,
            TransactionType.Trade: self.processTrade,
            TransactionType.Transfer: self.processTransfer,
            TransactionType.CorporateAction: self.processCorporateAction
        }

        if from_timestamp >= 0:
            frontier = from_timestamp
            silent = False
        else:
            frontier = self.getCurrentFrontier()
            operations_count = readSQL(self.db, "SELECT COUNT(id) FROM all_transactions WHERE timestamp >= :frontier",
                               [(":frontier", frontier)])
            if operations_count > self.SILENT_REBUILD_THRESHOLD:
                silent = False
                if QMessageBox().warning(None, g_tr('Ledger', "Confirmation"), f"{operations_count}" +
                                         g_tr('Ledger', " operations require rebuild. Do you want to do it right now?"),
                                         QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
                    return
        if not silent:
            logging.info(g_tr('Ledger', "Re-build ledger from: ") +
                         f"{datetime.fromtimestamp(frontier).strftime('%d/%m/%Y %H:%M:%S')}")
        start_time = datetime.now()
        _ = executeSQL(self.db, "DELETE FROM deals WHERE close_sid >= "
                                "(SELECT coalesce(MIN(id), 0) FROM sequence WHERE timestamp >= :frontier)",
                       [(":frontier", frontier)])
        _ = executeSQL(self.db, "DELETE FROM ledger WHERE timestamp >= :frontier", [(":frontier", frontier)])
        _ = executeSQL(self.db, "DELETE FROM sequence WHERE timestamp >= :frontier", [(":frontier", frontier)])
        _ = executeSQL(self.db, "DELETE FROM ledger_sums WHERE timestamp >= :frontier", [(":frontier", frontier)])
        self.db.commit()

        if fast_and_dirty:  # For 30k operations difference of execution time is - with 0:02:41 / without 0:11:44
            _ = executeSQL(self.db, "PRAGMA synchronous = OFF")
        query = executeSQL(self.db, "SELECT type, id, timestamp, subtype, account, currency, asset, amount, "
                                    "category, price, fee_tax, coupon, peer, tag FROM all_transactions "
                                    "WHERE timestamp >= :frontier", [(":frontier", frontier)])
        while query.next():
            self.current = readSQLrecord(query, named=True)
            seq_query = executeSQL(self.db, "INSERT INTO sequence(timestamp, type, operation_id) "
                                            "VALUES(:timestamp, :type, :operation_id)",
                                   [(":timestamp", self.current['timestamp']), (":type", self.current['type']),
                                    (":operation_id", self.current['id'])])
            self.current_seq = seq_query.lastInsertId()
            operationProcess[self.current['type']]()
            if not silent and (query.at() % 1000) == 0:
                logging.info(g_tr('Ledger', "Processed ") + f"{int(query.at()/1000)}" +
                             g_tr('Ledger', "k records, current frontier: ") +
                             f"{datetime.fromtimestamp(self.current['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
        if fast_and_dirty:
            _ = executeSQL(self.db, "PRAGMA synchronous = ON")

        end_time = datetime.now()
        if not silent:
            logging.info(g_tr('Ledger', "Ledger is complete. Elapsed time: ") + f"{end_time - start_time}" +
                         g_tr('Ledger', ", new frontier: ") + f"{datetime.fromtimestamp(self.current['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
        self.updateBalancesView()
        self.updateHoldingsView()

    def showRebuildDialog(self, parent):
        rebuild_dialog = RebuildDialog(parent, self.getCurrentFrontier())
        if rebuild_dialog.exec_():
            self.rebuild(from_timestamp=rebuild_dialog.getTimestamp(),
                         fast_and_dirty=rebuild_dialog.isFastAndDirty(), silent=False)
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import backtrader as bt
import datetime

app = Flask(__name__)
socketio = SocketIO(app)

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])


def run_strategy():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    data = bt.feeds.GenericCSVData(
        dataname='testdata/000300.2002-2022.csv',

        fromdate=datetime.datetime(2022, 4, 8),
        todate=datetime.datetime(2022, 6, 1),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),

        datetime=0,
        open=1,
        close=2,
        high=3,
        low=4,
        volume=5,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    run_strategy()
    emit('after connect',  {'data':'Lets dance'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)

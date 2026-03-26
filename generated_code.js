// 자동매매 이동평균 교차 전략 (테스트용)
const SMA_PERIOD_SHORT = 5;
const SMA_PERIOD_LONG = 20;

function checkSignals(data) {
  const shortSma = data.slice(-SMA_PERIOD_SHORT).reduce((a, b) => a + b) / SMA_PERIOD_SHORT;
  const longSma = data.slice(-SMA_PERIOD_LONG).reduce((a, b) => a + b) / SMA_PERIOD_LONG;

  if (shortSma > longSma) {
    return "BUY_SIGNAL";
  } else if (shortSma < longSma) {
    return "SELL_SIGNAL";
  }
  return "HOLD";
}

const mockData = Array.from({ length: 30 }, () => Math.random() * 100);
console.log("현재 전략 신호:", checkSignals(mockData));
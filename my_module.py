# import plotly.graph_objects as go

# 샘플 데이터
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 17, 22]

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))
fig.update_layout(
    title="간단한 라인 차트",
    xaxis_title="X 축",
    yaxis_title="Y 축",
    template="plotly_dark",
)

# HTML 파일로 저장 (브라우저에서 바로 확인 가능)
fig.write_html("plotly_chart.html")
print("Plotly 차트가 plotly_chart.html 로 저장되었습니다.")

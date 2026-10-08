// 连接本地MQTT Websocket 9001端口
const client = mqtt.connect('ws://localhost:9001')
let history = []

// 连接成功
client.on('connect', () => {
    console.log("MQTT连接成功！")
    client.subscribe("dormmate/sensor")
})

// 收到传感器消息
client.on('message', (topic, payload) => {
    const data = JSON.parse(payload.toString())
    // 更新页面显示
    document.getElementById('temp').innerText = data.temperature
    document.getElementById('humi').innerText = data.humidity
    document.getElementById('status').innerText = data.status

    history.push(data)
    renderTable()
})

// 渲染历史表格
function renderTable() {
    const tbody = document.getElementById("tableBody")
    tbody.innerHTML = ""
    history.forEach(item => {
        const tr = document.createElement("tr")
        tr.innerHTML = `<td>${item.time}</td><td>${item.temperature}</td><td>${item.humidity}</td><td>${item.status}</td>`
        tbody.appendChild(tr)
    })
}

// 导出CSV按钮逻辑
document.getElementById("exportBtn").onclick = function () {
    if (history.length === 0) {
        alert("没有可导出的记录")
        return
    }
    // UTF-8 BOM 防止Excel中文乱码
    let csv = "\uFEFFtime,temperature,humidity,status\n"
    history.forEach(row => {
        csv += `${row.time},${row.temperature},${row.humidity},${row.status}\n`
    })
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = "dormmate.csv"
    a.click()
    URL.revokeObjectURL(url)
}
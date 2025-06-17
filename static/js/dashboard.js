if (typeof vendasPorVendedor === 'object' && vendasPorVendedor !== null) {
    const labels = Object.keys(vendasPorVendedor);
    const dataValues = Object.values(vendasPorVendedor);

    // GRÁFICO DE BARRA
    const ctxBarra = document.getElementById('graficoVendas').getContext('2d');
    new Chart(ctxBarra, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Vendas (R$)',
                data: dataValues,
                backgroundColor: 'rgba(0, 123, 255, 0.7)',
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // GRÁFICO DE PIZZA
    const ctxPizza = document.getElementById('graficoPizza').getContext('2d');
    new Chart(ctxPizza, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Vendas (%)',
                data: dataValues,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });

    // PLUGIN PARA LINHA VERTICAL PONTILHADA
    const linhaPontilhadaPlugin = {
        id: 'linhaPontilhadaPlugin',
        afterDraw: (chart) => {
            if (chart.tooltip?._active?.length) {
                const ctx = chart.ctx;
                const x = chart.tooltip._active[0].element.x;
                const topY = chart.chartArea.top;
                const bottomY = chart.chartArea.bottom;

                ctx.save();
                ctx.beginPath();
                ctx.setLineDash([5, 5]);
                ctx.moveTo(x, topY);
                ctx.lineTo(x, bottomY);
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#999';
                ctx.stroke();
                ctx.restore();
            }
        }
    };

    // GRÁFICO DE LINHA – Vendas diárias por vendedor
    if (typeof vendasDiariasData === 'object' && vendasDiariasData !== null) {
        const ctxLinha = document.getElementById('graficoLinha').getContext('2d');

        const datasets = vendasDiariasData.vendedores.map((vendedor, index) => {
            const cor = `hsl(${index * 60}, 70%, 50%)`;
            return {
                label: vendedor,
                data: vendasDiariasData.valores[vendedor],
                borderColor: cor,
                backgroundColor: cor,
                fill: false,
                tension: 0.1
            };
        });

        new Chart(ctxLinha, {
            type: 'line',
            data: {
                labels: vendasDiariasData.datas,
                datasets: datasets
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        enabled: true,
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: '' }
                    },
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Vendas (R$)' }
                    }
                }
            },
            plugins: [linhaPontilhadaPlugin]
        });
    }
}
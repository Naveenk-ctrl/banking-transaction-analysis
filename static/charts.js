// Credit vs Debit Pie Chart
const totals = JSON.parse(document.getElementById('totalsData').textContent);
const labels = totals.map(item => item.TransactionType);
const values = totals.map(item => item.Total);

const ctx = document.getElementById('creditDebitChart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: 'Credit vs Debit',
            data: values,
            backgroundColor: ['#00c853', '#d50000'],
            borderWidth: 1
        }]
    },
    options: { responsive: false, plugins: { legend: { position: 'bottom' } } }
});

// Monthly Trend Line Chart
const monthly = JSON.parse(document.getElementById('monthlyData').textContent);
const months = monthly.map(item => item.Month);
const credit = monthly.map(item => item.Credit);
const debit = monthly.map(item => item.Debit);

const ctx2 = document.getElementById('monthlyTrendChart').getContext('2d');
new Chart(ctx2, {
    type: 'line',
    data: {
        labels: months,
        datasets: [
            { label: 'Credit', data: credit, borderColor: '#00c853', fill: false, tension: 0.3 },
            { label: 'Debit', data: debit, borderColor: '#d50000', fill: false, tension: 0.3 }
        ]
    },
    options: { responsive: true, plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true } } }
});



const renderChart = (data, labels) => {
    var ctx = document.getElementById('cat-myChart').getContext('2d');
    ctx.canvas.width = 100;
    ctx.canvas.height = 100;
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Categories',
                data: data,
                backgroundColor: [
                    '#dc6967',
                    '#dc67ce',
                    '#8067dc',
                    '#dcd267',
                    '#67b7dc',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    '#dc6967',
                    '#dc67ce',
                    '#8067dc',
                    '#dcd267',
                    '#67b7dc',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: "Expenses Per Category"
            },
            maintainAspectRatio: true,
            responsive: true,
        },
    });
};
    
const getChartData = () => {
    console.log("fetching");
    fetch("/expenses/expense_category_summary")
        .then((res) => res.json())
        .then((results) => {
            console.log("results", results);
            const category_data = results.expense_category_data;
            const [labels, data] = [
                Object.keys(category_data),
                Object.values(category_data),
            ];
            renderChart(data, labels);
    });
};
document.onload = getChartData();













const renderMChart = (data, labels) => {
    var ctx = document.getElementById('monthly-myChart').getContext('2d');
    ctx.canvas.width = 100;
    ctx.canvas.height = 100;
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Categories',
                data: data,
                backgroundColor: [
                    '#dc6967',
                    '#dc67ce',
                    '#8067dc',
                    '#dcd267',
                    '#67b7dc',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    '#dc6967',
                    '#dc67ce',
                    '#8067dc',
                    '#dcd267',
                    '#67b7dc',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: "Expenses Per Category"
            },
            maintainAspectRatio: true,
            responsive: true,
        },
    });
};
    
const getMonthlyData = () => {
    console.log("fetching");
    fetch("/expenses/expense_monthly_data")
        .then((res) => res.json())
        .then((results) => {
            console.log("results", results);
            const category_data = results.expense_monthly_data;
            const [labels, data] = [
                Object.keys(category_data),
                Object.values(category_data),
            ];
            renderMChart(data, labels);
    });
};
document.onload = getMonthlyData();

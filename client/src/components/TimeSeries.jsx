import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function TimeSeries({ data_set }) {
    console.log(data_set);
    const [chartData, setChartData] = useState({
        labels: Object.keys(data_set).length ? Object.keys(data_set) : [],
        datasets: [
            {
                label: "My First dataset",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: Object.keys(data_set).length ? Object.values(data_set) : [],
            },
        ],
    });
    useEffect(() => {
    if (data_set) {
        const parsedDates = Object.keys(data_set).map(key =>
            new Date(Number(key))
        );
        setChartData(prevChartData => ({
            ...prevChartData,
            labels: parsedDates,
        }));
    }
}, [data_set]);
    useEffect(() => {
        if (data_set) {
            setChartData({
                labels: Object.keys(data_set).length ? Object.keys(data_set) : [],
                datasets: [
                    {
                        label: "My First dataset",
                        fill: false,
                        lineTension: 0.1,
                        backgroundColor: "rgba(75,192,192,0.4)",
                        borderColor: "rgba(75,192,192,1)",
                        borderCapStyle: "butt",
                        borderDash: [],
                        borderDashOffset: 0.0,
                        borderJoinStyle: "miter",
                        pointBorderColor: "rgba(75,192,192,1)",
                        pointBackgroundColor: "#fff",
                        pointBorderWidth: 1,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: "rgba(75,192,192,1)",
                        pointHoverBorderColor: "rgba(220,220,220,1)",
                        pointHoverBorderWidth: 2,
                        pointRadius: 1,
                        pointHitRadius: 10,
                        data: Object.values(data_set).length ? Object.values(data_set) : [],
                    },
                ],
            });
        }
    }, [data_set]);

    return (
        <div>
            <h2>Time Series</h2>
            <Line data={chartData} />
        </div>
    );
}
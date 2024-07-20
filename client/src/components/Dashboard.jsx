import {useEffect, useState } from'react';
import TimeSeries from "./TimeSeries.jsx";

export default function Dashboard() {
    const [timeSeriesData, setTimeSeriesData] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/')
            .then(res => res.json())
            .then(data => {
                console.log(data);
                setTimeSeriesData(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h1>Dashboard</h1>
            <TimeSeries data_set={timeSeriesData} />
        </div>
    );
}
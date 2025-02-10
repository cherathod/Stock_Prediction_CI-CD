import { fetchAndRenderChart } from './chart.js';

document.addEventListener("DOMContentLoaded", () => {
    const stockButtons = document.querySelectorAll(".stock-button");
    
    stockButtons.forEach(button => {
        button.addEventListener("click", () => {
            const symbol = button.dataset.symbol; 
            fetchAndRenderChart(symbol);
        });
    });
});

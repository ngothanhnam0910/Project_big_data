import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import CanvasJSChart from '@canvasjs/vue-charts';
import CanvasJSStockChart from '@canvasjs/vue-stockcharts';

const app = createApp(App)

app.use(CanvasJSChart);
app.use(CanvasJSStockChart);

app.use(router)

app.mount('#app')

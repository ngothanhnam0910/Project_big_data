<script setup>
import {Row, Col, Card, Button, Input, Skeleton} from 'ant-design-vue';
import CanvasJS from '@canvasjs/stockcharts';
import axios from 'axios';
import { ref } from 'vue';

let isLoading = ref(true);
let frequency = 'minute';
let symbol = 'SNS';
var dps1 = [], dps2 = [], dps3 = [];



axios.get(`http://localhost:5000/get_symbol_correlation/${symbol}?frequency=${frequency}`)
    .then(response => {
      response.data.symbol_correlation.forEach(data => {
        dps1.push({ x: new Date(data["recorded_time"]), y: [data["open"], data["high"], data["low"], data["close"]] });
        dps2.push({ x: new Date(data["recorded_time"]), y: data["tweet_count"] });
      });

      isLoading.value = false
    })


let getChart = async(pair) => {
  console.log(pair.toUpperCase());
  isLoading.value = true;
  await axios.get(`http://localhost:5000/get_symbol_correlation/${pair.toUpperCase()}?frequency=${frequency}`)
    .then(response => {
      console.log(response.data);
      dps1 = []; dps2 = [];
      response.data.symbol_correlation.forEach(data => {
        dps1.push({ x: new Date(data["recorded_time"]), y: [data["open"], data["high"], data["low"], data["close"]] });
        dps2.push({ x: new Date(data["recorded_time"]), y: data["tweet_count"] });
        dps3.push({ x: new Date(data["recorded_time"]), y: data["close"] });
      });

      isLoading.value = false
    })
}

let addSymbols = (e) => {
        var suffixes = ["", "K", "M", "B"];
        var order = Math.max(Math.floor(Math.log(Math.abs(e.value)) / Math.log(1000)), 0);
        if (order > suffixes.length - 1) order = suffixes.length - 1;
        var suffix = suffixes[order];
        return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
      }
let options = {
          theme: "light2",
          exportEnabled: true,
          title: {
            text: "Coin Price/ Mentions"
          },
          charts: [{
            toolTip: {
              shared: true
            },
            axisX: {
              lineThickness: 5,
              tickLength: 0,
              labelFormatter: function(e) {
                return "";
              }
            },
            axisY: {
              prefix: "$"
            },
            legend: {
              verticalAlign: "top"
            },
            data: [{
              showInLegend: true,
              name: "Coin Price (in USDT)",
              yValueFormatString: "$#,###.##",
              type: "candlestick",
              dataPoints: dps1
            }]
          }, {
            height: 80,
            toolTip: {
              shared: true
            },
            axisY: {
              prefix: "$",
              labelFormatter: addSymbols
            },
            legend: {
              verticalAlign: "top"
            },
            data: [{
              showInLegend: true,
              name: "Number of mentions",
              yValueFormatString: "#,###.##",
              dataPoints: dps2
            }]
          }],
          navigator: {
            data: [{
              dataPoints: dps3
            }],
            slider: {
              minimum: new Date(2023, 1, 8),
              maximum: new Date(2024, 1, 10)
            }
          }
        }
</script>

<template>
  <div v-if="isLoading == true">
    <Skeleton />
</div>
<div v-if="isLoading == false">
  <div style="display: flex; flex-direction: row; align-items: center; justify-content: end; margin-bottom: 25px;">
    <Input type="text" v-model:value="this.pair" placeholder="Search" style="width: 200px; margin-right: 10px;"></Input>
    <Button @click="getChart(this.pair)">Submit</Button>
  </div>
  <CanvasJSStockChart :options="options" :style="this.styleOptions" />
</div>
</template>

<script>
  import btcData from "../assets/btcusd2018.json";
  
  export default {
    data() {
      
      return {
        chart: null,
        pair: '',
        styleOptions: {
          width: "100%",
          height: "420px"
        }
      }
    },
    methods: {

    }
  }
</script>

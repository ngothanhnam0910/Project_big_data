<!-- App.vue -->
<script setup>
import {Row, Col, Card, Button, Input, Skeleton} from 'ant-design-vue';
import axios from 'axios';
import { ref } from 'vue';
import CanvasJS from '@canvasjs/stockcharts';

let isLoading = ref(true);
let frequency = 'minute';
let symbol = 'SNS';
var dps1 = [], dps2 = [];


axios.get(`http://localhost:5000/get_symbol_tweets/${symbol}?frequency=${frequency}`)
    .then(response => {
      console.log(response);
      response.data.tweets.forEach(data => {
        dps1.push({ x: new Date(data["recorded_time"]), y: data["tweet_count"] });
        dps2.push({ x: new Date(data["recorded_time"]), y: data["sentiment"] });
      });

      isLoading.value = false
    })

let  getCorrelation = async (pairs) => {
  console.log(pairs.toUpperCase());
  isLoading.value = true; 
  await axios.get(`http://localhost:5000/get_symbol_tweets/${pairs.toUpperCase()}?frequency=${frequency}`)
    .then(response => {
      dps1 = [];
      dps2 = [];
      response.data.tweets.forEach(data => {
        dps1.push({ x: new Date(data["recorded_time"]), y: data["tweet_count"] });
        dps2.push({ x: new Date(data["recorded_time"]), y: data["sentiment"] });
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

let  options = {
          exportEnabled: true,
          theme: "light2",
          title: {
            text: `Number of tweets/sentiment`
          },
          subtitles: [{
            text: ""
          }],
          charts: [{
            height: 130,
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
          },
          {
            height: 130,
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
              name: "Sentiment",
              yValueFormatString: "#,###.##",
              dataPoints: dps2
            }]
          }],
          navigator: {
            data: [{
              dataPoints: dps2
            }],
            slider: {
              minimum: new Date(2020, 1, 1),
              maximum: new Date(2024, 11, 1)
            }
          }
        };

</script>
<template>
  <div v-if="isLoading == true">
    <Skeleton />
</div>
<div v-if="isLoading == false">
  <div style="display: flex; flex-direction: row; align-items: center; justify-content: end; margin-bottom: 25px;">
    <Input type="text" v-model:value="this.pair" placeholder="Search" style="width: 200px; margin-right: 10px;"></Input>
    <Button @click="() => {getCorrelation(this.pair);}">Submit</Button>
  </div>
  <CanvasJSStockChart :options="options" :style="this.styleOptions" />
</div>
</template>

<script>
  export default {
    data() {
    
      return {
        chart: null,
        pair: '',
        styleOptions: {
          width: "100%",
          height: "400px"
        }
      }
    }
  }
</script>